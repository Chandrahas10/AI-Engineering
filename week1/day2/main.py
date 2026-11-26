import os
from dotenv import load_dotenv
from groq import Groq 

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found")

client =Groq(api_key =my_api_key)

model = "openai/gpt-oss-20b"
role="user"
prompt="I love you"
messageSystem={
        "role":"system",
        "content":"You are my loving girlfriend"
    }

message={
    "role":role,
    "content":prompt
}


messages=[messageSystem,message]

Response=client.chat.completions.create(model=model,messages=messages,temperature=1.5)
# print(Response)
answer=Response.choices[0].message.content 
print(answer)