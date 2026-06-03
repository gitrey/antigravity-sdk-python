"""Example demonstrating how to launch a code review and stream results in real time.

This script triggers the 'code-review-agent' with `stream=True` and listens to
real-time stream events (such as tool start/stop, text updates, code execution logs,
and final outputs). It also filters credentials/secrets to prevent leakage in stdout.
"""

import os
import sys
from utils import get_client, get_secret

# Fetch credentials (falls back to local environment vars if not in GCP Secret Manager)
github_token = get_secret("GITHUB_REPO_ACCESS_TOKEN", "GITHUB_TOKEN")
atlassian_token = get_secret("ATLASSIAN_AUTH_TOKEN", "ATLASSIAN_TOKEN")

# Fetch config values loaded from environment or .env
repo_name = os.environ.get("REPO", "default")
pr_num = os.environ.get("PR_NUMBER", "default")
jira_instance = os.environ.get("JIRA_INSTANCE", "default")
jira_project_key = os.environ.get("JIRA_PROJECT_KEY", "default")
jira_cloud_id = os.environ.get("JIRA_CLOUD_ID", "default")

# Initialize GenAI client
client = get_client()


def redact_secrets(text, secrets):
    if not text:
        return text
    for s in secrets:
        if s and len(s) > 5:
            text = text.replace(s, "[REDACTED]")
    return text

# List of secrets to protect in stdout
protect_secrets = [github_token, atlassian_token]

response_stream = client.interactions.create(
    agent="code-review-agent",
    input=f"""
    Review PR #{pr_num} in https://github.com/{repo_name} repository
    and provide your feedback.
    JIRA instance: {jira_instance}
    JIRA PROJECT KEY: {jira_project_key}
    JIRA_CLOUD_ID: {jira_cloud_id}

    [CREDENTIALS]
    GITHUB_REPO_ACCESS_TOKEN={github_token}
    ATLASSIAN_AUTH_TOKEN={atlassian_token}
    """,
    environment="remote",
    stream=True,
    background=True,
)

print("Connecting to Agent and listening to the stream...\n")

for event in response_stream:
    event_type = getattr(event, "event_type", None)

    if event_type == "interaction.created":
        print(f"\n=== Interaction Created! ID: {event.interaction.id} ===\n")

    elif event_type == "step.start":
        step_type = event.step.type
        print(f"\n\n>>> [Step Start: {step_type}]")
        
        raw_result = getattr(event.step, "result", None)
        if raw_result:
            redacted_result = redact_secrets(str(raw_result), protect_secrets)
            if step_type == "mcp_server_tool_result":
                print(f"[Result: MCP tool result] -> {redacted_result}")
            elif step_type == "code_execution_result":
                print(f"[Result: Code execution result] -> {redacted_result}")
            elif step_type == "function_result":
                print(f"[Result: Function result] -> {redacted_result}")

    elif event_type == "step.delta":
        delta = event.delta
        delta_type = getattr(delta, "type", None)

        if delta_type == "text":
            sys.stdout.write(redact_secrets(delta.text, protect_secrets))
            sys.stdout.flush()
        elif delta_type == "arguments_delta":
            sys.stdout.write(redact_secrets(delta.arguments or "", protect_secrets))
            sys.stdout.flush()
        elif delta_type == "code_execution_call":
            print(f"\n[Tool Call: Code Execution] -> {redact_secrets(delta.arguments, protect_secrets)}")
        elif delta_type == "mcp_server_tool_call":
            print(f"\n[Tool Call: MCP {delta.server_name}.{delta.name}]")
        elif delta_type == "code_execution_result":
            print(f"\n[Tool Result: Code Execution] -> {redact_secrets(delta.result, protect_secrets)}")
        elif delta_type == "mcp_server_tool_result":
            print(f"\n[Tool Result: MCP tool returned result]")

    elif event_type == "step.stop":
        print("\n<<< [Step Stop]")

    elif event_type == "error":
        print(f"\n!!! [Error Event]: {redact_secrets(event.message, protect_secrets)}")

    elif event_type == "interaction.completed":
        print("\n\n=== Interaction Completed ===")

print("\nStream finished.")
