import json
import os
import requests
from config import load_config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARTS_CACHE = os.path.join(BASE_DIR, "data", "parts_cache.json")
DIGIKEY_TOKEN_URL = "https://api.digikey.com/v1/oauth2/token"
DIGIKEY_URL = "https://api.digikey.com/products/v4/search/keyword"

def load_cache():
    os.makedirs(os.path.dirname(PARTS_CACHE), exist_ok=True)
    if not os.path.exists(PARTS_CACHE):
        with open(PARTS_CACHE, "w") as f:
            json.dump({}, f)
        return {}
    
    with open(PARTS_CACHE, "r") as f:
        return json.load(f)

def save_cache(cache):
    os.makedirs(os.path.dirname(PARTS_CACHE), exist_ok=True)
    with open(PARTS_CACHE, "w") as f:
        json.dump(cache, f, indent=2)

def get_token(client_id, client_secret):
    response = requests.post(
        DIGIKEY_TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
    )
    return response.json()["access_token"]

def extract_data(response):
    data = response.json()
    products = data.get("Products", [])

    if not products:
        return {"source": "digikey", "part_number": "unknown", "error": "not found"}
    
    product = products[0]
    result = {"source": "digikey", "part_number": product["ManufacturerProductNumber"]}
    for i in product["Parameters"]:
        result[i["ParameterText"]] = i["ValueText"]
    return result

def digikey(part_id):
    keys = load_config()
    client_id = keys["DIGIKEY_CLIENT_ID"]
    client_secret = keys["DIGIKEY_CLIENT_SECRET"]
    token = get_token(client_id, client_secret)
    
    headers = {"Authorization": f"Bearer {token}",
               "X-DIGIKEY-Client-Id": client_id,
               "Content-Type": "application/json"}

    response = requests.post(
        DIGIKEY_URL,
        json = {"Keywords": part_id, "RecordCount": 1},
        headers = headers
    )
    result = extract_data(response)
    return result

def get_components(part_ids):
    cache = load_cache()
    results = {}
    missing = []
    for i in part_ids:

        if i in cache:
            results[i] = cache[i]
    
        else:
            new_part = digikey(i)
            if new_part.get("error"):
                missing.append(i)
            else:
                cache[i] = new_part
                results[i] = new_part
            
    save_cache(cache)
    return results, missing