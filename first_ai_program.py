import ollama
model_name='llama3.2:3b'
prompt="Explain how AI works in one line"
response=ollama.generate(model=model_name,
                         prompt=prompt)
print(response.response)
