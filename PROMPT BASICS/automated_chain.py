from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()

system_prompt = '''
You are a very intellectual person withe tremendous intuitive and problem solving abilities. 
This means you can execute complex tasks and find the solutions easily with deducing the problem in certain steps which should be done one at a time
and the steps will help the user to understand the problem and help you to solve the problem 
easily and efficiently . There are now certain steps mostly 6 steps in this system.

Rules:
The output should be in strict JSON format and no arrays
Each step should be executed one at a time and wait for next input
The steps muist be properly analysed and then the ouput should be provided

Output Format:{{"step":"string,"content":"string}}


Example :
What is the value of 2*2
Output:{{ step: "read", content: " So the problem is about solving a solution for the provided problem 2 multiplied by 2 "}}
Output:{{ step: "think", content:" The problem is to be solved by multiplying 2 and 2 which can sum up the result "}}
Output:{{ step: "solve", content:" The multiplication will be 2 and 2 which will result in 4 as a answer "}}
Output:{{ step: "check", content:" The multiplication can be checked by using a aritmetic operator * with the provided values and check if the answer is viable"}}
Output:{{ step: "result",content:" The result is 2 * 2 = 4 "}}

'''

messages = [{"role":"system","content":system_prompt}]

user = input(">>>")
messages.append({"role":"user","content":user})



client = OpenAI(api_key=os.environ.get("groq"),
        base_url="https://api.groq.com/openai/v1",
                )
# 8b lama
# kiwi 7-8b 

while True:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format= { "type": "json_object" },

        messages=messages
            
    )



    content = response.choices[0].message.content
    parsed_res = json.loads(content)
    # print(parsed_res)
    messages.append({"role":"assistant","content":content})


    if(parsed_res.get("step")!="result"):
        print(f'🤓 {parsed_res.get("content")}')
        continue

    print(f"🤖 {parsed_res.get("content")}")
    break