#!/bin/bash

# Setup script for Box MCP integration with Content Agent

echo "Setting up Box MCP integration for Content Agent..."

# Check if Box MCP server exists
if [ ! -d "/Users/adamanzuoni/mcp-server-box" ]; then
    echo "Error: Box MCP server not found at /Users/adamanzuoni/mcp-server-box"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check for environment variables
echo "Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your Box and OpenAI credentials"
fi

# Install Box MCP server dependencies
echo "Installing Box MCP server dependencies..."
cd /Users/adamanzuoni/mcp-server-box
uv pip install -r requirements.txt
cd -

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials:"
echo "   - OPENAI_API_KEY"
echo "   - BOX_CLIENT_ID"
echo "   - BOX_CLIENT_SECRET"
echo "   - BOX_FOLDER_ID"
echo ""
echo "2. Run the test script:"
echo "   python test_content_agent.py"
echo ""
echo "3. Run the main content agent:"
echo "   python content_agent_mcp.py"