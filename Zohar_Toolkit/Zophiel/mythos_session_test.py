import requests
import json
import os
import time
import urllib3

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.mythoshub.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Referer': 'https://www.mythoshub.com/codex',
    'Origin': 'https://www.mythoshub.com'
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'MYTHOS_DB')

def try_session_access():
    print("[*] Attempting Session-Based Access to /api/codex...")
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # 1. Visit Homepage to get cookies/CSRF tokens
    print("    Visiting Homepage...")
    try:
        resp = session.get(BASE_URL, verify=False, timeout=10)
        print(f"    Homepage Status: {resp.status_code}")
        print(f"    Cookies: {session.cookies.get_dict()}")
        
        # 2. Visit Codex Page (Frontend)
        resp = session.get(f"{BASE_URL}/codex", verify=False)
        
        # 3. Try API Endpoint with cookies
        api_url = f"{BASE_URL}/api/codex"
        print(f"    Hitting API: {api_url}")
        resp = session.get(api_url, verify=False)
        
        if resp.status_code == 200:
            print("[!] SUCCESS! Access Granted.")
            data = resp.json()
            with open(os.path.join(OUTPUT_DIR, 'api_codex_dump.json'), 'w') as f:
                json.dump(data, f, indent=2)
            print(f"[+] Dumped {len(str(data))} bytes to api_codex_dump.json")
            return True
        elif resp.status_code == 401:
            print("[-] 401 Unauthorized. Login required.")
        else:
            print(f"[-] Failed with {resp.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
        
    return False

if __name__ == "__main__":
    try_session_access()
