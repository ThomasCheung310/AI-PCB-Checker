import os

def load_config
    NEXAR_CLIENT_ID = os.getenv("NEXAR_CLIENT_ID")
    NEXAR_CLIENT_SECRET = os.getenv("NEXAR_CLIENT_SECRET")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    keys["NEXAR_CLIENT_ID"] = NEXAR_CLIENT_ID
    keys["NEXAR_CLIENT_SECRET"] = NEXAR_CLIENT_SECRET
    keys["GITHUB_TOKEN"] = GITHUB_TOKEN
    
    return keys