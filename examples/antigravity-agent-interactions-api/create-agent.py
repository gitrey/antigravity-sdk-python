from google import genai

client = genai.Client()

agent = client.agents.create(
    id="swe",
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
                license compatibity, and best practices.
                """,
            },
            {
                "type": "repository",
                "source": "https://github.com/gitrey/discount-manager",
                "target": "/workspace/repo",
            },
        ],
    },
)

print(f"Created agent: {agent.id}")
