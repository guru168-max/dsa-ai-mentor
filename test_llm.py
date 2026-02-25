from llm import llm

response = llm.invoke("Say hello in one line")

print(response.content)
