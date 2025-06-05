import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, Response, HTTPException, Query
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
import os
import subprocess
from pathlib import Path
import json

from io import BytesIO

app = FastAPI()
openai = AsyncOpenAI()

# Base directory for voice agents
VOICE_AGENT_DIR = Path(__file__).parent / "voice_agent"

def load_voice_configs() -> Dict[str, Dict[str, Any]]:
    """Load voice configurations from voice_agent directories"""
    configs = {}
    
    # Keep the original coach config as default
    configs["coach"] = {
        "default_input": """Alright, team, let's bring the energy—time to move, sweat, and feel amazing!

We're starting with a dynamic warm-up, so roll those shoulders, stretch it out, and get that body ready! Now, into our first round—squats, lunges, and high knees—keep that core tight, push through, you got this!

Halfway there, stay strong—breathe, focus, and keep that momentum going! Last ten seconds, give me everything you've got!

And… done! Take a deep breath, shake it out—you crushed it! Stay hydrated, stay moving, and I'll see you next time!""",
        "instructions": """Voice: High-energy, upbeat, and encouraging, projecting enthusiasm and motivation.

Punctuation: Short, punchy sentences with strategic pauses to maintain excitement and clarity.

Delivery: Fast-paced and dynamic, with rising intonation to build momentum and keep engagement high.

Phrasing: Action-oriented and direct, using motivational cues to push participants forward.

Tone: Positive, energetic, and empowering, creating an atmosphere of encouragement and achievement.""",
        "voice": "coral",
        "states": None
    }
    
    # Load configurations from voice_agent directories
    if VOICE_AGENT_DIR.exists():
        for dir_path in VOICE_AGENT_DIR.iterdir():
            if dir_path.is_dir():
                script_path = dir_path / "script.txt"
                instructor_path = dir_path / "instructor.txt"
                
                conversation_states_path = dir_path / "conversation_states.json"
                
                if script_path.exists() and instructor_path.exists():
                    try:
                        # Read conversation states if available
                        states = None
                        if conversation_states_path.exists():
                            with open(conversation_states_path, 'r') as f:
                                states = json.load(f)
                        
                        # Read the full script content for parsing
                        with open(script_path, 'r') as f:
                            script_content = f.read()
                            
                        # Extract intro dialogue for default
                        lines = script_content.split('\n')
                        input_text = []
                        for i, line in enumerate(lines):
                            if line.strip().startswith(('Coach Blaze:', 'Dr. Red Tape:')):
                                dialogue = line.split(':', 1)[1].strip()
                                if dialogue.startswith('"') and dialogue.endswith('"'):
                                    dialogue = dialogue[1:-1]
                                input_text.append(dialogue)
                                # Just get first few lines for default
                                if len(input_text) >= 3:
                                    break
                            
                        # Read instructor file for voice instructions
                        with open(instructor_path, 'r') as f:
                            instructions = f.read()
                        
                        # Determine voice based on character
                        voice = "coral" if "coach" in dir_path.name.lower() else "onyx"
                        
                        configs[dir_path.name] = {
                            "default_input": ' '.join(input_text[:3]) if input_text else "Welcome to ACME Corporation!",
                            "instructions": instructions,
                            "voice": voice,
                            "states": states,
                            "script_content": script_content
                        }
                    except Exception as e:
                        print(f"Error loading config for {dir_path.name}: {e}")
    
    return configs

# Load audio configurations
AUDIO_CONFIGS = load_voice_configs()


def get_step_content(config: Dict[str, Any], step: Optional[str] = None) -> Dict[str, str]:
    """Get content for a specific step from conversation states"""
    if not step:
        return {
            "input": config["default_input"],
            "instructions": config["instructions"],
            "voice": config["voice"]
        }
    
    # Try to extract from script content based on section number
    if config.get("script_content"):
        script_lines = config["script_content"].split('\n')
        section_key = f"Section {int(step) - 1}:"  # Convert step to 0-based section
        
        # Find the section
        in_section = False
        section_text = []
        character_name = "Coach Blaze" if "coach" in config.get("voice", "") else "Dr. Red Tape"
        
        for i, line in enumerate(script_lines):
            if section_key in line:
                in_section = True
                continue
            elif in_section and f"Section {int(step)}:" in line:
                break
            elif in_section and line.strip():
                # Extract dialogue from this character
                if line.strip().startswith(f"{character_name}:"):
                    dialogue = line.split(':', 1)[1].strip()
                    if dialogue.startswith('"') and dialogue.endswith('"'):
                        dialogue = dialogue[1:-1]
                    section_text.append(dialogue)
        
        if section_text:
            return {
                "input": " ".join(section_text[:5]),  # Use first 5 dialogue lines
                "instructions": config["instructions"],
                "voice": config["voice"]
            }
    
    # Fallback to conversation states
    if config.get("states"):
        for state in config["states"]:
            # Match by number prefix (e.g., "1" matches "1_greeting")
            if state["id"].startswith(f"{step}_"):
                # Combine description and examples for the input
                input_text = state["description"] + "\n\n"
                if state.get("examples"):
                    input_text += " ".join(state["examples"])
                
                return {
                    "input": input_text,
                    "instructions": config["instructions"],
                    "voice": config["voice"]
                }
    
    # If step not found, return default
    return {
        "input": config["default_input"],
        "instructions": config["instructions"],
        "voice": config["voice"]
    }


async def generate_audio_stream(config: Dict[str, str]):
    """Generate audio stream from OpenAI TTS API"""
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=config["voice"],
        input=config["input"],
        instructions=config["instructions"],
        response_format="mp3",  # Using mp3 for web compatibility
    ) as response:
        async for chunk in response.iter_bytes():
            yield chunk


@app.get("/")
async def root():
    """Root endpoint"""
    endpoints = {}
    for name, config in AUDIO_CONFIGS.items():
        endpoint_info = {"url": f"/{name}"}
        if config.get("states"):
            # Extract just the numbers from step IDs
            step_numbers = []
            for state in config["states"]:
                step_num = state["id"].split("_")[0]
                step_numbers.append(step_num)
            endpoint_info["available_steps"] = step_numbers
        endpoints[name] = endpoint_info
    
    return {
        "message": "Audio API Server", 
        "endpoints": endpoints,
        "usage": "Add ?step=<number> to select a specific conversation state (e.g., ?step=1, ?step=2)"
    }


@app.get("/debug/{agent_name}")
async def debug_agent(agent_name: str, step: Optional[str] = Query(None)):
    """Debug endpoint to see what content would be generated"""
    if agent_name not in AUDIO_CONFIGS:
        raise HTTPException(status_code=404, detail=f"Voice agent '{agent_name}' not found")
    
    config = AUDIO_CONFIGS[agent_name]
    step_config = get_step_content(config, step)
    
    return {
        "agent": agent_name,
        "step": step,
        "has_script": bool(config.get("script_content")),
        "has_states": bool(config.get("states")),
        "content_preview": step_config["input"][:200] + "..." if len(step_config["input"]) > 200 else step_config["input"],
        "voice": step_config["voice"]
    }


# Create dynamic endpoints for each voice agent
def create_audio_endpoint(agent_name: str):
    async def audio_endpoint(step: Optional[str] = Query(None, description="Conversation state step ID")):
        if agent_name not in AUDIO_CONFIGS:
            raise HTTPException(status_code=404, detail=f"Voice agent '{agent_name}' not found")
        
        config = AUDIO_CONFIGS[agent_name]
        step_config = get_step_content(config, step)
        
        return StreamingResponse(
            generate_audio_stream(step_config),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"inline; filename={agent_name}_{step or 'default'}.mp3",
                "Cache-Control": "no-cache",
            }
        )
    
    return audio_endpoint


# Register all voice agent endpoints
for agent_name in AUDIO_CONFIGS.keys():
    endpoint_func = create_audio_endpoint(agent_name)
    endpoint_func.__name__ = f"{agent_name}_audio"
    app.add_api_route(
        f"/{agent_name}",
        endpoint_func,
        methods=["GET"],
        summary=f"Generate {agent_name} audio",
        response_class=StreamingResponse
    )


# Add CORS middleware for frontend access
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)