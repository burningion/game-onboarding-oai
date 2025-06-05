# Content Agent

## Overview

The Content Agent is responsible for digesting and processing content from Box folders using the Box MCP server and OpenAI Agent SDK. This agent is part of the Level Up game onboarding system.

## Architecture

Based on the Level Up diagram, the Content Agent:
- Receives requests from the Box Docs Folder
- Processes content using the Content Processing Agent SDK
- Generates scripts that feed into the Story/Script Agent
- Integrates with the overall Level Up game system

## Key Components

### 1. Box Integration
- Uses Box MCP server to access folder contents
- Processes documents from designated Box folders
- Maintains sync with Box content updates

### 2. Content Processing
- Utilizes OpenAI Agent SDK for content analysis
- Extracts key information from documents
- Structures content for game onboarding use

### 3. Script Generation
- Transforms processed content into game-ready scripts
- Ensures compatibility with Story/Script Agent requirements
- Maintains narrative consistency

## Implementation

The Content Agent is implemented using:
- **OpenAI Agents SDK**: For intelligent content processing
- **Box MCP Server**: For Box folder integration
- **Python**: Primary implementation language
- **Async/Await**: For efficient content processing

## Agent Flow

1. **Content Discovery**: Monitors Box folder for new/updated content
2. **Content Analysis**: Processes documents using AI capabilities
3. **Script Generation**: Creates structured scripts for game use
4. **Handoff**: Passes generated scripts to Story/Script Agent

## Configuration

Required environment variables:
- `OPENAI_API_KEY`: OpenAI API authentication
- `BOX_CLIENT_ID`: Box application credentials
- `BOX_CLIENT_SECRET`: Box application secret
- `BOX_FOLDER_ID`: Target Box folder for content

## Usage

```python
from content_agent import ContentAgent

# Initialize the agent
content_agent = ContentAgent(
    name="Content Processor",
    instructions="Process Box folder content and generate game scripts",
    box_folder_id=os.getenv("BOX_FOLDER_ID")
)

# Run the agent
result = await content_agent.process_folder()
```