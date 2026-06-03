import os
import time
from utils import get_client

client = get_client()

jira_instance = os.environ.get("JIRA_INSTANCE", "default")
jira_project_key = os.environ.get("JIRA_PROJECT_KEY", "default")
jira_cloud_id = os.environ.get("JIRA_CLOUD_ID", "default")

result = client.interactions.create(
    agent="code-review-agent",
    input=f"""
    Review PR # 1 in https://github.com/gitrey/widget-types repository
    and provide your feedback.
    JIRA instance: {jira_instance}
    JIRA PROJECT KEY: {jira_project_key}
    JIRA_CLOUD_ID: {jira_cloud_id}
    """,
    environment="remote",
    background=True,
)

print(f"Interaction created with ID: {result.id}. Polling for results...")

while True:
    time.sleep(5)
    status_res = client.interactions.get(id=result.id)
    print(f"Current status: {status_res.status}")
    if status_res.status not in ["in_progress"]:
        result = status_res
        break

print("\n--- Final Review Output ---")
print(result.output_text)
