"""Self-contained test script to verify custom agent creation and environment visibility.

This script executes a full lifecycle test:
1. Deletes any pre-existing 'swe-test' agent definition.
2. Creates a new 'swe-test' agent with an inline-configured Markdown file.
3. Triggers an interaction testing if the agent can read its workspace file.
"""

from google import genai

# Initialize the standard Google GenAI Client
client = genai.Client()

# 1. Clean up existing test agent if it exists
try:
    client.agents.delete(id="swe-test")
    print("Deleted old swe-test")
except Exception as e:
    pass

# 2. Create agent with an inline source file loaded into its workspace
agent = client.agents.create(
    id="swe-test",
    base_agent="antigravity-preview-05-2026",
    system_instruction="You are a software engineer.",
    base_environment={
        "type": "remote",
        "sources": [
            {
                "type": "inline",
                "target": ".agents/AGENTS.md",
                "content": """
                Review code for security vulnerabilities,
                license compatibility, and best practices.
                """,
            }
        ],
    },
)
print("Created new swe-test agent.")

# 3. Test agent interaction & verify file visibility
try:
    result = client.interactions.create(
        agent="swe-test",
        input="Say Hello and tell me if you can see .agents/AGENTS.md",
        environment="remote",
    )
    print("\n--- Interaction Output ---")
    print(result.output_text)
except Exception as e:
    print("Interaction failed:", e)

