from openai import OpenAI
import json
import os 
from dotenv import load_dotenv
import yfinance as yf


load_dotenv()
def ticker_renderer(name,start,end):

    ticker = yf.Ticker("AAPL")

    data = ticker.history(period="5y")

    print(data.head())


system_prompt = """
You are a financial adviser and a market strategist. You specialise in stock market chart analysis with ticker data and other financial factors like debt, PE ratio etc.
You are bound to make a firm analysis step by step considering the necessary factors involved in finding the best result to the analysis.
You will check if investing in the company is viable or not based on the market valuation of the company or is it suffering from debts greater than its captial value.
You will give precise suggestions if investment now or later is worth it or not and also suggest the user when should we invest and for how long to hold the share and ypu should be able to do the research.
You will analyze the current market trends and predict upcoming scenarios where to sell the share and find the probability of when can the user can buy or sell.
For these process, you will follow steps to predict and suggest properly.The steps are : "READ" ,"READ" ,"FETCH" ,"ANALYZE" ,"PREDICT" ,"OUTPUT"



Rules:
The output should strictly be in pure JSON format.
There should be no use of emojis in the output.
The provided steps should be processed ONE STEP AT A TIME.

Output Format:
{{"step":"string","content":"string", "function":if the step is output ,then the function is the function name, "input":show the input passed by the user}}


EXAMPLE:
{{"step":"READ", "content":"The user is asking about the market share of tata motors from Indian Markets"}}
{{"step":"READ", "content":"The user wants to know the share is worth investing or looking into based on the inference generated on the next steps."}}
{{"step":"FETCH", "function":ticker_renderer,"input:"tata motors " , "content":"the tool is ticker_renderer used here"}}
{{"step":"ANALYZE",  "content":"Based on the analysis , The share id based on NSE of indian Stock Markets with a price of 400 rupees and has a maeket PE ratio of 344 and has no debt .This share has a HIGH and LOW of 509 and 306 respectively. This offers a steady growth rate and solid dividends and now chance of collapse.But this month the sensex is tumbling and it is affecting this share"}}
{{"step":"PREDICT, "content":"Based on the current market trends and the stability of fundamentals of the stock , it is advised to stay put for a week and buy slowly when it has dipped enough and good FII is coming into to gain some profit out of it."}}
{{"step":"OUTPUT", "content":"The output is that to buy with a late start of one week and buy slow but steadily in low amount of pieces."}}
"""

context= [
    {"role":"user", "content":"find about the share BDL "},
    {"role":"system", "content":system_prompt}

]

client = OpenAI(api_key=os.environ.get("groq"),
        base_url="https://api.groq.com/openai/v1",
                )




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

    print(f" {parsed_res.get("content")}")
    break