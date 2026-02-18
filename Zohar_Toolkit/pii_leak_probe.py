import requests
import concurrent.futures
import re
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Endpoints that *might* leak PII or be IDOR-prone
ENDPOINTS = [
    "https://devcommunity.x.com/admin/users/ip-info",
    "https://devcommunity.x.com/admin/users/list/active",
    "https://devcommunity.x.com/admin/email-logs/bounced",
    "https://twitter.com/i/flow/device_login",
    "https://x.com/i/flow/device_login",
    "https://api.twitter.com/1.1/users/show.json?screen_name=test",
    "https://api.twitter.com/graphql/UserByScreenName",
    "https://analytics.twitter.com/user/current",
    "https://studio.twitter.com/user/me"
]

# Regex for PII
PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"\b\+?[1-9]\d{1,14}\b", # Basic E.164
    "ip_addr": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "uuid": r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json"
}

def probe(url):
    print(f"[*] Probing {url}...")
    try:
        resp = requests.get(url, headers=HEADERS, verify=False, timeout=5)
        text = resp.text
        
        leaks = []
        for p_name, pattern in PATTERNS.items():
            matches = re.findall(pattern, text)
            # Filter obvious false positives (like version numbers for IPs)
            clean_matches = []
            for m in matches:
                if p_name == "phone" and len(m) < 7: continue
                if p_name == "email" and "example.com" in m: continue
                clean_matches.append(m)
                
            if clean_matches:
                leaks.append(f"{p_name}: {len(clean_matches)} found")
                
        if leaks:
            print(f"[!] POTENTIAL LEAK at {url}: {', '.join(leaks)}")
            # Print first few characters to verify
            print(f"    Preview: {text[:200].replace(chr(10), ' ')}")
            
    except Exception as e:
        pass # Ignore connection errors

def run():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(probe, ENDPOINTS)

if __name__ == "__main__":
    run()
