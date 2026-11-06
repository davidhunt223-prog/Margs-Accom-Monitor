import os
import sys
import requests
from curl_cffi import requests as cffi_requests

# Search Criteria
REGION = "margaret-river-western-australia"
CHECKIN = "2026-12-26"
CHECKOUT = "2027-01-03"
ADULTS = 4
MIN_BEDROOMS = 2
MAX_BUDGET_AUD = 5000
PETS_ALLOWED = True

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_alert(message: str):
    if not DISCORD_WEBHOOK_URL:
        print(f"[DRY-RUN ALERT] {message}")
        return
    payload = {
        "content": (
            "🚨 **Margaret River Pet-Friendly Accom Alert** 🚨\n"
            f"{message}\n"
            f"**Dates:** {CHECKIN} to {CHECKOUT} (Flex)\n"
            f"**Budget cap:** ${MAX_BUDGET_AUD} total\n"
            f"**Specs:** {ADULTS} Adults, {MIN_BEDROOMS}+ Bed, Pets OK"
        )
    }
    resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    print(f"Notification status: {resp.status_code}")

def check_stays():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept-Language": "en-AU,en;q=0.9",
    }
    url = "https://www.hometogo.com.au/f/margaret-river/pet-friendly/"
    params = {
        "adults": ADULTS,
        "rooms": MIN_BEDROOMS,
        "pets": 1,
        "max_price": MAX_BUDGET_AUD,
    }

    try:
        session = cffi_requests.Session(impersonate="chrome120")
        response = session.get(url, params=params, headers=headers, timeout=20)
        if response.status_code == 200:
            print("Successfully queried accommodation index.")
        else:
            print(f"Warning: Endpoint returned HTTP {response.status_code}")
    except Exception as err:
        print(f"Encountered error during search: {err}", file=sys.stderr)

if __name__ == "__main__":
    check_stays()
