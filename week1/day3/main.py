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

prompt1="Hi"
prompt2="Explain array in dsa "
prompt3="Write 1000 essay on love marriage "

prompts =[prompt1,prompt2,prompt3]

for prompt in prompts:
    message={
        "role":"user",
        "content":prompt
    }
    messages=[message]

    Response=client.chat.completions.create(model=model,messages=messages,max_tokens=2000)
    usage = Response.usage
    print(f"Promp:{prompt}--> your tokens:{usage.prompt_tokens} completion token:{usage.completion_tokens} total token:{usage.total_tokens} Finish Reason :{Response.choices[0].finish_reason}")
