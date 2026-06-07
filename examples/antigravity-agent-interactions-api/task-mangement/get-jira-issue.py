"""Example demonstrating how to launch a Jira issue retrieval interaction and stream results in real time.

This script triggers the 'jira-product-owner-agent' with `stream=True` to stream real-time events
(such as step execution, MCP tool calls, model thinking, and final descriptions) without polling.
"""

import os
import sys
from utils import get_client, get_secret

# Initialize GenAI client
client = get_client()

# Fetch target JIRA environment variables loaded from .env or os.environ
jira_instance = os.environ.get("JIRA_INSTANCE", "https://example.atlassian.net")
jira_project_key = os.environ.get("JIRA_PROJECT_KEY", "GENDEV")
jira_cloud_id = os.environ.get("JIRA_CLOUD_ID", "default")
issue_number = os.environ.get("ISSUE_NUMBER", "GENDEV-101")
atlassian_token = get_secret("ATLASSIAN_AUTH_TOKEN")


response_stream = client.interactions.create(
    agent="jira-product-owner-agent",
    input=f"""
    Get the details, description, and acceptance criteria for Jira issue number {issue_number}.
    JIRA instance: {jira_instance}
    JIRA PROJECT KEY: {jira_project_key}
    JIRA_CLOUD_ID: {jira_cloud_id}

    [CREDENTIALS]
    ATLASSIAN_AUTH_TOKEN={atlassian_token}
    """,
    environment="remote",
    stream=True,
    background=True,
)

print("Connecting to Agent and streaming execution steps...\n")

for event in response_stream:
    event_type = getattr(event, "event_type", None)

    if event_type == "interaction.created":
        print(f"\n=== Interaction Created! ID: {event.interaction.id} ===\n")

    elif event_type == "step.start":
        step_type = event.step.type
        print(f"\n>>> [Step Start: {step_type}]")
        if step_type == "function_call":
            print(f"[Call Details]: {event.step}")
        raw_result = getattr(event.step, "result", None)
        if raw_result:
            res_str = str(raw_result)
            print(f"[Result: {step_type}] -> {res_str[:500]}..." if len(res_str) > 500 else res_str)

    elif event_type == "step.delta":
        delta = event.delta
        delta_type = getattr(delta, "type", None)

        if delta_type == "text":
            sys.stdout.write(delta.text)
            sys.stdout.flush()
        elif delta_type == "thinking":
            sys.stdout.write(delta.thinking or "")
            sys.stdout.flush()
        elif delta_type in ("function_call", "mcp_server_tool_call"):
            print(f"\n[Tool Call Delta]: {delta}")
        elif delta_type in ("function_result", "mcp_server_tool_result"):
            print(f"\n[Tool Result Delta]: {delta}")

    elif event_type == "step.stop":
        print("\n<<< [Step Stop]")

    elif event_type == "error":
        print(f"\n!!! [Error]: {event.message}")

    elif event_type == "interaction.completed":
        print("\n\n=== Interaction Completed ===")

print("\nExecution finished.")
