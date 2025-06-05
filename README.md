# Gamified Onboarding for OpenAI Agents Hackathon NYC

# Repo structure

This repo uses `uv` for dependencies. You can do a `uv sync`, and you should have all of the Python dependencies to run the repo.

There's a React frontend that lives in `frontend/`, and you can just do an `npm start` to get that running too.

Images, etc. get put in `assets/`.

We use Doppler to manage secrets. To install:

```
brew install gnupg
brew install dopplerhq/cli/doppler
doppler login
```

Followed by a:

```
doppler run -- uv run main.py 
```

# Content Agent - Generate Voice Agents from HR Documents

The Content Agent uses OpenAI's Agents SDK to automatically generate voice agent content from company documents (like employee handbooks). It creates the personality instructions, dialogue scripts, and conversation flows needed for voice-based onboarding agents.

## Workflow Overview

```
┌─────────────────────┐
│   HR Department    │
│  Uploads Documents  │
│  (Handbooks, etc.)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Document Store    │
│  (ACME_docs folder) │
│  • Employee Handbook│
│  • Benefits Guide   │
│  • Code of Conduct │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Content Agent     │
│  (OpenAI Agents)    │
│  • Analyzes docs    │
│  • Extracts topics  │
│  • Generates content│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Generated Files    │
│  • instructor.txt   │
│  • script.txt       │
│  • conversation.json│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Voice Agent       │
│  (Coach Blaze, etc.)│
│  • Interactive      │
│  • Personalized     │
│  • Engaging         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   New Employee      │
│  Onboarding Session │
│  • Voice interaction│
│  • Q&A support      │
│  • Progress tracking│
└─────────────────────┘
```

### Process Flow

1. **Document Upload**: HR uploads company documents (handbooks, policies, guides) to the designated folder
   - Local folder: `ACME_docs/`
   - Cloud storage: Box integration via MCP server (see Box MCP section below)
   
2. **Content Processing**: The Content Agent analyzes documents using OpenAI's Agents SDK to:
   - Extract key topics and information
   - Organize content into conversational sections
   - Generate personality-appropriate dialogue
   
3. **Voice Agent Creation**: Three files are generated:
   - `instructor.txt`: Defines agent personality and behavior
   - `script.txt`: Complete dialogue script with sections
   - `conversation_states.json`: Structured conversation flow
   
4. **Voice Interaction**: The generated voice agent conducts onboarding sessions with new employees
   - Speech-to-speech conversations
   - Context-aware responses
   - Progress tracking
   
5. **Gamified Experience**: Optionally integrate with the game frontend for visual engagement
   - Interactive 2D platformer game
   - Coach Blaze character guides employees
   - Collect core values and complete challenges

## Prerequisites

1. Set your OpenAI API key in `.env`:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

2. Install dependencies (if not already done):
   ```bash
   uv sync
   ```

## Running the Content Agent

### Interactive Mode (Recommended for single agents)

Run the interactive CLI to create a voice agent step-by-step:

```bash
uv run python run_content_agent.py
```

The interactive mode will:
- List available documents in the `ACME_docs/` folder
- Let you choose a document to process
- Ask for the agent's name and personality description
- Generate three files in `voice_agent/<agent_name>/`:
  - `instructor.txt` - Personality and tone instructions
  - `script.txt` - Complete dialogue script
  - `conversation_states.json` - Structured conversation flow

### Batch Mode (For multiple agents)

Create multiple agents at once using a configuration file:

```bash
uv run python run_content_agent.py --batch agent_batch_config.json
```

Example batch config file:
```json
[
  {
    "agent_name": "friendly_hr_specialist",
    "source_document": "ACME_docs/ACME_Employee_Handbook.txt",
    "personality": "Warm and professional HR specialist who makes new employees feel welcome"
  },
  {
    "agent_name": "benefits_expert",
    "source_document": "ACME_docs/ACME_Employee_Handbook.txt",
    "personality": "Enthusiastic benefits specialist who loves helping employees maximize their compensation"
  }
]
```

### Direct Python Usage

You can also use the content agent programmatically:

```python
import asyncio
from content_agent import create_voice_agent_content

async def main():
    result = await create_voice_agent_content(
        source_document="ACME_docs/ACME_Employee_Handbook.txt",
        agent_name="onboarding_specialist",
        agent_personality="Professional HR specialist who is warm and thorough"
    )
    print(result)

asyncio.run(main())
```

## Switching AI Models

By default, the content agent uses `gpt-4o`. To use a different model:

1. Edit `agent_config.py`:
   ```python
   MODEL_NAME = "o3"  # or any other OpenAI model
   ```

2. Or set an environment variable:
   ```bash
   export CONTENT_AGENT_MODEL="o3"
   uv run python run_content_agent.py
   ```

Note: Some models (like o3) require organization verification. Visit https://platform.openai.com/settings/organization/general to verify.

## Generated Files

The content agent creates three files for each voice agent:

1. **instructor.txt** - Defines the agent's personality, tone, and behavioral instructions
2. **script.txt** - A complete dialogue script with sections matching the source document
3. **conversation_states.json** - Structured conversation flow for voice interactions

These files follow the same format as the example Coach Blaze agent in `voice_agent/coach_blaze/`.

# Running the Box MCP server

Assumes your environment variables are set:

```
uvx -p 3.13 --with boxsdk --from mcp-server-box@0.1.2 mcp-server-box
```

Look [here](https://github.com/openai/openai-agents-python/blob/main/examples/mcp/filesystem_example/main.py#L35-L50) for an example for how to wire it up.


```
    async with MCPServerStdio(
        name="Filesystem Server, via uvx",
        params={
            "command": "uvx",
            "args": ["-p", "3.13", "--with", "boxsdk", "--from", "mcp-server-box@0.1.2", "mcp-server-box"],
            "env": {"BOX_CLIENT_ID": os.environ['BOX_CLIENT_ID], "BOX_CLIENT_SECRET": os.environ['BOX_CLIENT_SECRET'], "BOX_FOLDER_ID", os.environ['BOX_FOLDER_ID'] }
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="MCP Filesystem Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)

```

# Future Roadmap

## Phase 1: Enhanced Box Integration (Q1 2025)
- **Full Box MCP Integration**: Seamless document upload/download via Box API
- **Auto-sync**: Automatically detect new HR documents in Box folders
- **Version Control**: Track document versions and regenerate agents on updates
- **Multi-tenant Support**: Separate Box folders for different companies/departments

## Phase 2: Advanced Voice Capabilities (Q2 2025)
- **Multi-language Support**: Generate voice agents in multiple languages
- **Voice Cloning**: Use custom voice profiles for brand consistency
- **Emotion Detection**: Adapt responses based on employee sentiment
- **Accent Adaptation**: Support various accents and dialects

## Phase 3: Enhanced Gamification (Q2 2025)
- **Multiplayer Mode**: New employees onboard together
- **Achievement System**: Unlock badges and rewards
- **Leaderboards**: Friendly competition for onboarding completion
- **Custom Game Themes**: Company-branded game environments

## Phase 4: Analytics & Insights (Q3 2025)
- **Onboarding Analytics**: Track completion rates and pain points
- **Knowledge Gaps**: Identify areas where employees need more help
- **Engagement Metrics**: Measure interaction quality and satisfaction
- **Custom Reports**: Generate insights for HR teams

## Phase 5: AI Personalization (Q3 2025)
- **Adaptive Learning**: Adjust content based on employee role/department
- **Smart Q&A**: Handle complex, context-aware questions
- **Personality Matching**: Match agent personality to employee preferences
- **Dynamic Content**: Generate role-specific onboarding paths

## Phase 6: Enterprise Features (Q4 2025)
- **SSO Integration**: Single sign-on with corporate systems
- **HRIS Integration**: Connect with HR information systems
- **Compliance Tracking**: Ensure mandatory training completion
- **API Platform**: Allow third-party integrations

## Technical Improvements
- **Performance Optimization**: Faster document processing
- **Scalability**: Handle thousands of concurrent users
- **Offline Mode**: Download agents for offline onboarding
- **Mobile Apps**: Native iOS/Android applications