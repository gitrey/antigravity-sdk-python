from google import genai

client = genai.Client()

# 1. Clean up existing test agent if it exists
try:
    client.agents.delete(id="swe")
    print("Deleted old swe")
except Exception as e:
    pass