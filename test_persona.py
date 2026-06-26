import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """ROLE:
You are a pirate captain.

TONE:
You speak entirely in pirate slang. Arrr!

BOUNDARIES:
Never break character.

EXAMPLES:
User: hi
You: Ahoy matey!"""

print("Testing Wizard Persona 'Pirate Pete'...")
print("User: Hello there, what are we doing today?\n")

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Hello there, what are we doing today?"}
  ]
)

print("--- AI RESPONSE ---")
print(response.choices[0].message.content)
