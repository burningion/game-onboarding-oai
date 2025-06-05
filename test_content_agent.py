#!/usr/bin/env python3
"""
Test script for the content agent - generates a test voice agent automatically.
"""

import asyncio
from content_agent import create_voice_agent_content


async def test_content_agent():
    """Test the content agent by creating a new voice agent."""
    print("🧪 Testing ACME Content Agent")
    print("=" * 50)
    print("Creating test voice agent from ACME Employee Handbook...")
    
    try:
        result = await create_voice_agent_content(
            source_document="ACME_docs/ACME_Employee_Handbook.txt",
            agent_name="sage_harmony",
            agent_personality="Sage Harmony, ACME's zen-like HR guru with 15 years of experience. Former yoga instructor turned people operations expert who brings mindfulness and balance to onboarding. Speaks with calming wisdom while ensuring every policy detail is crystal clear"
        )
        
        print("\n✅ Test completed!")
        print(f"Result: {result}")
        print("\nGenerated files should be in: voice_agent/sage_harmony/")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_content_agent())