"""Shared configuration and utility functions for task management examples.

This module provides common helper functions to load local environmental variables,
initialize the Google GenAI Client with billing headers, and retrieve sensitive tokens
from Google Cloud Secret Manager.
"""

import os
import subprocess
from google import genai
from google.genai import types


def load_env():
    """Reads a local .env file manually and registers its variables in os.environ.
    
    This avoids dependencies on external dotenv libraries while keeping scripts portable.
    """
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
                    if line.strip() and not line.strip().startswith("#") and "=" in line:
                        key, val = line.strip().split("=", 1)
                        os.environ[key.strip()] = val.strip().strip('"').strip("'")
            break


# Load environmental variables immediately on module import
load_env()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "default")


def get_client() -> genai.Client:
    """Initializes and returns a Google GenAI Client configured for Vertex AI.
    
    Attaches the required X-Goog-User-Project billing header to verify access rights.
    """
    return genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
        http_options=types.HttpOptions(headers={"X-Goog-User-Project": PROJECT_ID}),
    )


def get_secret(secret_name, env_var_fallback=None):
    """Retrieves a secret version value from Google Cloud Secret Manager.
    
    If the secret query fails or env_var_fallback is provided and set,
    it falls back to reading from local environment variables.
    """
    if env_var_fallback:
        fallback = os.environ.get(env_var_fallback)
        if fallback:
            return fallback
    try:
        result = subprocess.run(
            [
                "gcloud",
                "secrets",
                "versions",
                "access",
                "latest",
                f"--secret={secret_name}",
                f"--project={PROJECT_ID}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error fetching secret {secret_name}: {e}")
        return ""
