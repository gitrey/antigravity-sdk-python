"""Utility script to query and inspect configured tools for a specific agent definition.

It retrieves the agent details from the registry and prints all tools it is authorized
to execute.
"""

from utils import get_client

# Initialize GenAI client
client = get_client()

# Fetch target agent definition details from registry
agent = client.agents.get(id="code-review-agent")
print("--- Agent Tools ---")
for tool in agent.tools or []:
    print(tool)
