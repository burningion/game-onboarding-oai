# Testing the Content Agent

This guide provides instructions for testing the Content Agent independently, without requiring Box MCP server integration.

## Prerequisites

1. **Environment Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies
   pip install openai-agents pydantic python-dotenv
   ```

2. **API Key Configuration**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=sk-your-actual-key-here
   ```

## Test Scenarios

### 1. Basic Content Processing Test

Create a file `test_basic.py`:

```python
import asyncio
from content_agent import process_educational_content

async def test_basic():
    # Test with educational content
    content = """
    Introduction to Machine Learning
    
    Learning Objectives:
    - Understand what machine learning is
    - Learn about supervised vs unsupervised learning
    - Explore common ML algorithms
    - Practice with real datasets
    
    Machine learning is a subset of AI that enables computers to learn from data.
    """
    
    result = await process_educational_content(content, "ML_Basics.txt")
    print(f"Result: {result}")

asyncio.run(test_basic())
```

### 2. Guardrail Testing

Test the educational content guardrail:

```python
import asyncio
from content_agent import process_educational_content

async def test_guardrails():
    # Test 1: Valid educational content
    valid_content = """
    Physics: Newton's Laws of Motion
    
    Objectives:
    - Understand the three laws of motion
    - Apply laws to real-world scenarios
    - Solve physics problems
    """
    
    # Test 2: Non-educational content (should be blocked)
    invalid_content = """
    My favorite recipe for chocolate cake:
    Mix flour, sugar, and cocoa powder...
    """
    
    print("Testing valid educational content:")
    result1 = await process_educational_content(valid_content, "Physics.txt")
    print(f"Result: {result1}\n")
    
    print("Testing non-educational content:")
    result2 = await process_educational_content(invalid_content, "Recipe.txt")
    print(f"Result: {result2}")

asyncio.run(test_guardrails())
```

### 3. Script Generation Test

Test the script generation functionality:

```python
import asyncio
from content_agent import ContentOutput, generate_game_script

async def test_script_generation():
    # Create sample processed content
    processed_content = ContentOutput(
        title="Introduction to Coding",
        summary="Learn basic programming concepts through interactive gameplay",
        key_points=[
            "Variables and data types",
            "Control flow (if/else)",
            "Loops and iteration",
            "Functions"
        ],
        script_elements={
            "difficulty": "beginner",
            "age_group": "10-14",
            "game_style": "adventure"
        },
        metadata={
            "subject": "Computer Science",
            "duration": "30 minutes"
        }
    )
    
    # Generate game script
    script = await generate_game_script(processed_content)
    print(f"Generated Script:\n{script}")

asyncio.run(test_script_generation())
```

### 4. End-to-End Pipeline Test

Test the complete pipeline from raw content to game script:

```python
import asyncio
from agents import Runner
from content_agent import triage_agent

async def test_full_pipeline():
    # Educational content about space
    space_content = """
    Journey to the Solar System
    
    Learning Objectives:
    - Identify all planets in our solar system
    - Understand planetary characteristics
    - Learn about orbits and gravity
    - Explore space exploration history
    
    Content:
    Our solar system consists of the Sun and eight planets. Each planet has unique
    characteristics. Mercury is the closest to the Sun, while Neptune is the farthest.
    The inner planets (Mercury, Venus, Earth, Mars) are rocky, while the outer planets
    (Jupiter, Saturn, Uranus, Neptune) are gas giants.
    
    Key Facts:
    - Earth is the only known planet with life
    - Jupiter is the largest planet
    - Saturn has prominent rings
    - Mars is called the "Red Planet"
    """
    
    # Run through the triage agent
    result = await Runner.run(triage_agent, f"""
    Document: Solar System Educational Module
    
    Please process this educational content and create a game script:
    
    {space_content}
    """)
    
    print(f"Pipeline Result:\n{result.final_output}")
    print(f"\nTrace ID: {result.trace_id}")

asyncio.run(test_full_pipeline())
```

## Mock Box Integration Test

To test the Box integration without the actual Box MCP server:

```python
import asyncio
from typing import List, Dict, Any

class MockBoxClient:
    """Mock Box client for testing"""
    
    async def list_folder_contents(self, folder_id: str) -> Dict[str, Any]:
        return {
            "entries": [
                {"id": "123", "name": "Math_Basics.pdf", "type": "file"},
                {"id": "124", "name": "Science_Lab.docx", "type": "file"}
            ]
        }
    
    async def read_file(self, file_id: str) -> str:
        mock_contents = {
            "123": """
            Mathematics: Introduction to Algebra
            
            Learning Goals:
            - Understand variables and expressions
            - Solve simple equations
            - Apply algebra to word problems
            """,
            "124": """
            Science Lab: Chemical Reactions
            
            Objectives:
            - Observe chemical reactions safely
            - Understand reactants and products
            - Balance chemical equations
            """
        }
        return mock_contents.get(file_id, "File not found")

# Test with mock client
async def test_with_mock_box():
    mock_client = MockBoxClient()
    
    # Simulate processing folder contents
    folder_contents = await mock_client.list_folder_contents("test_folder")
    
    for file_info in folder_contents["entries"]:
        if file_info["type"] == "file":
            content = await mock_client.read_file(file_info["id"])
            print(f"\nProcessing: {file_info['name']}")
            
            # Use the content agent to process
            from content_agent import process_educational_content
            result = await process_educational_content(content, file_info['name'])
            print(f"Result: {result}")

asyncio.run(test_with_mock_box())
```

## Performance Testing

Test the agent with various content sizes:

```python
import asyncio
import time
from content_agent import process_educational_content

async def performance_test():
    test_cases = [
        ("small", "Python basics: variables are containers for data."),
        ("medium", "Python Programming Course\n" + "\n".join([
            f"Lesson {i}: Topic details..." for i in range(1, 11)
        ])),
        ("large", "Comprehensive Programming Guide\n" + "\n".join([
            f"Chapter {i}: " + "Content " * 100 for i in range(1, 21)
        ]))
    ]
    
    for size, content in test_cases:
        start_time = time.time()
        result = await process_educational_content(content, f"{size}_test.txt")
        end_time = time.time()
        
        print(f"\n{size.upper()} content:")
        print(f"- Processing time: {end_time - start_time:.2f} seconds")
        print(f"- Success: {'error' not in result}")

asyncio.run(performance_test())
```

## Running Tests

1. **Quick Test**
   ```bash
   python test_basic.py
   ```

2. **Full Test Suite**
   Create a `run_all_tests.py`:
   ```python
   import asyncio
   import sys
   
   async def run_all_tests():
       print("=" * 50)
       print("CONTENT AGENT TEST SUITE")
       print("=" * 50)
       
       # Import and run each test
       tests = [
           ("Basic Processing", "test_basic"),
           ("Guardrails", "test_guardrails"),
           ("Script Generation", "test_script_generation"),
           ("Full Pipeline", "test_full_pipeline"),
           ("Mock Box Integration", "test_with_mock_box"),
           ("Performance", "performance_test")
       ]
       
       for test_name, test_module in tests:
           print(f"\n[{test_name}]")
           try:
               # Dynamic import and run
               exec(f"from {test_module} import test_function")
               await test_function()
               print("✓ PASSED")
           except Exception as e:
               print(f"✗ FAILED: {e}")
   
   asyncio.run(run_all_tests())
   ```

## Debugging Tips

1. **Enable Debug Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check Agent Traces**
   - View traces at: https://platform.openai.com/traces
   - Use the trace_id from results to debug specific runs

3. **Test Individual Agents**
   ```python
   from agents import Runner
   from content_agent import content_processing_agent
   
   result = await Runner.run(
       content_processing_agent,
       "Your test content here"
   )
   ```

## Common Issues

1. **API Key Not Found**
   - Ensure `.env` file exists and contains valid `OPENAI_API_KEY`
   - Check environment variable is loaded: `print(os.getenv("OPENAI_API_KEY"))`

2. **Import Errors**
   - Verify `openai-agents` is installed: `pip show openai-agents`
   - Check Python version: `python --version` (requires 3.8+)

3. **Async Errors**
   - Always use `asyncio.run()` for top-level async functions
   - Don't mix sync and async code without proper handling

## Next Steps

After testing the Content Agent independently:

1. **Integration Testing**: Test with actual Box MCP server
2. **Load Testing**: Process multiple documents concurrently
3. **Error Handling**: Test edge cases and error scenarios
4. **Monitoring**: Set up logging and metrics for production use