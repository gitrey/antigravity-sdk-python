"""Script to register or update the custom 'swe-reviewer' Agent Platform configuration.

Idempotently clears any pre-existing definition and registers the software engineering agent
provisioned with secure Cloud Storage source workspace mounts and outbound network allowlists.
"""

from utils import PROJECT_ID, get_client

# Initialize the Agent Platform GenAI Client
client = get_client()

try:
    client.agents.delete(id="swe-reviewer")
except Exception:
    pass

# Create a custom agent configuration
agent = client.agents.create(
    id="swe-reviewer",
    base_agent="antigravity-preview-05-2026",
    system_instruction="You are a software engineer.",
    base_environment={
        "type": "remote",
        "network": {"allowlist": [{"domain": "*"}]},
        # Provision sources that will be loaded into the agent's workspace environment
        "sources": [
            {
                "type": "gcs",
                "source": f"gs://{PROJECT_ID}-agents/.agents/AGENTS.md",
                "target": ".agents/AGENTS.md",
            }
        ],
    },
)

print(f"Created agent: {agent.id}")
