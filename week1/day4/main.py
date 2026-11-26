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
#structure it
from pydantic import BaseModel
class Ticket(BaseModel):
    name:str 
    email:str
    issue:str
    phone_no:int

schema=Ticket.model_json_schema()

Response_format={
    "type":"json_object"
}

system_prompt=f"""" 
Extract the personal information from the ticket strictly based on this schema and give a json output. 
{schema}
"""

messages_system={
    "role":"system",
    "content":system_prompt
}

text="Hello my name is chandrahas. I have an iphone which is not working at all.my address is shirwal. my email is chandrahaskori8@gmail.conm . My contact no is 89567829347. recently my relationship with my girlfriend is broken so she broke my iphone" 
prompt=f"""
This is a customer ticket. Please extract the personal information from this.
{text}
"""


message={
        "role":"user",
        "content":prompt
}
messages=[messages_system,message]

Response=client.chat.completions.create(
    model=model,
    messages=messages,
     response_format=Response_format)
answer=Response.choices[0].message.content 
print(answer)

# how to read this
import json 
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

#pass this 
print(ticket.name)
print(ticket.email)
print(ticket.issue)
print(ticket.phone_no)
