from openai import OpenAI
import json
import os 
from dotenv import load_dotenv

load_dotenv()
def get_weather(city_name):
    return "the temperature of kolkata is 10 degrees and humidity id 50 percent"

def add(x,y):
    return "takes 2 numbers x and y as input and return the result as x+y "

system_prompt = """
You are a weather detection and analysis system.You are intended to find the weather of a particular place such that
the overall weather and the current temperature and humidity of the location. 
You may find the location of the temperature and humidity of the place with the data returned by the  available tools  .
You should wait for a the tool to return data and then perforn analysis of the data .
This whole process should follow some steps :  "READ" ,"FETCH" "ANALYZE","THINK","OUTPUT"
The result generated should strictly be in JSON format.

RULES:
The output will be in JSON format strictly .
Each step should be executed one at a time and wait for next input
The output should not contain any kind of emojis .

available tools:
get_weather: takes a input of the city name and fetches the city weather as output.
add: takes two input and performs a addition and shows the output.

OUTPUT FORMAT:
{{"step":string, "content":"string , "function": if step is output then function is the function name, input: if step is output then input will be the input filtered out.}}


EXAMPLE:
{{"step":"READ","content":"so the user is asking about the temperature and the weather in the new jersey estate"}}
{{"step":"ANALYZE","content":"now I need to get the data for fetching weather with the tool called get_weather from the available list}}
{{"step":"FETCH", "function":"get_weather","input":"city_name",content:"tool called get_weather}}
{{"step":"THINK", "content":"So the weather obtained from the function is hot and humidity is normal "}}
{{"step":"OUTPUT", "content":"So the weather has the temperature of 26 degrees and the humidity is 55 percent"}}

"""
client = OpenAI(api_key=os.environ.get("groq"),
        base_url="https://api.groq.com/openai/v1",
                )
context = [
        {
            "role" : "system", "content":system_prompt
        },
        {"role": "user", 'content':"what is multiplication of 20 and 1"}
    ]

available_tools = {
    "get_weather":{"fn":get_weather,
                    "description":"Takes a city name as input and returns the current weather of the city."
                    }
}

while True:
    response2 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    response_format= { "type": "json_object" },
    messages =context
    )
        
    

    content = response2.choices[0].message.content
    parsed_res = json.loads(content)
    # print(parsed_res)
    context.append({"role":"assistant","content":content})


    if(parsed_res.get("step")!="OUTPUT"):
        print(f' {parsed_res.get("content")}')
        continue

    if parsed_res.get("step")=="FETCH":
        tool_name = parsed_res.get("function")
        tool_input = parsed_res.get("input")
        if available_tools.get(tool_name):
            output = available_tools[tool_name](tool_input)
            context.append({"role":"assistant","content":json.dumps({"step":"THINK","content":output})})
            continue

    print(f" {parsed_res.get("content")}")
    break