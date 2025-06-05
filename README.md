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