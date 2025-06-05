#!/usr/bin/env python3
"""
Test full game generation from onboarding document
"""

import asyncio
import os
from pathlib import Path
from game_generation_agent_simple import GameGenerationAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def generate_complete_game():
    """Generate a complete game from the ACME handbook"""
    
    print("🎮 ACME Onboarding Game Generator")
    print("=" * 50)
    
    # Read the employee handbook
    doc_path = "ACME_docs/ACME_Employee_Handbook.txt"
    with open(doc_path, 'r') as f:
        content = f.read()
    
    # Create the agent
    agent = GameGenerationAgent(model="gpt-4o")
    
    # Parse main sections (simplified)
    sections = [
        {
            "name": "WelcomeScene",
            "type": "platformer",
            "content": content[:500] + "\nIntroduction to ACME Corp and company culture."
        },
        {
            "name": "CoreValuesScene", 
            "type": "collection",
            "content": """
            ACME Core Values:
            - Innovation: We embrace new ideas
            - Integrity: We do the right thing
            - Excellence: We strive for the best
            - Teamwork: We work together
            - Customer Focus: We put customers first
            """
        },
        {
            "name": "BenefitsScene",
            "type": "collection", 
            "content": """
            Employee Benefits:
            - Health Insurance (Medical, Dental, Vision)
            - 401(k) with 6% company match
            - 15 days PTO, 10 holidays
            - Life insurance 2x salary
            - Professional development budget $2000/year
            - 12 weeks paid parental leave
            """
        },
        {
            "name": "SecurityScene",
            "type": "puzzle",
            "content": """
            Security Policies:
            - Strong passwords required (8+ characters)
            - Two-factor authentication mandatory
            - Report suspicious emails immediately
            - Lock computer when away
            - No sharing of credentials
            - Annual security training required
            """
        }
    ]
    
    # Ensure output directory
    output_dir = Path("frontend/src/game/scenes/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_scenes = []
    
    # Generate each scene
    for i, section in enumerate(sections):
        print(f"\n📝 Generating scene {i+1}/{len(sections)}: {section['name']}")
        
        try:
            result = await agent.generate_game_scene(
                scene_name=section['name'],
                onboarding_content=section['content'],
                scene_type=section['type']
            )
            
            # Save the scene
            scene_path = output_dir / f"{section['name']}.ts"
            with open(scene_path, 'w') as f:
                f.write(result['scene_code'])
            
            print(f"   ✅ Saved to: {scene_path}")
            print(f"   📦 Assets: {len(result['assets'])} items")
            print(f"   🎯 Objectives: {len(result['learning_objectives'])} items")
            
            generated_scenes.append({
                "name": section['name'],
                "type": section['type'],
                "assets": result['assets'],
                "objectives": result['learning_objectives']
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Generate a summary
    summary_path = output_dir / "game_summary.json"
    import json
    with open(summary_path, 'w') as f:
        json.dump({
            "game_name": "ACME Onboarding Adventure",
            "scenes": generated_scenes,
            "total_scenes": len(generated_scenes),
            "generated_at": datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n✨ Game generation complete!")
    print(f"📊 Summary saved to: {summary_path}")
    print(f"🎮 Total scenes generated: {len(generated_scenes)}")
    
    # Generate example integration code
    integration_code = f"""// Add to frontend/src/game/config.ts

import PreloadScene from './scenes/PreloadScene';
import MenuScene from './scenes/MenuScene';
{chr(10).join(f"import {scene['name']} from './scenes/generated/{scene['name']}';" for scene in generated_scenes)}

const config: Phaser.Types.Core.GameConfig = {{
  // ... existing config ...
  scene: [
    PreloadScene,
    MenuScene,
    {', '.join(scene['name'] for scene in generated_scenes)}
  ]
}};
"""
    
    print("\n📋 Integration code:")
    print(integration_code)


if __name__ == "__main__":
    from datetime import datetime
    asyncio.run(generate_complete_game())