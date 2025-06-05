"""
Configuration for the content agent.
Change MODEL_NAME to switch between different OpenAI models.
"""

# Model configuration
# Options: "gpt-4o", "gpt-4-turbo", "o3", "o3-mini", etc.
MODEL_NAME = "gpt-4o"  # Change this to "o3" once your verification is complete

# You can also set this via environment variable
import os
MODEL_NAME = os.getenv("CONTENT_AGENT_MODEL", MODEL_NAME)