import os
from dotenv import load_dotenv
from groq import Groq 

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found")

client =Groq(api_key =my_api_key)

model = "openai/gpt-oss-20b"

def llm_ans(prompt):
    message=[{
        "role":"user",
        "content":prompt
    }]
    messages=message
    response=client.chat.completions.create(model=model,messages=messages)
    return response.choices[0].message.content

bad_prompt= """
#ROLE:
You are the support assistant at mobile/compuyter company 
#TASK:
You have to classify issue in the catefory
#CONSTRAINT:
You have to classify the issue in the one of three category billing , technical, return 
#OUTPUT FORMAT:
Your answer is in one word only. The one word from the category given in the constraint .
#Example:
for instance if a user complaint says he wants to refund then the category is return 
#fallback:
if the issue is unrelated with this three category mention in the constraint , then answer should be other.
This is laptop complaint :
my gf is broken relationship with me 
classify this 
"""

print(llm_ans( bad_prompt))