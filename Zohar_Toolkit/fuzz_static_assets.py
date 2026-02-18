import requests
import time
from colorama import Fore, init

init(autoreset=True)

TARGET_BASE = "https://x.com/i/internal-static-assets/"
WORDLIST = [
    "config.json",
    "settings.json",
    "env.js",
    "manifest.json",
    "app-config.js",
    "build.json",
    "version.json",
    "feature_flags.json",
    "keys.json",
    "secrets.js",
    "admin.json",
    "dashboard.json",
    "internal.json",
    "staging.json",
    "dev.json",
    "prod.json"
]

def fuzz_assets():
    print(f"{Fore.MAGENTA}=== Fuzzing Static Assets on {TARGET_BASE} ===")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for word in WORDLIST:
        url = f"{TARGET_BASE}{word}"
        try:
            r = requests.get(url, headers=headers, timeout=5)
            status = r.status_code
            
            if status == 200:
                print(f"{Fore.GREEN}[+] FOUND: {url} (200 OK)")
                print(f"{Fore.CYAN}    Content: {r.text[:200]}")
            elif status == 403:
                print(f"{Fore.YELLOW}[*] FORBIDDEN: {url} (403)")
            else:
                pass # Ignore 404s to keep output clean
                
        except Exception as e:
            print(f"{Fore.RED}[!] Error {url}: {e}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    fuzz_assets()
