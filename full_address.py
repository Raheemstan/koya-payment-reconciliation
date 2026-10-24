import os

import requests
from dotenv import load_dotenv

load_dotenv()

def get_full_address(latitude, longitude):
    url = "https://api.apilayer.net/positionstack/v1/reverse"

    params = {
        "access_key": os.getenv("ACCESS_KEY"),
        "query": f"{latitude},{longitude}"
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    result = response.json()

    addresses = result.get("data", [])
    return addresses[0] if addresses else None


address = get_full_address(6.4410, 3.5357)

if address:
    print("Full address:", address.get("label"))
    print("Address details:", address)
else:
    print("No address found.")
