"""Utility script to query and inspect steps and outputs of a specific agent interaction.

Given an interaction ID, it retrieves the model execution history, tool calls, and final outputs
and prints them in a formatted way.
"""

from utils import get_client

# Initialize GenAI client
client = get_client()

# Query details of a specific past interaction ID
interaction_id = "ChBkYzFmZjdhMWE2MDY0ZWY1EAgaAzM3NioEbWFpbg"
res = client.interactions.get(id=interaction_id)


print("--- MODEL DUMP ---")
import pprint
pprint.pprint(res.model_dump())


