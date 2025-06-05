#!/usr/bin/env python3
"""
Simplified Game Generation Agent using Chat Completions API
Generates real-time game content based on onboarding documents
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameGenerationAgent:
    """Agent that generates Phaser.js game scenes based on onboarding content"""
    
    def __init__(self, model: str = "gpt-4o"):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.system_prompt = """You are a game development expert specializing in creating educational games for employee onboarding using Phaser.js and TypeScript.

Your role is to:
1. Analyze onboarding content and transform it into engaging game mechanics
2. Generate complete, working Phaser.js scene code
3. Create educational gameplay that reinforces key concepts
4. Design mini-games and challenges
5. Ensure the game is fun, educational, and accessible

When generating game content:
- Use TypeScript and Phaser 3 framework
- Create complete scene classes extending Phaser.Scene
- Include preload(), create(), and update() methods
- Add interactive elements (collectibles, obstacles, NPCs)
- Include progress tracking and scoring
- Add visual feedback and animations
- Ensure mobile responsiveness

Always provide:
1. Complete TypeScript scene code
2. List of required assets
3. Game mechanics explanation
4. Learning objectives covered
"""
    
    async def generate_game_scene(
        self,
        scene_name: str,
        onboarding_content: str,
        scene_type: str = "platformer",
        existing_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a complete game scene based on onboarding content"""
        
        prompt = f"""Generate a Phaser.js game scene for employee onboarding.

Scene Name: {scene_name}
Scene Type: {scene_type}
Onboarding Content:
{onboarding_content}

{"Existing Code Reference:\n" + existing_code if existing_code else ""}

Create a complete TypeScript scene that:
- Teaches the onboarding concepts through gameplay
- Uses {scene_type} mechanics
- Includes clear objectives and scoring
- Has engaging visuals and animations

Format your response as:
## Scene Code
```typescript
// Complete scene code here
```

## Required Assets
- List all image/audio assets needed

## Game Mechanics
Explain how the game works

## Learning Objectives
- List what players will learn
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            result = self._parse_scene_response(content)
            result['scene_name'] = scene_name
            result['timestamp'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating scene: {e}")
            raise
    
    async def generate_mini_game(
        self,
        concept: str,
        game_type: str,
        difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """Generate a mini-game for specific concepts"""
        
        prompt = f"""Create a mini-game to teach an onboarding concept.

Concept: {concept}
Game Type: {game_type}
Difficulty: {difficulty}

Create a complete Phaser.js mini-game scene that:
- Focuses on teaching the concept
- Uses {game_type} mechanics (quiz, puzzle, action, or simulation)
- Is appropriately challenging for {difficulty} level
- Can be completed in 2-3 minutes

Format your response as:
## Mini-Game Code
```typescript
// Complete mini-game scene code
```

## Visual Design
Describe the visual elements

## Scoring System
Explain the scoring/feedback system

## Integration Notes
How to integrate with the main game
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content
            return self._parse_mini_game_response(content)
            
        except Exception as e:
            logger.error(f"Error generating mini-game: {e}")
            raise
    
    def _parse_scene_response(self, response: str) -> Dict[str, Any]:
        """Parse the response to extract scene code and metadata"""
        import re
        
        result = {
            "scene_code": "",
            "assets": [],
            "mechanics": "",
            "learning_objectives": []
        }
        
        # Extract TypeScript code
        code_pattern = r"```typescript(.*?)```"
        code_match = re.search(code_pattern, response, re.DOTALL)
        if code_match:
            result["scene_code"] = code_match.group(1).strip()
        
        # Extract sections
        sections = response.split("##")
        for section in sections:
            section_lower = section.lower()
            
            if "required assets" in section_lower or "assets" in section_lower:
                # Extract bullet points
                lines = section.split('\n')
                for line in lines:
                    if line.strip().startswith('-'):
                        result["assets"].append(line.strip()[1:].strip())
            
            elif "game mechanics" in section_lower or "mechanics" in section_lower:
                # Get the content after the header
                lines = section.split('\n')[1:]
                result["mechanics"] = '\n'.join(lines).strip()
            
            elif "learning objectives" in section_lower:
                # Extract bullet points
                lines = section.split('\n')
                for line in lines:
                    if line.strip().startswith('-'):
                        result["learning_objectives"].append(line.strip()[1:].strip())
        
        return result
    
    def _parse_mini_game_response(self, response: str) -> Dict[str, Any]:
        """Parse mini-game response"""
        import re
        
        result = {
            "mini_game_code": "",
            "visual_design": "",
            "scoring_system": "",
            "integration_notes": ""
        }
        
        # Extract TypeScript code
        code_pattern = r"```typescript(.*?)```"
        code_match = re.search(code_pattern, response, re.DOTALL)
        if code_match:
            result["mini_game_code"] = code_match.group(1).strip()
        
        # Extract sections
        sections = response.split("##")
        for section in sections:
            section_lower = section.lower()
            
            if "visual design" in section_lower:
                lines = section.split('\n')[1:]
                result["visual_design"] = '\n'.join(lines).strip()
            
            elif "scoring" in section_lower:
                lines = section.split('\n')[1:]
                result["scoring_system"] = '\n'.join(lines).strip()
            
            elif "integration" in section_lower:
                lines = section.split('\n')[1:]
                result["integration_notes"] = '\n'.join(lines).strip()
        
        return result


# Example usage
async def test_generation():
    """Test the game generation"""
    agent = GameGenerationAgent(model="gpt-4o")
    
    test_content = """
    Employee Benefits:
    - Health Insurance (Medical, Dental, Vision)
    - 401(k) with 6% company match
    - 15 days PTO, 10 holidays
    - Life insurance 2x salary
    - Professional development budget $2000/year
    """
    
    result = await agent.generate_game_scene(
        scene_name="BenefitsCollectionScene",
        onboarding_content=test_content,
        scene_type="collection"
    )
    
    return result


if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🎮 Testing Game Generation Agent...")
        result = await test_generation()
        
        print(f"\n✅ Generated scene: {result['scene_name']}")
        print(f"📝 Code length: {len(result['scene_code'])} characters")
        print(f"📦 Assets: {result['assets']}")
        print(f"🎯 Objectives: {result['learning_objectives']}")
        
        # Save the generated scene
        with open("test_benefits_scene.ts", "w") as f:
            f.write(result['scene_code'])
        print("\n💾 Scene saved to test_benefits_scene.ts")
    
    asyncio.run(main())