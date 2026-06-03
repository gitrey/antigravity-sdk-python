"""Utility script to clean up and delete a custom agent definition.

This script deletes the custom 'swe' agent created in previous steps, ensuring
the agent registry is clean.
"""

from google import genai

# Initialize the standard Google GenAI Client
client = genai.Client()

# Clean up existing test agent if it exists in the registry
try:
    client.agents.delete(id="swe")
    print("Deleted old 'swe' agent.")
except Exception as e:
    # Safely ignore if the agent doesn't exist
    print(f"Swe agent deletion skipped or failed: {e}")