#!/usr/bin/env python3
"""
Content Agent for ACME Onboarding
Uses OpenAI Agents SDK to process company documents and generate voice agent content.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from agents import Agent, Runner, function_tool
import asyncio
from dotenv import load_dotenv
from agent_config import MODEL_NAME

# Load environment variables from .env file
load_dotenv()


@function_tool
def read_document(file_path: str) -> str:
    """Read and return the contents of a document."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


@function_tool
def save_agent_content(agent_name: str, content_type: str, content: str) -> str:
    """Save generated content for a voice agent."""
    output_dir = Path(f"voice_agent/{agent_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove .txt if already in content_type
    if content_type.endswith('.txt'):
        file_path = output_dir / content_type
    else:
        file_path = output_dir / f"{content_type}.txt"
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully saved {content_type} for {agent_name} at {file_path}"
    except Exception as e:
        return f"Error saving file: {str(e)}"


@function_tool
def save_conversation_states(agent_name: str, states: str) -> str:
    """Save conversation states for a voice agent (expects JSON string)."""
    output_dir = Path(f"voice_agent/{agent_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / "conversation_states.json"
    try:
        # Parse the JSON string to validate it
        parsed_states = json.loads(states)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_states, f, indent=2)
        return f"Successfully saved conversation states for {agent_name} at {file_path}"
    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {str(e)}"
    except Exception as e:
        return f"Error saving conversation states: {str(e)}"


# Create specialized agents for different content generation tasks
instructor_agent = Agent(
    name="Instructor Agent",
    model=MODEL_NAME,
    instructions="""You create personality and tone instructions for voice agents based on company documentation.
    
    When creating an instructor.txt file:
    1. Define a clear personality and identity for the agent
    2. Specify their task and demeanor
    3. Set appropriate tone, enthusiasm, formality, and emotion levels
    4. Include pacing and filler word guidance
    5. Add specific behavioral instructions
    
    Format the output as seen in the Coach Blaze example, with sections for:
    - Personality and Tone (Identity, Task, Demeanor, Tone, Enthusiasm, Formality, Emotion, Filler Words, Pacing, Other details)
    - Instructions (including confirmation behaviors)""",
    tools=[read_document, save_agent_content]
)

script_agent = Agent(
    name="Script Agent",
    model=MODEL_NAME,
    instructions="""You create detailed voice agent scripts based on company documentation.
    
    When creating a script.txt file:
    1. Structure the script in clear, numbered sections
    2. Use the agent's personality consistently throughout
    3. Include specific dialogue with natural speech patterns
    4. Add stage directions and transitions
    5. Cover all key information from the source documents
    6. Keep segments concise (10-12 minutes total)
    
    Format with section headers, agent dialogue, and clear transitions between topics.""",
    tools=[read_document, save_agent_content]
)

conversation_states_agent = Agent(
    name="Conversation States Agent",
    model=MODEL_NAME,
    instructions="""You create structured conversation state JSON files for voice agents.
    
    Each state should include:
    - id: Unique identifier (e.g., "1_greeting", "2_overview")
    - description: Brief description of the state's purpose
    - instructions: Array of specific instructions for the agent
    - examples: Array of example phrases the agent might say
    - transitions: Array of conditions for moving to next states
    
    Ensure states flow logically and cover all content from the script.
    
    IMPORTANT: When calling save_conversation_states, pass the states as a JSON string, not a list.""",
    tools=[read_document, save_conversation_states]
)

content_coordinator = Agent(
    name="Content Coordinator",
    model=MODEL_NAME,
    instructions="""You coordinate the creation of voice agent content from company documents.
    
    Your workflow:
    1. Analyze the source document to understand key information
    2. Determine the appropriate agent personality and approach
    3. Coordinate with specialized agents to create:
       - instructor.txt (personality and instructions)
       - script.txt (detailed dialogue script)
       - conversation_states.json (structured conversation flow)
    4. Ensure all content is consistent and covers the source material
    
    You can create multiple agents with different personalities for the same content.""",
    handoffs=[instructor_agent, script_agent, conversation_states_agent],
    tools=[read_document]
)


async def create_voice_agent_content(
    source_document: str,
    agent_name: str,
    agent_personality: str
) -> Dict[str, str]:
    """
    Create complete voice agent content from a source document.
    
    Args:
        source_document: Path to the source document
        agent_name: Name for the voice agent (used for folder name)
        agent_personality: Description of the agent's personality
    
    Returns:
        Dictionary with paths to created files
    """
    prompt = f"""
    Create voice agent content for "{agent_name}" based on the document at {source_document}.
    
    Agent personality: {agent_personality}
    
    Please:
    1. Read and analyze the source document
    2. Create instructor.txt with personality and tone instructions
    3. Create script.txt with a complete dialogue script
    4. Create conversation_states.json with structured conversation flow
    
    Ensure all content is consistent with the personality and covers key information from the source.
    """
    
    result = await Runner.run(content_coordinator, input=prompt)
    return {"status": "completed", "agent": agent_name, "output": result.final_output}


async def main():
    """Main function to demonstrate content agent usage."""
    print("ACME Content Agent - Voice Agent Generator")
    print("=" * 50)
    
    # Example: Create a new onboarding agent
    print("\nCreating new onboarding agent from ACME Employee Handbook...")
    
    result = await create_voice_agent_content(
        source_document="ACME_docs/ACME_Employee_Handbook.txt",
        agent_name="onboarding_specialist",
        agent_personality="Professional, warm, and thorough HR specialist who makes new employees feel welcome and informed"
    )
    
    print(f"\n{result}")
    
    # Example: Create a benefits-focused agent
    print("\nCreating benefits specialist agent...")
    
    result2 = await create_voice_agent_content(
        source_document="ACME_docs/ACME_Employee_Handbook.txt",
        agent_name="benefits_guru",
        agent_personality="Enthusiastic benefits expert who loves helping employees maximize their compensation package"
    )
    
    print(f"\n{result2}")


if __name__ == "__main__":
    # Ensure OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)
    
    asyncio.run(main())