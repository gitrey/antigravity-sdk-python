"""Utility script to query and list custom agents registered in a specific Google Cloud project location.

Unlike the top-level list script, this queries agents within the context of the
project ID specified in the .env or environment configuration.
"""

from utils import get_client, PROJECT_ID

# Initialize GenAI client
client = get_client()

# Fetch agents within the project scope
agents = client.agents.list(parent=f"projects/{PROJECT_ID}/locations/global")

agents_list = agents.agents or []

print(f"Found {len(agents_list)} Antigravity agents:")

for a in agents_list:
    name_id = a.name.split("/")[-1] if a.name else a.id
    print(f"Agent ID: {name_id} (Base: {a.base_agent})")