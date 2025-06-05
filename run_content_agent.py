#!/usr/bin/env python3
"""
Interactive CLI for the ACME Content Agent
Generates voice agent content from company documents.
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from content_agent import create_voice_agent_content
from agent_config import MODEL_NAME

# Load environment variables from .env file
load_dotenv()


def list_available_documents():
    """List all available documents in ACME_docs."""
    docs_dir = Path("ACME_docs")
    if not docs_dir.exists():
        return []
    
    return [f for f in docs_dir.iterdir() if f.is_file() and f.suffix in ['.txt', '.pdf', '.md']]


def get_user_input(prompt: str, default: str = None) -> str:
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("This field is required. Please provide a value.")


async def interactive_mode():
    """Run the content agent in interactive mode."""
    print("\n🤖 ACME Content Agent - Voice Agent Generator")
    print("=" * 60)
    print("This tool creates voice agent content from company documents.")
    print(f"Using OpenAI {MODEL_NAME} model for advanced content generation.")
    print("=" * 60)
    
    # List available documents
    print("\n📄 Available Documents:")
    docs = list_available_documents()
    
    if not docs:
        print("No documents found in ACME_docs/")
        return
    
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc.name}")
    
    # Get document selection
    while True:
        try:
            choice = int(get_user_input("\nSelect a document number"))
            if 1 <= choice <= len(docs):
                selected_doc = docs[choice - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(docs)}")
        except ValueError:
            print("Please enter a valid number")
    
    print(f"\n✅ Selected: {selected_doc.name}")
    
    # Get agent details
    print("\n🎭 Define Your Voice Agent:")
    
    agent_name = get_user_input(
        "Agent folder name (lowercase, use underscores)",
        "friendly_onboarding_agent"
    ).lower().replace(" ", "_")
    
    print("\n📝 Personality Examples:")
    print("  - Professional HR specialist who is warm and thorough")
    print("  - Energetic coach who motivates with sports metaphors")
    print("  - Friendly tech buddy who explains things simply")
    print("  - Knowledgeable mentor who shares wisdom and experience")
    
    personality = get_user_input("\nDescribe the agent's personality")
    
    # Confirmation
    print("\n📋 Summary:")
    print(f"  Document: {selected_doc.name}")
    print(f"  Agent Name: {agent_name}")
    print(f"  Personality: {personality}")
    
    confirm = get_user_input("\nProceed with generation? (y/n)", "y").lower()
    
    if confirm != 'y':
        print("❌ Generation cancelled.")
        return
    
    # Generate content
    print("\n🚀 Generating voice agent content...")
    print("This may take a minute...\n")
    
    try:
        result = await create_voice_agent_content(
            source_document=str(selected_doc),
            agent_name=agent_name,
            agent_personality=personality
        )
        
        print("\n✅ Success! Voice agent content created:")
        print(f"  📁 voice_agent/{agent_name}/")
        print(f"     📄 instructor.txt - Personality and tone instructions")
        print(f"     📄 script.txt - Complete dialogue script")
        print(f"     📄 conversation_states.json - Structured conversation flow")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return
    
    # Offer to create another
    another = get_user_input("\n\nCreate another agent? (y/n)", "n").lower()
    if another == 'y':
        await interactive_mode()


async def batch_mode(config_file: str):
    """Run the content agent in batch mode with a config file."""
    import json
    
    try:
        with open(config_file, 'r') as f:
            configs = json.load(f)
    except Exception as e:
        print(f"Error reading config file: {e}")
        return
    
    print(f"\n🤖 Running batch generation for {len(configs)} agents...")
    
    for config in configs:
        print(f"\n📍 Creating {config['agent_name']}...")
        try:
            await create_voice_agent_content(
                source_document=config['source_document'],
                agent_name=config['agent_name'],
                agent_personality=config['personality']
            )
            print(f"✅ {config['agent_name']} created successfully")
        except Exception as e:
            print(f"❌ Error creating {config['agent_name']}: {e}")


def main():
    """Main entry point."""
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("\nPlease set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Check for batch mode
    if len(sys.argv) > 1:
        if sys.argv[1] == "--batch" and len(sys.argv) > 2:
            asyncio.run(batch_mode(sys.argv[2]))
        else:
            print("Usage:")
            print("  python run_content_agent.py          # Interactive mode")
            print("  python run_content_agent.py --batch config.json  # Batch mode")
    else:
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()