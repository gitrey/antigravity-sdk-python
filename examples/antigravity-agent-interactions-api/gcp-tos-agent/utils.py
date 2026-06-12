"""Shared utility functions and environment configuration for GCP TOS Agent examples."""

import os
from google import genai
from google.genai import types


def load_env():
    """Reads a local .env file and registers its variables in os.environ."""
    curr = os.path.abspath(os.path.dirname(__file__))
    candidates = [
        os.path.join(curr, ".env"),
        os.path.join(os.path.dirname(curr), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(curr)), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(curr))), ".env"),
    ]
    for env_path in candidates:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if (
                        line.strip()
                        and not line.strip().startswith("#")
                        and "=" in line
                    ):
                        key, val = line.strip().split("=", 1)
                        os.environ[key.strip()] = val.strip().strip('"').strip("'")
            break


# Load environment variables on import
load_env()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")


def get_client() -> genai.Client:
    """Initializes and returns a Google GenAI Client configured for Agent Platform."""
    return genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
        http_options=types.HttpOptions(headers={"X-Goog-User-Project": PROJECT_ID}),
    )
