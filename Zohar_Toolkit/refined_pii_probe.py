import requests
import re
import json
import time
import os
from colorama import Fore, Style, init

# Initialize colors
init(autoreset=True)

# Configuration
OUTPUT_FILE = "refined_pii_results.json"
TARGETS = [
    "https://grok.x.com/i/api/2/grok/add_response",
    "https://grok.x.com/i/api/graphql",
    "https://x.com/i/api/2/grok/add_response",
    "https://x.com/i/api/graphql",
    "https://api.x.com/1.1/account/settings.json", # Typical endpoint
    "https://api.x.com/2/users/me",
    "https://analytics.x.com/i/api/1/analytics"
]

# Headers mimicking a logged-in session (partially) or guest
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA", # Public Guest Token often found in JS
    "x-guest-token": "", # Would need to be fetched dynamically if we wanted full guest access
    "Content-Type": "application/json"
}

# Regex Patterns - Refined
PATTERNS = {
    "email": r'(?i)"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"', # Must be quoted (JSON value)
    "phone_strict": r'"\+?[1-9]\d{9,14}"', # Quoted phone number
    "api_key": r'(?i)"(api_key|access_token|secret)":\s*"[a-zA-Z0-9_\-]{20,}"',
    "uuid": r'"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"'
}

# Ignore list (False Positives)
IGNORE_STRINGS = [
    "abs.twimg.com",
    ".js",
    ".css",
    "version",
    "webpack",
    "react"
]

def fetch_guest_token():
    """Attempts to get a guest token for unauthenticated access."""
    try:
        print(f"{Fore.CYAN}[*] Attempting to fetch Guest Token...")
        # Often triggering the main page sets a cookie or returns a token
        r = requests.post("https://api.x.com/1.1/guest/activate.json", headers={"Authorization": HEADERS["Authorization"]})
        if r.status_code == 200:
            token = r.json().get("guest_token")
            print(f"{Fore.GREEN}[+] Guest Token Acquired: {token}")
            return token
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to get guest token: {e}")
    return None

def scan_endpoint(url, guest_token=None):
    headers = HEADERS.copy()
    if guest_token:
        headers["x-guest-token"] = guest_token
    
    print(f"{Fore.YELLOW}[*] Scanning {url}...")
    
    # Try GET
    try:
        r = requests.get(url, headers=headers, timeout=10)
        analyze_response(url, "GET", r)
    except Exception as e:
        print(f"{Fore.RED}[!] GET Error: {e}")

    # Try POST (often needed for GraphQL/API)
    try:
        # Empty payload or generic query
        payload = {"query": "{ viewer { id } }", "variables": {}}
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        analyze_response(url, "POST", r)
    except Exception as e:
        print(f"{Fore.RED}[!] POST Error: {e}")

def analyze_response(url, method, response):
    content = response.text
    
    # Skip large HTML blobs if possible, focus on JSON
    is_json = False
    try:
        json_content = response.json()
        content = json.dumps(json_content) # Convert back to string for regex but cleaner
        is_json = True
    except:
        pass

    results = []
    
    for name, pattern in PATTERNS.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            val = match.group(0)
            
            # Filter False Positives
            if any(ign in val for ign in IGNORE_STRINGS):
                continue
            
            # Additional logic: Phone numbers shouldn't look like version hashes
            if name == "phone_strict" and len(val.replace('"', '').replace('+', '')) > 15:
                continue

            print(f"{Fore.RED}[!] POTENTIAL LEAK ({name}): {val} in {url} ({method})")
            results.append({
                "type": name,
                "value": val,
                "url": url,
                "method": method
            })

    if results:
        save_results(results)

def save_results(new_results):
    existing = []
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r") as f:
                existing = json.load(f)
        except:
            pass
    
    existing.extend(new_results)
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(existing, f, indent=2)

def main():
    print(f"{Fore.MAGENTA}=== Refined PII Probe vs X Corp ===")
    
    guest_token = fetch_guest_token()
    
    for url in TARGETS:
        scan_endpoint(url, guest_token)
        time.sleep(1)

if __name__ == "__main__":
    main()
