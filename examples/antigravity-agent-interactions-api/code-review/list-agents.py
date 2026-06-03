from utils import get_client, PROJECT_ID

client = get_client()

agents = client.agents.list(parent=f"projects/{PROJECT_ID}/locations/global")
print(f"Raw Response: {agents.model_dump_json(by_alias=True)}")

agents_list = agents.agents or []

print(f"Found {len(agents_list)} Antigravity agents:")

for a in agents_list:
    print(f"{a}")