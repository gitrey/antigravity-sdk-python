import os
import subprocess
from google import genai
from google.genai import types


def load_env():
    # Find .env relative to the current file location
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#") and "=" in line:
                    key, val = line.strip().split("=", 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")


# Load environment on import
load_env()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "default")


def get_client() -> genai.Client:
    return genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
        http_options=types.HttpOptions(headers={"X-Goog-User-Project": PROJECT_ID}),
    )


def get_secret(secret_name, env_var_fallback=None):
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
