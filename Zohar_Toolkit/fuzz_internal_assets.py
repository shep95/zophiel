import requests
import concurrent.futures
import os
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Targets that had /i/internal-static-assets
TARGETS = [
    "https://grok.x.com",
    "https://analytics.x.com",
    "https://studio.twitter.com",
    "https://video.twitter.com",
    "https://twitter.com",
    "https://x.com",
    "https://0.twitter.com",
    "https://devcommunity.x.com" # Added just in case
]

BASE_PATH = "/i/internal-static-assets/"

WORDLIST = [
    "config.json",
    "manifest.json",
    "settings.json",
    "env.json",
    "secrets.json",
    "constants.js",
    "app.js",
    "main.js",
    "admin.js",
    "dashboard.js",
    "internal.js",
    "feature_flags.json",
    "experiments.json",
    "build-manifest.json",
    "asset-manifest.json",
    "routes.json",
    "api.js",
    "endpoints.json",
    "developer.json",
    "keys.json"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fuzz(target):
    found = []
    print(f"[*] Fuzzing {target}{BASE_PATH}...")
    
    for word in WORDLIST:
        url = f"{target}{BASE_PATH}{word}"
        try:
            resp = requests.get(url, headers=HEADERS, verify=False, timeout=5)
            if resp.status_code == 200:
                # Filter out soft 404s (usually HTML)
                ct = resp.headers.get("Content-Type", "").lower()
                if "application/json" in ct or "javascript" in ct or "text/plain" in ct:
                    print(f"[!] FOUND: {url} ({len(resp.content)} bytes)")
                    found.append(url)
                elif "<html" not in resp.text.lower():
                     print(f"[?] POTENTIAL (Non-HTML): {url} ({len(resp.content)} bytes)")
                     found.append(url)
        except:
            pass
            
    return found

def run():
    all_findings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fuzz, t): t for t in TARGETS}
        for future in concurrent.futures.as_completed(future_to_url):
            res = future.result()
            all_findings.extend(res)
            
    if not all_findings:
        print("[-] No interesting static assets found.")
    else:
        print(f"[+] Total Assets Found: {len(all_findings)}")

if __name__ == "__main__":
    run()
