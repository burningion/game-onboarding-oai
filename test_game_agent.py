#!/usr/bin/env python3
"""
Test script for Game Generation Agent
"""

import asyncio
import os
from game_generation_agent import GameGenerationAgent

async def test_game_generation():
    """Test basic game scene generation"""
    print("🧪 Testing Game Generation Agent\n")
    
    # Test content
    test_content = """
    CORE VALUES
    Our company values guide everything we do:
    - Innovation: Think outside the box
    - Integrity: Always do the right thing
    - Excellence: Strive for the best
    - Teamwork: Together we achieve more
    - Customer Focus: Put customers first
    """
    
    # Use gpt-4o for testing (o3 requires verification)
    agent = GameGenerationAgent(model="gpt-4o")
    
    try:
        print("1️⃣ Creating agent...")
        await agent.create_agent()
        print("   ✅ Agent created successfully\n")
        
        print("2️⃣ Generating test scene...")
        result = await agent.generate_game_scene(
            scene_name="TestCoreValuesScene",
            onboarding_content=test_content,
            scene_type="collection"
        )
        
        print("   ✅ Scene generated successfully!")
        print(f"   📝 Scene code length: {len(result['scene_code'])} characters")
        print(f"   📦 Assets needed: {result['assets']}")
        print(f"   🎯 Learning objectives: {result['learning_objectives']}")
        print(f"   🎮 Mechanics: {result['mechanics'][:100]}...\n")
        
        # Save test output
        output_path = "test_generated_scene.ts"
        with open(output_path, 'w') as f:
            f.write(result['scene_code'])
        print(f"3️⃣ Test scene saved to: {output_path}")
        
        # Test mini-game generation
        print("\n4️⃣ Testing mini-game generation...")
        mini_game = await agent.generate_mini_game(
            concept="Password Security",
            game_type="puzzle",
            difficulty="medium"
        )
        
        print("   ✅ Mini-game generated successfully!")
        print(f"   🎮 Mini-game type: puzzle")
        print(f"   📝 Code length: {len(mini_game['mini_game_code'])} characters")
        
        print("\n✨ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not set in environment")
        print("Please set your OpenAI API key in .env file")
    else:
        asyncio.run(test_game_generation())