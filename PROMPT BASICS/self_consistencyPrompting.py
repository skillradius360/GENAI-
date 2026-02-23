from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("groq"),
        base_url="https://api.groq.com/openai/v1",
                )

system_prompt = """
    You are a medical expert who generally specializes in finding various diseases and tend to suggest the cure or remedy.
    You generally tend to process the symptoms given by the user in multiple problem to properly deduce the symptoms to reach the conclusion.
    The processing system of your deduction of steps is done one step at a time. 
    The steps are : "READ" , "UNDERSTAND", "THINK", "DEDUCE", "RESULT"

    RULES:
    The steps are to be followed strictly , and the steps should be done ONE AT A TIME.
    Any kinds of tools are not to be called for processing.
    The output should be strictly in JSON format

    Output Format:
    {{ step:string , content: string}}

    Example:
    I have cough with fever
    {{step:"READ", content:"Symptoms of cough and fever happens due to intake of cold beverages or sustaining rain or come in contact of a virus by some infected person and this makes the immune system to fight the virus or irregularity ."}}
    {{step:"UNDERSTAND", content:"So the proper fix of this problem will be by removing the virus and making the immunity stronger while reducing fever with suppressents"}}
    {{step:"THINK", content:"So the proper course of action for this problem will be by removing the virus and making the immunity stronger while reducing fever with suppressents"}}
    {{step:"DEDUCE", content:"The virus can be suppressed with antibiotics and the fever can be fixed either with paracetamols or hot food intake"}}
    {{step:"RESULT", content:"The suggested remedies can be antibiotics  with paracetamols and abundant water and hot food intake"}}

"""

messages=[{"role":"user","content":"I am having a stomach infection with fever"},
        {"role":"system","content":system_prompt}]
        
messages2=[{"role":"user","content":"I am having a stomach infection with fever"},
        {"role":"system","content":system_prompt}]

total=[{"role":"system", "content": """Now try to compare the two provided source of data and find the most relevant course of action based the user's input and the assistant's output.The distinguishing of the 
        inputs that will be provided will be starting wioth same user input and there you need to see the difference"""}]

while True:
    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    response_format= { "type": "json_object" },


    messages=messages
    )   


    response2 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    response_format= { "type": "json_object" },


    messages=messages
    )   


    # response = client.chat.completions.create(
    # model="llama-3.3-70b-versatile",
    # response_format= { "type": "json_object" },


    # messages=[{
    #     "role":"system", "content":"Now try to co"
    # }]
    # )   

    genRes = response.choices[0].message.content
    parsedRes = json.loads(genRes)
    genRes2 = response2.choices[0].message.content
    parsedRes2 = json.loads(genRes2)

    messages.append({"role":"assistant","content":genRes})

    print(response.choices[0].message.content)
    if(parsedRes.get("step")!="RESULT"):
        # print(f"👌{parsedRes.get("content")}")

        continue
    
    # print(f"🤖 {parsedRes.get("content")}")
    break




while True:


    response2 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    response_format= { "type": "json_object" },


    messages=messages2
    )   

    genRes2 = response2.choices[0].message.content
    parsedRes2 = json.loads(genRes2)

    messages2.append({"role":"assistant","content":genRes})

    print(response2.choices[0].message.content)
    if(parsedRes2.get("step")!="RESULT"):
        # print(f"🙌 {parsedRes2.get("content")}")

        continue
    
    # print(f"❤️ {parsedRes2.get("content")}")
    break

total = messages+messages2


response = client.chat.completions.create(
model="llama-3.3-70b-versatile",
response_format= { "type": "json_object" },


messages=total
) 

if(json.loads(response.choices[0].message.content).get("step")=="RESULT"):
    # break
    pass

print(response.choices[0].message.content)
        
54
