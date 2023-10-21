import json
import openai 

def load_api_key(secrets_file="secrets.json"):
    with open(secrets_file) as f:
        secrets = json.load(f)
    return secrets["OPENAI_API_KEY"]

api_key = load_api_key()

content = input("User: ")

openai.api_key = api_key

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": content}
	]
)
chat_response = completion.choices[0].message.content
print(f'ChatGPT: {chat_response}')