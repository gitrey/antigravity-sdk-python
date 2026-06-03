"""Utility script to query and list all custom Antigravity agent definitions.

This script fetches and lists all custom agents registered under the authenticated
project context.
"""

from google import genai

# Initialize the standard Google GenAI Client
client = genai.Client()

# Retrieve list of all custom agents
agents = client.agents.list()
agents_list = agents.agents or []

print(f"Found {len(agents_list)} Antigravity agents:")
for a in agents_list:
    print(f"Agent ID: {a.id} (Base: {a.base_agent})")