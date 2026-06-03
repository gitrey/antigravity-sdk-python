"""Example demonstrating interaction with the custom-defined 'swe' agent.

This script triggers a new interaction with the custom 'swe' agent (created in
create-agent.py), asking it to perform a code review on a pull request.
"""

from google import genai

# Initialize the standard Google GenAI Client
client = genai.Client()

# Create a synchronous interaction with the custom agent
result = client.interactions.create(
    agent="swe",  # Calls the custom agent ID
    input="Review PR # 1 and provide your feedback",
    environment="remote",  # Run inside the remote environment configured for the agent
)

print("\n--- Review Output ---")
print(result.output_text)