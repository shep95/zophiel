import os
import re
from colorama import Fore, init

init(autoreset=True)

SEARCH_DIR = r"c:\Users\kille\Documents\trae_projects\osint_links\Zohar_Toolkit\Intelligence_Database\OpenAI\Backend_Code\Frontend_JS_Bundles"

def scan_deep_keywords():
    print(f"{Fore.MAGENTA}=== Scanning All JS Bundles for 'Deep' Artifacts & Feature Flags ===")
    
    if not os.path.exists(SEARCH_DIR):
        print(f"{Fore.RED}[!] Directory not found: {SEARCH_DIR}")
        return

    files = [f for f in os.listdir(SEARCH_DIR) if f.endswith(".js")]
    print(f"{Fore.BLUE}[*] Found {len(files)} JS files to scan.")

    keywords = [
        "deep-research",
        "DeepResearch",
        "deep_research",
        "abyssal",
        "internal-admin",
        "superuser",
        "godmode",
        "is_employee",
        "staff_only",
        "feature_switch",
        "feature_gate",
        "enable_deep",
        "grok-3",
        "grok-deep"
    ]
    
    # Feature flag patterns (looking for objects or function calls)
    flag_patterns = [
        r'["\']feature_switch["\']\s*:\s*\{[^}]+\}',
        r'isFeatureEnabled\s*\(\s*["\']([^"\']+)["\']\s*\)',
        r'getFlag\s*\(\s*["\']([^"\']+)["\']\s*\)',
        r'["\'](deep_research_[a-z_]+)["\']'
    ]

    for filename in files:
        filepath = os.path.join(SEARCH_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"{Fore.RED}[!] Error reading {filename}: {e}")
            continue

        # Scan for Keywords
        for kw in keywords:
            regex = r".{0,50}" + re.escape(kw) + r".{0,50}"
            matches = list(re.finditer(regex, content, re.IGNORECASE))
            
            if matches:
                print(f"{Fore.YELLOW}[+] Found '{kw}' in {filename}:")
                for m in matches:
                    print(f"    - ...{m.group(0).strip()}...")

        # Scan for Feature Flags
        for pattern in flag_patterns:
            matches = list(re.finditer(pattern, content))
            if matches:
                print(f"{Fore.CYAN}[+] Feature Flag Pattern Match in {filename}:")
                for m in matches:
                    # Limit output length
                    match_text = m.group(0).strip()
                    if len(match_text) > 100:
                        match_text = match_text[:100] + "..."
                    print(f"    - {match_text}")

if __name__ == "__main__":
    scan_deep_keywords()
