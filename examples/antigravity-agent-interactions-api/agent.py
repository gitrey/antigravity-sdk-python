"""Example demonstrating a direct interaction with the base Antigravity agent.

This script shows how to trigger a query directly using the base agent model
without first creating a custom agent definition. The agent is tasked with a
research query and asked to save the response to a markdown file in its environment.
"""

from google import genai

# Initialize the standard Google GenAI Client
client = genai.Client()

# Create a direct interaction with the base preview agent model
interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="""
    Save response in agy.md file: What is the current status of the 
    Google Antigravity apps(Agent Manager, IDE, CLI, SDK)?
    """,
    environment="remote",  # Run the agent in a sandboxed remote environment
)

# Print execution details and output returned by the agent
print(f"Interaction ID: {interaction.id}")
print(f"Environment ID: {interaction.environment_id}")
print(f"Output: {interaction.output_text}")

