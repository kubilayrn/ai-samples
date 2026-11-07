from ollama import chat

MODEL = "qwen3:1.7b"

response = chat(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "Sen Türkçe cevap veren bir Python eğitmenisin."
        },
        {
            "role": "user",
            "content": "FastAPI nedir? İki cümleyle açıkla."
        }
    ],
)

print(response.message.content)
