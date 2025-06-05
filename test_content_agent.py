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
            agent_name="test_onboarding_agent",
            agent_personality="Professional and friendly HR specialist who makes new employees feel welcome and thoroughly informed about company policies and benefits"
        )
        
        print("\n✅ Test completed!")
        print(f"Result: {result}")
        print("\nGenerated files should be in: voice_agent/test_onboarding_agent/")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_content_agent())