import requests
import json
import time
import urllib3
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET_BASE = "https://chatgpt.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/json,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

DEEP_ENDPOINTS = [
    "/deep-research",
    "/features/deep-research",
    "/backend-api/f/conversation",
    "/backend-api/sentinel/sdk.js",
    "/public-api/f/conversation",
    "/search",
    "/grok", # Check if Grok is mounted here on ChatGPT infrastructure (unlikely but possible given shared codebase artifacts)
    "/deep",
    "/research",
    "/admin",
    "/api/auth/session",
    "/codex/settings/environment/default",
    "/codex/settings/environment/production",
    "/codex/settings",
    "/canvas/codex",
    "/projects"
]

def log_result(endpoint, status, length, content_type, redirect_url=None):
    print(f"[{status}] {endpoint} (Len: {length}) [{content_type}]")
    if redirect_url:
        print(f"    -> Redirects to: {redirect_url}")

def probe_endpoint(endpoint):
    url = f"{TARGET_BASE}{endpoint}"
    try:
        # First HEAD request
        response = requests.head(url, headers=HEADERS, verify=False, allow_redirects=False, timeout=10)
        
        # If interesting, do GET
        if response.status_code in [200, 302, 401, 403, 404]: # Even 404 might be interesting if custom
            response = requests.get(url, headers=HEADERS, verify=False, allow_redirects=False, timeout=10)
            
            content_type = response.headers.get("Content-Type", "unknown")
            redirect_url = response.headers.get("Location")
            
            log_result(endpoint, response.status_code, len(response.text), content_type, redirect_url)
            
            # Analyze Content for Keywords
            content_lower = response.text.lower()
            keywords = ["deep research", "sahara", "waitlist", "upsell", "internal", "admin", "employee"]
            found_keywords = [k for k in keywords if k in content_lower]
            
            if found_keywords:
                print(f"    [!] INTERESTING CONTENT FOUND: {found_keywords}")
                
            # Save if it's a 200 OK non-HTML (likely API) or contains keywords
            if response.status_code == 200 and ("application/json" in content_type or found_keywords):
                filename = f"deep_sea_artifact_{endpoint.replace('/', '_')}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"URL: {url}\n")
                    f.write(f"Status: {response.status_code}\n")
                    f.write(f"Headers: {response.headers}\n")
                    f.write("\n--- BODY ---\n")
                    f.write(response.text)
                print(f"    [+] Saved artifact to {filename}")

    except Exception as e:
        print(f"[ERROR] Failed to probe {endpoint}: {str(e)}")

def main():
    print(f"[*] Starting Deep Sea Probe against {TARGET_BASE}")
    print(f"[*] Time: {datetime.now()}")
    
    for ep in DEEP_ENDPOINTS:
        probe_endpoint(ep)
        time.sleep(1) # Polite delay

if __name__ == "__main__":
    main()
