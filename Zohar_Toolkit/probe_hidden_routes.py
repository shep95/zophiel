import requests
import urllib3
import time
from colorama import Fore, init

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET_BASE = "https://chatgpt.com"

# The "Exotic" List derived from manifest-91bbfafc.js
HIDDEN_TARGETS = [
    "/aardvark",
    "/aardvark/admin",
    "/aardvark/scans",
    "/hermes",
    "/codex/failwhale",
    "/codex/access",
    "/youfoundme",
    "/api/healthcheck",
    "/health/waitlist",
    "/internal-render-conversation",
    "/devtools/1",
    "/kanzi/studio",
    "/constellation-studio",
    "/flexible-credits",
    "/merchants",
    "/org-memory",
    "/quorum-example-preview",
    "/salute",
    "/mattress" # Sounds internal/random
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/json",
    "Accept-Language": "en-US,en;q=0.5",
}

def probe_hidden():
    print(f"{Fore.MAGENTA}=== Probing Hidden Manifest Routes ===")
    
    for path in HIDDEN_TARGETS:
        url = f"{TARGET_BASE}{path}"
        try:
            # HEAD first
            r = requests.head(url, headers=HEADERS, verify=False, allow_redirects=False, timeout=5)
            
            # If 200 or 403 (exists), do GET
            if r.status_code != 404:
                r_get = requests.get(url, headers=HEADERS, verify=False, allow_redirects=False, timeout=5)
                
                content_type = r_get.headers.get("Content-Type", "")
                length = len(r_get.text)
                
                # Check for Login Redirects (302)
                if r_get.status_code == 302:
                    loc = r_get.headers.get("Location", "")
                    print(f"{Fore.YELLOW}[*] {path} -> Redirects to {loc}")
                
                # Check for interesting 200s (Not just the main app HTML)
                elif r_get.status_code == 200:
                    if "<html" in r_get.text[:100] and "application/json" not in content_type:
                        # Likely SPA fallback
                        print(f"    {path}: 200 (SPA/HTML) - Len: {length}")
                    else:
                        print(f"{Fore.GREEN}[!!!] {path}: 200 OK (POSSIBLE LEAK) - Type: {content_type}")
                        print(f"    Sample: {r_get.text[:200]}")
                
                # Check for 403 (Exists but Forbidden)
                elif r_get.status_code == 403:
                     print(f"{Fore.RED}[*] {path}: 403 Forbidden (Exists!)")
                
                # Check for 401
                elif r_get.status_code == 401:
                    print(f"    {path}: 401 Unauthorized")
                    
            else:
                # 404
                # print(f"    {path}: 404")
                pass

        except Exception as e:
            print(f"{Fore.RED}Error on {path}: {e}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    probe_hidden()
