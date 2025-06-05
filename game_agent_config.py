"""
Configuration for Game Generation Agent
"""

import os

# Model configuration
# Note: o3 requires organization verification
# Visit https://platform.openai.com/settings/organization/general
GAME_MODEL_NAME = os.getenv("GAME_AGENT_MODEL", "o3")

# Fallback models if o3 is not available
FALLBACK_MODELS = ["gpt-4o", "gpt-4-turbo-preview"]

# Agent configuration
AGENT_CONFIG = {
    "name": "Game Generation Agent",
    "description": "Generates Phaser.js game content for employee onboarding",
    "temperature": 0.7,
    "max_tokens": 4000,
}

# Game generation settings
GAME_SETTINGS = {
    "default_scene_type": "platformer",
    "supported_scene_types": ["platformer", "collection", "puzzle", "quiz", "simulation"],
    "default_difficulty": "medium",
    "difficulties": ["easy", "medium", "hard"],
    "mini_game_types": ["quiz", "puzzle", "action", "simulation"],
}

# Output paths
OUTPUT_PATHS = {
    "generated_scenes": "frontend/src/game/scenes/generated/",
    "generated_assets": "frontend/public/assets/generated/",
    "game_configs": "frontend/src/game/configs/",
}

# Scene templates
SCENE_TEMPLATES = {
    "platformer": {
        "physics": {"gravity": {"x": 0, "y": 300}},
        "player_speed": 160,
        "jump_velocity": -330,
    },
    "collection": {
        "physics": {"gravity": {"x": 0, "y": 0}},
        "player_speed": 200,
        "collection_radius": 50,
    },
    "puzzle": {
        "physics": {"gravity": {"x": 0, "y": 0}},
        "drag_enabled": True,
        "snap_distance": 30,
    },
    "quiz": {
        "physics": None,
        "time_limit": 30,
        "points_per_correct": 100,
    },
}

# Asset generation prompts
ASSET_PROMPTS = {
    "character": "Create a friendly, professional character sprite for {role}",
    "background": "Create a {theme} themed background for onboarding",
    "collectible": "Create an icon representing {concept}",
    "obstacle": "Create a challenge/obstacle representing {challenge}",
}

# Learning objective mappings
OBJECTIVE_MAPPINGS = {
    "core_values": ["innovation", "integrity", "excellence", "teamwork", "customer_focus"],
    "benefits": ["health", "retirement", "time_off", "development", "wellness"],
    "policies": ["conduct", "security", "communication", "safety", "compliance"],
    "procedures": ["onboarding", "reporting", "requests", "feedback", "training"],
}