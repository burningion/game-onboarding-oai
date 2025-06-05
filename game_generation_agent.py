#!/usr/bin/env python3
"""
Game Generation Agent using OpenAI Agents SDK
Generates real-time game content based on onboarding documents
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameGenerationAgent:
    """Agent that generates Phaser.js game scenes based on onboarding content"""
    
    def __init__(self, model: str = "o3"):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.agent = None
        
    async def create_agent(self):
        """Create the game generation assistant"""
        instructions = """You are a game development expert specializing in creating educational games for employee onboarding.
        
Your role is to:
1. Analyze onboarding content and transform it into engaging game mechanics
2. Generate Phaser.js scene code for interactive gameplay
3. Create level progression that matches the onboarding flow
4. Design mini-games and challenges that reinforce key concepts
5. Ensure the game is fun, educational, and accessible

When generating game content:
- Use TypeScript and Phaser 3 framework
- Follow the existing game architecture (scenes, config, components)
- Create engaging mechanics that teach through gameplay
- Include clear objectives and feedback
- Add visual polish with animations and effects
- Ensure mobile responsiveness

Game Design Principles:
- Each level should teach specific onboarding concepts
- Use collectibles to represent key information
- Include NPCs for guidance (like Coach Blaze)
- Add challenges that test understanding
- Reward progress with points and achievements
"""
        
        self.agent = await self.client.beta.assistants.create(
            model=self.model,
            instructions=instructions,
            name="Game Generation Agent",
            description="Generates Phaser.js game scenes for employee onboarding",
            tools=[
                {"type": "code_interpreter"},
                {"type": "file_retrieval"}
            ]
        )
        logger.info(f"Created game generation assistant with ID: {self.agent.id}")
        return self.agent
    
    async def generate_game_scene(
        self,
        scene_name: str,
        onboarding_content: str,
        scene_type: str = "platformer",
        existing_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a complete game scene based on onboarding content"""
        
        thread = await self.client.beta.threads.create()
        
        prompt = f"""Generate a Phaser.js game scene for employee onboarding.

Scene Name: {scene_name}
Scene Type: {scene_type}
Onboarding Content:
{onboarding_content}

Requirements:
1. Create a TypeScript scene class extending Phaser.Scene
2. Include preload(), create(), and update() methods
3. Design gameplay that teaches the onboarding concepts
4. Add interactive elements (collectibles, obstacles, NPCs)
5. Include progress tracking and scoring
6. Add visual feedback and animations
7. Ensure smooth controls and physics

{"Existing Code Reference:\n" + existing_code if existing_code else ""}

Generate:
1. Complete scene code (TypeScript)
2. Required assets list
3. Game mechanics explanation
4. Learning objectives mapping
"""
        
        message = await self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )
        
        # Run the assistant
        run = await self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.agent.id
        )
        
        # Wait for completion
        while run.status in ["queued", "in_progress", "requires_action"]:
            await asyncio.sleep(1)
            run = await self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        # Get the response
        messages = await self.client.beta.threads.messages.list(
            thread_id=thread.id,
            order="desc",
            limit=1
        )
        
        response = messages.data[0].content[0].text.value
        
        # Parse the response to extract code and metadata
        result = self._parse_scene_response(response)
        result['scene_name'] = scene_name
        result['timestamp'] = datetime.now().isoformat()
        
        return result
    
    async def generate_game_config(
        self,
        game_title: str,
        scenes: List[str],
        features: List[str]
    ) -> Dict[str, Any]:
        """Generate game configuration and setup files"""
        
        thread = await self.client.threads.create()
        
        prompt = f"""Generate Phaser.js game configuration for an onboarding game.

Game Title: {game_title}
Scenes: {', '.join(scenes)}
Features: {', '.join(features)}

Generate:
1. Game configuration (config.ts)
2. Main app component updates
3. Asset preloader setup
4. Scene management structure
5. Save/load system for progress tracking

Ensure the configuration:
- Supports all listed scenes
- Enables requested features
- Optimizes for performance
- Handles responsive design
- Includes error handling
"""
        
        message = await self.client.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )
        
        run = await self.client.threads.runs.create(
            thread_id=thread.id,
            agent_id=self.agent.id
        )
        
        # Wait for completion
        while run.status in ["queued", "in_progress", "requires_action"]:
            await asyncio.sleep(1)
            run = await self.client.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        messages = await self.client.threads.messages.list(
            thread_id=thread.id,
            order="desc",
            limit=1
        )
        
        response = messages.data[0].content[0].text.value
        return self._parse_config_response(response)
    
    async def generate_mini_game(
        self,
        concept: str,
        game_type: str,
        difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """Generate a mini-game for specific concepts"""
        
        thread = await self.client.threads.create()
        
        prompt = f"""Create a mini-game to teach an onboarding concept.

Concept: {concept}
Game Type: {game_type}
Difficulty: {difficulty}

Mini-game types:
- quiz: Multiple choice questions with visual feedback
- puzzle: Drag-and-drop or matching games
- action: Quick reflex games with concept integration
- simulation: Role-playing scenarios

Generate:
1. Complete mini-game code as a Phaser scene
2. Visual design specifications
3. Scoring and feedback system
4. Integration with main game flow
5. Accessibility considerations
"""
        
        message = await self.client.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )
        
        run = await self.client.threads.runs.create(
            thread_id=thread.id,
            agent_id=self.agent.id
        )
        
        while run.status in ["queued", "in_progress", "requires_action"]:
            await asyncio.sleep(1)
            run = await self.client.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        messages = await self.client.threads.messages.list(
            thread_id=thread.id,
            order="desc",
            limit=1
        )
        
        response = messages.data[0].content[0].text.value
        return self._parse_mini_game_response(response)
    
    async def enhance_existing_scene(
        self,
        scene_code: str,
        enhancement_type: str,
        requirements: List[str]
    ) -> Dict[str, Any]:
        """Enhance an existing game scene with new features"""
        
        thread = await self.client.threads.create()
        
        prompt = f"""Enhance an existing Phaser.js game scene.

Current Scene Code:
```typescript
{scene_code}
```

Enhancement Type: {enhancement_type}
Requirements: {', '.join(requirements)}

Enhancement types:
- visual: Add animations, particles, effects
- gameplay: Add new mechanics or challenges
- accessibility: Improve controls and feedback
- educational: Strengthen learning elements
- performance: Optimize for better FPS

Generate:
1. Updated scene code with enhancements
2. List of changes made
3. New assets required (if any)
4. Performance impact assessment
"""
        
        message = await self.client.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )
        
        run = await self.client.threads.runs.create(
            thread_id=thread.id,
            agent_id=self.agent.id
        )
        
        while run.status in ["queued", "in_progress", "requires_action"]:
            await asyncio.sleep(1)
            run = await self.client.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        messages = await self.client.threads.messages.list(
            thread_id=thread.id,
            order="desc",
            limit=1
        )
        
        response = messages.data[0].content[0].text.value
        return self._parse_enhancement_response(response)
    
    def _parse_scene_response(self, response: str) -> Dict[str, Any]:
        """Parse the agent's response to extract scene code and metadata"""
        result = {
            "scene_code": "",
            "assets": [],
            "mechanics": "",
            "learning_objectives": []
        }
        
        # Extract TypeScript code blocks
        import re
        code_pattern = r"```typescript(.*?)```"
        code_matches = re.findall(code_pattern, response, re.DOTALL)
        if code_matches:
            result["scene_code"] = code_matches[0].strip()
        
        # Extract assets list
        assets_pattern = r"(?:Assets|Required Assets):\s*((?:[-•]\s*.+\n?)+)"
        assets_match = re.search(assets_pattern, response, re.MULTILINE)
        if assets_match:
            assets_text = assets_match.group(1)
            result["assets"] = [line.strip().lstrip('-•').strip() 
                              for line in assets_text.split('\n') if line.strip()]
        
        # Extract mechanics explanation
        mechanics_pattern = r"(?:Game Mechanics|Mechanics):\s*((?:.+\n?)+?)(?=\n\n|\Z)"
        mechanics_match = re.search(mechanics_pattern, response, re.MULTILINE)
        if mechanics_match:
            result["mechanics"] = mechanics_match.group(1).strip()
        
        # Extract learning objectives
        objectives_pattern = r"(?:Learning Objectives|Objectives):\s*((?:[-•]\s*.+\n?)+)"
        objectives_match = re.search(objectives_pattern, response, re.MULTILINE)
        if objectives_match:
            objectives_text = objectives_match.group(1)
            result["learning_objectives"] = [line.strip().lstrip('-•').strip() 
                                           for line in objectives_text.split('\n') if line.strip()]
        
        return result
    
    def _parse_config_response(self, response: str) -> Dict[str, Any]:
        """Parse configuration response"""
        result = {
            "config_code": "",
            "app_updates": "",
            "preloader": "",
            "scene_manager": "",
            "save_system": ""
        }
        
        # Similar parsing logic for different code sections
        import re
        
        # Extract different code sections
        sections = {
            "config": r"```typescript\s*//\s*config\.ts(.*?)```",
            "app": r"```typescript\s*//\s*App\.tsx(.*?)```",
            "preloader": r"```typescript\s*//\s*PreloadScene(.*?)```",
            "scene_manager": r"```typescript\s*//\s*SceneManager(.*?)```",
            "save_system": r"```typescript\s*//\s*SaveSystem(.*?)```"
        }
        
        for key, pattern in sections.items():
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                result[f"{key}_code"] = match.group(1).strip()
        
        return result
    
    def _parse_mini_game_response(self, response: str) -> Dict[str, Any]:
        """Parse mini-game response"""
        result = {
            "mini_game_code": "",
            "visual_design": "",
            "scoring_system": "",
            "integration_notes": "",
            "accessibility": ""
        }
        
        import re
        
        # Extract mini-game code
        code_pattern = r"```typescript(.*?)```"
        code_match = re.search(code_pattern, response, re.DOTALL)
        if code_match:
            result["mini_game_code"] = code_match.group(1).strip()
        
        # Extract other sections
        patterns = {
            "visual_design": r"(?:Visual Design|Design):\s*((?:.+\n?)+?)(?=\n\n|\Z)",
            "scoring_system": r"(?:Scoring|Score System):\s*((?:.+\n?)+?)(?=\n\n|\Z)",
            "integration_notes": r"(?:Integration|Main Game):\s*((?:.+\n?)+?)(?=\n\n|\Z)",
            "accessibility": r"(?:Accessibility):\s*((?:.+\n?)+?)(?=\n\n|\Z)"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, response, re.MULTILINE | re.IGNORECASE)
            if match:
                result[key] = match.group(1).strip()
        
        return result
    
    def _parse_enhancement_response(self, response: str) -> Dict[str, Any]:
        """Parse enhancement response"""
        result = {
            "enhanced_code": "",
            "changes": [],
            "new_assets": [],
            "performance_impact": ""
        }
        
        import re
        
        # Extract enhanced code
        code_pattern = r"```typescript(.*?)```"
        code_match = re.search(code_pattern, response, re.DOTALL)
        if code_match:
            result["enhanced_code"] = code_match.group(1).strip()
        
        # Extract changes list
        changes_pattern = r"(?:Changes Made|Changes):\s*((?:[-•]\s*.+\n?)+)"
        changes_match = re.search(changes_pattern, response, re.MULTILINE)
        if changes_match:
            changes_text = changes_match.group(1)
            result["changes"] = [line.strip().lstrip('-•').strip() 
                               for line in changes_text.split('\n') if line.strip()]
        
        # Extract new assets
        assets_pattern = r"(?:New Assets|Assets Required):\s*((?:[-•]\s*.+\n?)+)"
        assets_match = re.search(assets_pattern, response, re.MULTILINE)
        if assets_match:
            assets_text = assets_match.group(1)
            result["new_assets"] = [line.strip().lstrip('-•').strip() 
                                  for line in assets_text.split('\n') if line.strip()]
        
        # Extract performance impact
        performance_pattern = r"(?:Performance Impact|Performance):\s*((?:.+\n?)+?)(?=\n\n|\Z)"
        performance_match = re.search(performance_pattern, response, re.MULTILINE)
        if performance_match:
            result["performance_impact"] = performance_match.group(1).strip()
        
        return result


# Example usage functions
async def generate_benefits_level():
    """Example: Generate a benefits-themed level"""
    agent = GameGenerationAgent(model="gpt-4o")  # Use gpt-4o until o3 is available
    await agent.create_agent()
    
    onboarding_content = """
    Benefits Information:
    - Health Insurance: Medical, Dental, Vision
    - 401(k) with 6% company match
    - 15 days PTO, 10 holidays
    - Life insurance 2x salary
    - 12 weeks paid parental leave
    - $2000 annual training budget
    """
    
    result = await agent.generate_game_scene(
        scene_name="BenefitsBuffetScene",
        onboarding_content=onboarding_content,
        scene_type="collection"
    )
    
    return result


async def generate_security_mini_game():
    """Example: Generate a security training mini-game"""
    agent = GameGenerationAgent(model="gpt-4o")
    await agent.create_agent()
    
    result = await agent.generate_mini_game(
        concept="Password Security - Create strong passwords and enable 2FA",
        game_type="puzzle",
        difficulty="medium"
    )
    
    return result


if __name__ == "__main__":
    # Test the agent
    async def main():
        # Generate a benefits level
        print("Generating benefits level...")
        benefits_result = await generate_benefits_level()
        
        # Save the generated code
        with open("generated_benefits_scene.ts", "w") as f:
            f.write(benefits_result["scene_code"])
        
        print(f"Generated scene saved!")
        print(f"Assets needed: {benefits_result['assets']}")
        print(f"Learning objectives: {benefits_result['learning_objectives']}")
    
    asyncio.run(main())