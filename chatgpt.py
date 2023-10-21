import json
import openai 

def load_api_key(secrets_file="secrets.json"):
    with open(secrets_file) as f:
        secrets = json.load(f)
    return secrets["OPENAI_API_KEY"]

api_key = load_api_key()

openai.api_key = api_key

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "it's going to be sunny and warm in Houston Texas tomorrow. can you provide me with some outdoor activity recommendations?"}
	]
)
print(completion.choices[0].message.content)