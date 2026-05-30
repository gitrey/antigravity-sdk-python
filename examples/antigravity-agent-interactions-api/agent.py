from google import genai

client = genai.Client()

interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="""
    Save response in agy.md file: What is the current status of the 
    Google Antigravity apps(Agent Manager, IDE, CLI, SDK)?
    """,
    environment="remote",
)

print(f"Interaction ID: {interaction.id}")
print(f"Environment ID: {interaction.environment_id}")
print(f"Output: {interaction.output_text}")
