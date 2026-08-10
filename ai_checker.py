from openai import OpenAI
from config import load_config


keys = load_config()
token = keys["GROQ_API_KEY"]


def check_pcb(mcu, pcb, database):
    client = OpenAI(    
        base_url = "https://api.groq.com/openai/v1",   
        api_key = token,
    )

    compressed_pcb = '\n'.join(line.strip() for line in pcb.split('\n') 
                      if line.strip() and not line.startswith('#'))

    response = client.chat.completions.create(model="openai/gpt-oss-20b", 
                                messages= [
                                        {"role": "system", "content": "You are a PCB design engineer. Check the netlist for: 1) Missing essential circuits for the given MCU (programming circuit, reset, boot pins) 2) Power budget issues 3) Floating pins or missing grounds. Flag components without unknown parameters and state the limitations.  "},
                                        {"role": "user", "content": f"MCU: {mcu}\n\nNetlist:\n{compressed_pcb}\n\nComponent Database:\n{database}\n\nReturn your analysis in this format:\nOVERALL: PASS or FAIL\nWARNINGS: list any issues found\nSUGGESTIONS: list recommended fixes"}]
    )
    return response.choices[0].message.content
