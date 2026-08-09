import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    keys = {}
    keys["DIGIKEY_CLIENT_ID"] = os.getenv("DIGIKEY_CLIENT_ID")
    keys["DIGIKEY_CLIENT_SECRET"] = os.getenv("DIGIKEY_CLIENT_SECRET")
    keys["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
        
    return keys