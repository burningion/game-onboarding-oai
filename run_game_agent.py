#!/usr/bin/env python3
"""
Runner script for the Game Generation Agent
Generates Phaser.js game content based on onboarding documents
"""

import os
import sys
import json
import asyncio
import argparse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from game_generation_agent import GameGenerationAgent
from game_agent_config import (
    GAME_MODEL_NAME, FALLBACK_MODELS, OUTPUT_PATHS, 
    GAME_SETTINGS, SCENE_TEMPLATES
)


def ensure_directories():
    """Create output directories if they don't exist"""
    for path in OUTPUT_PATHS.values():
        Path(path).mkdir(parents=True, exist_ok=True)


async def generate_full_game(
    document_path: str,
    game_name: str,
    model: str = GAME_MODEL_NAME
) -> Dict[str, Any]:
    """Generate a complete game from an onboarding document"""
    
    print(f"\n🎮 Generating game: {game_name}")
    print(f"📄 Source document: {document_path}")
    print(f"🤖 Using model: {model}\n")
    
    # Read the onboarding document
    with open(document_path, 'r') as f:
        content = f.read()
    
    # Initialize the agent
    agent = GameGenerationAgent(model=model)
    
    try:
        await agent.create_agent()
    except Exception as e:
        if "o3" in str(e) and model == "o3":
            print(f"⚠️  Model {model} not available. Trying fallback...")
            model = FALLBACK_MODELS[0]
            agent = GameGenerationAgent(model=model)
            await agent.create_agent()
        else:
            raise
    
    # Parse document sections
    sections = parse_document_sections(content)
    
    # Generate scenes for each section
    generated_scenes = []
    scene_names = []
    
    for i, (section_title, section_content) in enumerate(sections.items()):
        print(f"\n📝 Generating scene {i+1}/{len(sections)}: {section_title}")
        
        scene_name = f"{game_name}Scene{i+1}"
        scene_type = determine_scene_type(section_title, section_content)
        
        result = await agent.generate_game_scene(
            scene_name=scene_name,
            onboarding_content=section_content,
            scene_type=scene_type
        )
        
        # Save the scene
        scene_path = Path(OUTPUT_PATHS["generated_scenes"]) / f"{scene_name}.ts"
        with open(scene_path, 'w') as f:
            f.write(result["scene_code"])
        
        print(f"   ✅ Saved to: {scene_path}")
        print(f"   📦 Assets needed: {len(result['assets'])} items")
        print(f"   🎯 Learning objectives: {len(result['learning_objectives'])} items")
        
        generated_scenes.append(result)
        scene_names.append(scene_name)
    
    # Generate game configuration
    print("\n⚙️  Generating game configuration...")
    config_result = await agent.generate_game_config(
        game_title=game_name.replace('_', ' ').title(),
        scenes=scene_names,
        features=["progress_tracking", "achievements", "save_system", "responsive_design"]
    )
    
    # Save configuration
    config_path = Path(OUTPUT_PATHS["game_configs"]) / f"{game_name}_config.ts"
    with open(config_path, 'w') as f:
        f.write(config_result.get("config_code", ""))
    
    print(f"   ✅ Configuration saved to: {config_path}")
    
    # Generate summary
    summary = {
        "game_name": game_name,
        "model_used": model,
        "source_document": document_path,
        "generated_at": datetime.now().isoformat(),
        "scenes": [
            {
                "name": scene["scene_name"],
                "assets": scene["assets"],
                "learning_objectives": scene["learning_objectives"],
                "mechanics": scene["mechanics"]
            }
            for scene in generated_scenes
        ],
        "total_scenes": len(generated_scenes),
        "config_path": str(config_path)
    }
    
    # Save summary
    summary_path = Path(OUTPUT_PATHS["generated_scenes"]) / f"{game_name}_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 Summary saved to: {summary_path}")
    
    return summary


async def generate_single_scene(
    scene_name: str,
    content: str,
    scene_type: str,
    model: str = GAME_MODEL_NAME
) -> Dict[str, Any]:
    """Generate a single game scene"""
    
    agent = GameGenerationAgent(model=model)
    await agent.create_agent()
    
    result = await agent.generate_game_scene(
        scene_name=scene_name,
        onboarding_content=content,
        scene_type=scene_type
    )
    
    # Save the scene
    scene_path = Path(OUTPUT_PATHS["generated_scenes"]) / f"{scene_name}.ts"
    with open(scene_path, 'w') as f:
        f.write(result["scene_code"])
    
    print(f"✅ Scene saved to: {scene_path}")
    
    return result


async def enhance_scene(
    scene_path: str,
    enhancement_type: str,
    requirements: List[str],
    model: str = GAME_MODEL_NAME
) -> Dict[str, Any]:
    """Enhance an existing scene with new features"""
    
    # Read existing scene
    with open(scene_path, 'r') as f:
        scene_code = f.read()
    
    agent = GameGenerationAgent(model=model)
    await agent.create_agent()
    
    result = await agent.enhance_existing_scene(
        scene_code=scene_code,
        enhancement_type=enhancement_type,
        requirements=requirements
    )
    
    # Save enhanced scene
    enhanced_path = scene_path.replace('.ts', '_enhanced.ts')
    with open(enhanced_path, 'w') as f:
        f.write(result["enhanced_code"])
    
    print(f"✅ Enhanced scene saved to: {enhanced_path}")
    print(f"📝 Changes made: {len(result['changes'])} modifications")
    
    return result


def parse_document_sections(content: str) -> Dict[str, str]:
    """Parse document into sections for scene generation"""
    sections = {}
    
    # Simple section parsing - can be enhanced
    lines = content.split('\n')
    current_section = "Introduction"
    current_content = []
    
    for line in lines:
        # Detect section headers (lines that are all caps or numbered)
        if line.strip() and (line.isupper() or line.strip()[0].isdigit()):
            if current_content:
                sections[current_section] = '\n'.join(current_content)
            current_section = line.strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Add last section
    if current_content:
        sections[current_section] = '\n'.join(current_content)
    
    # If no sections found, treat as single section
    if len(sections) <= 1:
        sections = {
            "Welcome & Introduction": content[:1000],
            "Core Information": content[1000:2000],
            "Policies & Procedures": content[2000:3000],
            "Resources & Support": content[3000:]
        }
    
    return sections


def determine_scene_type(title: str, content: str) -> str:
    """Determine the best scene type based on content"""
    title_lower = title.lower()
    content_lower = content.lower()
    
    if any(word in title_lower for word in ["benefit", "compensation", "perk"]):
        return "collection"
    elif any(word in title_lower for word in ["quiz", "test", "assessment"]):
        return "quiz"
    elif any(word in title_lower for word in ["policy", "procedure", "rule"]):
        return "puzzle"
    elif any(word in title_lower for word in ["scenario", "situation", "case"]):
        return "simulation"
    else:
        return "platformer"


async def interactive_mode():
    """Interactive CLI for game generation"""
    print("\n🎮 Game Generation Agent - Interactive Mode")
    print("=" * 50)
    
    # List available documents
    docs_path = Path("ACME_docs")
    if docs_path.exists():
        documents = list(docs_path.glob("*.txt"))
        print("\n📄 Available documents:")
        for i, doc in enumerate(documents, 1):
            print(f"   {i}. {doc.name}")
        
        # Select document
        while True:
            try:
                choice = input("\nSelect document number (or 'q' to quit): ")
                if choice.lower() == 'q':
                    return
                
                doc_index = int(choice) - 1
                if 0 <= doc_index < len(documents):
                    selected_doc = documents[doc_index]
                    break
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a number.")
    else:
        # Manual path entry
        selected_doc = input("\nEnter document path: ")
        selected_doc = Path(selected_doc)
    
    # Get game name
    game_name = input("\nEnter game name (e.g., 'benefits_adventure'): ")
    if not game_name:
        game_name = "onboarding_game"
    
    # Model selection
    print(f"\n🤖 Model selection (default: {GAME_MODEL_NAME}):")
    print("   1. o3 (requires verification)")
    print("   2. gpt-4o")
    print("   3. gpt-4-turbo-preview")
    
    model_choice = input("\nSelect model (1-3, or press Enter for default): ")
    if model_choice == "2":
        model = "gpt-4o"
    elif model_choice == "3":
        model = "gpt-4-turbo-preview"
    else:
        model = GAME_MODEL_NAME
    
    # Generate game
    print("\n🚀 Starting game generation...")
    result = await generate_full_game(
        document_path=str(selected_doc),
        game_name=game_name,
        model=model
    )
    
    print("\n✨ Game generation complete!")
    print(f"📁 Generated {result['total_scenes']} scenes")
    print(f"📊 Summary: {OUTPUT_PATHS['generated_scenes']}{game_name}_summary.json")


async def main():
    parser = argparse.ArgumentParser(
        description="Generate Phaser.js games from onboarding documents"
    )
    
    parser.add_argument(
        "--document", "-d",
        help="Path to onboarding document"
    )
    parser.add_argument(
        "--name", "-n",
        help="Game name"
    )
    parser.add_argument(
        "--model", "-m",
        default=GAME_MODEL_NAME,
        help=f"Model to use (default: {GAME_MODEL_NAME})"
    )
    parser.add_argument(
        "--scene", "-s",
        help="Generate single scene with name"
    )
    parser.add_argument(
        "--type", "-t",
        default="platformer",
        choices=GAME_SETTINGS["supported_scene_types"],
        help="Scene type"
    )
    parser.add_argument(
        "--enhance", "-e",
        help="Path to scene to enhance"
    )
    parser.add_argument(
        "--enhancement-type",
        choices=["visual", "gameplay", "accessibility", "educational", "performance"],
        help="Type of enhancement"
    )
    
    args = parser.parse_args()
    
    # Ensure output directories exist
    ensure_directories()
    
    if args.enhance:
        # Enhancement mode
        requirements = input("Enter enhancement requirements (comma-separated): ").split(",")
        await enhance_scene(
            scene_path=args.enhance,
            enhancement_type=args.enhancement_type or "visual",
            requirements=[r.strip() for r in requirements],
            model=args.model
        )
    elif args.scene:
        # Single scene mode
        content = input("Enter scene content/description: ")
        await generate_single_scene(
            scene_name=args.scene,
            content=content,
            scene_type=args.type,
            model=args.model
        )
    elif args.document and args.name:
        # Full game generation
        await generate_full_game(
            document_path=args.document,
            game_name=args.name,
            model=args.model
        )
    else:
        # Interactive mode
        await interactive_mode()


if __name__ == "__main__":
    asyncio.run(main())