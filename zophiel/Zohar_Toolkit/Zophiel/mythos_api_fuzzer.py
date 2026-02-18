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
    'Content-Type': 'application/json'
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'MYTHOS_DB')
os.makedirs(OUTPUT_DIR, exist_ok=True)

POTENTIAL_ENDPOINTS = [
    "/api/codex",
    "/api/codex/list",
    "/api/profiles",
    "/api/profiles/list",
    "/api/directory",
    "/api/search",
    "/api/search?q=a",
    "/api/users",
    "/api/public/codex",
    "/api/public/profiles",
    "/api/db/codex",
    "/api/v1/codex",
    "/api/v1/profiles",
    "/api/people",
    "/api/celebrities",
    "/api/data/codex",
    "/_next/data/build-id/codex.json" # Next.js specific pattern (tricky without build ID)
]

def fuzz_endpoints():
    print("[*] Fuzzing MythosHub API for Codex Database...")
    
    found_data = False
    
    for endpoint in POTENTIAL_ENDPOINTS:
        url = f"{BASE_URL}{endpoint}"
        print(f"    Trying: {endpoint} ...", end=" ")
        try:
            resp = requests.get(url, headers=HEADERS, verify=False, timeout=5)
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    print(f"SUCCESS! ({len(str(data))} bytes)")
                    
                    # Save it
                    filename = endpoint.replace("/", "_").replace("?", "_").strip("_") + ".json"
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                    
                    found_data = True
                    print(f"    [+] Saved to {filename}")
                    
                    # If we found a list, maybe stop? No, keep going.
                except:
                    print(f"200 OK but not JSON.")
            else:
                print(f"Failed ({resp.status_code})")
                
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error: {e}")

    if not found_data:
        print("[-] No public API endpoints guessed successfully.")
    else:
        print("[+] Fuzzing complete. Check output directory.")

if __name__ == "__main__":
    fuzz_endpoints()
