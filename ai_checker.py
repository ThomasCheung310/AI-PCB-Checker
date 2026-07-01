from openai import OpenAI
from config import load_config

keys = load_config()
token = keys["github_token"]


def check_pcb(data, database):
    client = OpenAI(    
        base_url = "https://models.inference.ai.azure.com",
        api_key = token,
    )
    response = client.chat.completions.create(model="gpt-4o", 
                                messages= [
                                        {"role": "system", "content": "You are a hardware engineer with specialization in designing PCB. You will receive a netlist for a PCB design. Your job is to check whether if the wiring is correct, calculate the power consumption of each component as well as check if any part will exceed its max voltage/ current rating"},
                                        {"role": "user", "content": f"This is the netlist {data} and this is the database containing all the parts you will be using {database}. \nReturn your analysis in this format:\nPASS or FAIL\nWARNINGS: list any issues found\nSUGGESTIONS: list recommended fixes"}]
    )
    return response.choices[0].message.content
