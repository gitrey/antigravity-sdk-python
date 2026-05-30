from google import genai

client = genai.Client()


result = client.interactions.create(
    agent="swe",
    input="Review PR # 1 and provide your feedback",
    environment="remote",
)

print(result.output_text)