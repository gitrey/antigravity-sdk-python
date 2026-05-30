from google import genai

client = genai.Client()

# 1. Clean up existing test agent if it exists
try:
    client.agents.delete(id="swe-test")
    print("Deleted old swe-test")
except Exception as e:
    pass

# 2. Create agent with only inline source
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
print("Created swe-test")

# 3. Test interaction
try:
    result = client.interactions.create(
        agent="swe-test",
        input="Say Hello and tell me if you can see .agents/AGENTS.md",
        environment="remote",
    )
    print("Interaction Output:")
    print(result.output_text)
except Exception as e:
    print("Interaction failed:", e)
