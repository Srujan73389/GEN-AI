import ollama
messages=[
    {
        "role":'system',
        "content":"You are a strict university professor. Answer in three bullet points"
    },
    {
        "role":"user",
        "content":"What is AI?"
    }
]
model_name='llama3.2:3b'

response=ollama.chat(model=model_name,messages=messages)
print(response.message.content)