import requests
import re
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Configuration
OUTPUT_DIR = r"C:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\OpenAI\Leaked_Assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GITHUB_BASE = "https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/"
LEAKED_FILES = [
    "gpt-5_new_params_and_tools.ipynb",
    "gpt-5_prompting_guide.ipynb",
    "gpt-5-1_prompting_guide.ipynb",
    "gpt-5-2_prompting_guide.ipynb",
    "gpt-5_frontend.ipynb",
    "gpt-5_troubleshooting_guide.ipynb",
    "gpt-5-mini_prompting_guide.ipynb",
    "gpt-5-nano_prompting_guide.ipynb",
    "codex_prompting_guide.ipynb",
    "apply_patch.py"
]

AGENTS_SDK_BASE = "https://raw.githubusercontent.com/openai/openai-agents-python/main/"
AGENTS_FILES = [
    "examples/tools/web_search.py",
    "src/agents/tool/web_search.py",
    "docs/tools.md"
]

COOKBOOK_URL = "https://cookbook.openai.com/"

def download_file(url, filename):
    try:
        print(f"[*] Attempting to download: {url}")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            file_path = os.path.join(OUTPUT_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"[+] SUCCESS: Saved {filename}")
            return True
        else:
            print(f"[-] FAILED: {url} (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"[!] ERROR: {e}")
        return False

def scan_cookbook_for_hidden_links():
    print("\n[*] Scanning cookbook.openai.com for hidden GitHub links...")
    try:
        response = requests.get(COOKBOOK_URL, timeout=10)
        if response.status_code != 200:
            print("[-] Failed to fetch cookbook homepage.")
            return

        # Regex for github links
        github_links = set(re.findall(r'https://github\.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+', response.text))
        
        print(f"[+] Found {len(github_links)} GitHub repositories:")
        for link in github_links:
            print(f"  - {link}")
            
        # Regex for specific codenames in JS
        matches = re.findall(r'(gpt-5|sora-2|codex_mcp)', response.text, re.IGNORECASE)
        if matches:
            print(f"[+] Found codename mentions in homepage source: {set(matches)}")

    except Exception as e:
        print(f"[!] Error scanning cookbook: {e}")

def main():
    print("=== DEEP DIVE PHASE 5: CODE HUNT & GITHUB RECON ===")
    
    # 1. Try to download the GPT-5 notebooks from GitHub (if they still exist)
    print("\n[1] Attempting to retrieve Leaked GPT-5 Notebooks...")
    found_any = False
    for file in LEAKED_FILES:
        if download_file(GITHUB_BASE + file, file):
            found_any = True
            
    # 2. Try to download Agents SDK files
    print("\n[2] Attempting to retrieve Agents SDK & WebSearchTool...")
    for file in AGENTS_FILES:
        filename = file.replace("/", "_")
        if download_file(AGENTS_SDK_BASE + file, filename):
            found_any = True

    # 3. Scan Cookbook for other traces
    scan_cookbook_for_hidden_links()

    if found_any:
        print(f"\n[SUCCESS] Leaked assets saved to: {OUTPUT_DIR}")
    else:
        print("\n[WARNING] No assets could be directly downloaded. They may have been deleted or moved.")

if __name__ == "__main__":
    main()
