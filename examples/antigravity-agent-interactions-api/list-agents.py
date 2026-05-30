from google import genai

client = genai.Client()

agents = client.agents.list()
print(f"Found {len(agents.agents)} Antigravity agents:")
for a in agents.agents:
    print(f"{a}")