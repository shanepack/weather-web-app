import json
import openai 

def load_api_key(secrets_file="secrets.json"):
    with open(secrets_file) as f:
        secrets = json.load(f)
    return secrets["OPENAI_API_KEY"]

api_key = load_api_key()

openai.api_key = api_key
while True:
	content = input("User: ")
	messages = [
		{"role": "system", "content": "You are a weather forecaster"}
		]
	messages.append({"role": "user", "content": content})
	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=messages
	)
	chat_response = completion.choices[0].message.content
	print(f'ChatGPT: {chat_response}')
	messages.append({"role": "assistant", "content": content})