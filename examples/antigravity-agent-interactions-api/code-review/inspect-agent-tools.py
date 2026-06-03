from utils import get_client

client = get_client()

agent = client.agents.get(id="code-review-agent")
print("--- Agent Tools ---")
for tool in agent.tools or []:
    print(tool)
