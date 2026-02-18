import os
import re
from colorama import Fore, init

init(autoreset=True)

SEARCH_DIR = r"c:\Users\kille\Documents\trae_projects\osint_links\Zohar_Toolkit"

PATTERNS = {
    "Stripe Public": r"pk_live_[0-9a-zA-Z]{24}",
    "Stripe Secret": r"sk_live_[0-9a-zA-Z]{24}",
    "Grok Transaction": r"grok-transaction",
    "Money API": r"/i/money/",
    "Guest Token": r"guest_token"
}

def deep_scan():
    print(f"{Fore.MAGENTA}=== Deep Scan for Keys and Money Patterns ===")
    
    for root, dirs, files in os.walk(SEARCH_DIR):
        for file in files:
            if file.endswith(".py") or file.endswith(".js") or file.endswith(".json") or file.endswith(".txt"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        
                    for name, pattern in PATTERNS.items():
                        matches = list(re.finditer(pattern, content))
                        if matches:
                            print(f"{Fore.GREEN}[+] Found {name} in {file}:")
                            for m in matches[:5]:
                                context = content[max(0, m.start()-50):min(len(content), m.end()+50)]
                                print(f"    - ...{context.replace(chr(10), ' ')}...")
                except Exception as e:
                    pass

if __name__ == "__main__":
    deep_scan()
