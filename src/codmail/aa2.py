import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)

response = client.responses.create(
    model="openai/gpt-oss-120b",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
