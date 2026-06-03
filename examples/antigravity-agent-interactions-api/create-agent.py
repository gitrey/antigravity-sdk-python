"""Example demonstrating how to create a custom Antigravity agent definition.

This script creates a custom developer agent named 'swe' that has access to:
1. Inline source files defined in the config (e.g. playbook guidelines).
2. A remote GitHub repository cloned directly into its workspace.
"""

from google import genai

# Initialize the standard Google GenAI Client
client = genai.Client()

# Create a custom agent configuration
agent = client.agents.create(
    id="swe",
    base_agent="antigravity-preview-05-2026",
    system_instruction="You are a software engineer.",
    base_environment={
        "type": "remote",
        # Provision sources that will be loaded into the agent's workspace environment
        "sources": [
            {
                "type": "inline",
                "target": ".agents/AGENTS.md",
                "content": """
                Review code for security vulnerabilities,
                license compatibity, and best practices.
                """,
            },
            {
                "type": "repository",
                "source": "https://github.com/gitrey/discount-manager",
                "target": "/workspace/repo",
            },
        ],
    },
)

print(f"Created agent: {agent.id}")

