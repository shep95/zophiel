import requests
import re
from colorama import Fore, init

init(autoreset=True)

URL = "https://abs.twimg.com/responsive-web/client-web/main.1ab552da.js"
FILE_NAME = "main_bundle.js"

def scan_secrets():
    print(f"{Fore.CYAN}[*] Downloading JS Bundle...")
    try:
        r = requests.get(URL)
        content = r.text
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{Fore.GREEN}[+] Saved to {FILE_NAME}")
    except Exception as e:
        print(f"{Fore.RED}[!] Download Failed: {e}")
        return

    print(f"{Fore.YELLOW}[*] Scanning for Secrets...")
    
    patterns = {
        "Stripe Key": r"pk_live_[0-9a-zA-Z]{24,}",
        "Google API": r"AIza[0-9A-Za-z-_]{35}",
        "AWS Key": r"AKIA[0-9A-Z]{16}",
        "Private Token": r"(?i)private_key|secret_key|auth_token",
        "Grok Internal": r"grok-[a-z0-9-]+"
    }
    
    found = False
    for name, regex in patterns.items():
        matches = re.findall(regex, content)
        if matches:
            found = True
            unique = list(set(matches))
            print(f"{Fore.RED}[!] FOUND {name}: {len(unique)} unique matches")
            for m in unique[:5]: # Show first 5
                print(f"    - {m}")
    
    if not found:
        print("[-] No obvious secrets found.")

if __name__ == "__main__":
    scan_secrets()
