"""Example demonstrating real-time interaction streaming with the custom 'swe-reviewer' agent.

This script launches an asynchronous background interaction with the custom 'swe-reviewer' agent
(registered via swe-review-agent.py), instructing it to evaluate a remote GitHub pull request
and stream execution steps and thought deltas back in real time.
"""

import sys
from utils import PROJECT_ID, get_client

# Initialize the Agent Platform GenAI Client
client = get_client()

# Create an asynchronous background interaction with streaming enabled
response_stream = client.interactions.create(
    agent="swe-reviewer",  # Calls the custom agent ID
    input="Review PR in https://github.com/gitrey/widget-types and provide your feedback",
    environment="remote",  # Run inside the remote environment configured for the agent
    stream=True,
    background=True,
)

print("Connecting to secure remote sandbox and listening to execution stream...\n")

for event in response_stream:
    event_type = getattr(event, "event_type", None)

    if event_type == "interaction.created":
        print(f"=== Interaction Created (ID: {event.interaction.id}) ===\n")

    elif event_type == "step.start":
        step_type = getattr(event.step, "type", "unknown")
        print(f"\n>>> [Step Started: {step_type}]", flush=True)

    elif event_type == "step.delta":
        delta = getattr(event, "delta", None)
        if delta:
            delta_type = getattr(delta, "type", None)
            if delta_type == "text":
                sys.stdout.write(delta.text)
                sys.stdout.flush()
            elif delta_type == "code_execution_call":
                print(f"\n[Executing Code]: {delta.arguments}", flush=True)
            elif delta_type == "mcp_server_tool_call":
                print(
                    f"\n[Calling MCP Tool]: {delta.server_name}.{delta.name}",
                    flush=True,
                )

    elif event_type == "step.stop":
        print("\n<<< [Step Completed]", flush=True)

    elif event_type == "error":
        print(f"\n!!! [Execution Error]: {event.message}", flush=True)

    elif event_type == "interaction.completed":
        print("\n\n=== Interaction Execution Successfully Completed ===", flush=True)
