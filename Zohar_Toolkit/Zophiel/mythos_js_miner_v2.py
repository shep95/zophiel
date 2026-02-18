import requests
from bs4 import BeautifulSoup
import os
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.mythoshub.com"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'MYTHOS_JS_DUMP')
os.makedirs(OUTPUT_DIR, exist_ok=True)
INDEX_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'MYTHOS_DB', 'index.html')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

def mine_local_index():
    print("[*] Parsing local index.html for JS chunks...")
    
    if not os.path.exists(INDEX_FILE):
        print("[-] index.html not found.")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    scripts = []
    for s in soup.find_all('script'):
        if s.get('src'):
            scripts.append(s['src'])
            
    print(f"[+] Found {len(scripts)} script tags.")
    
    found_intel = False
    
    for script_url in scripts:
        if script_url.startswith('/'):
            script_url = BASE_URL + script_url
        
        filename = script_url.split('/')[-1]
        print(f"    Downloading {filename}...", end=" ")
        
        try:
            # Try to fetch the JS file
            js_resp = requests.get(script_url, headers=HEADERS, verify=False, timeout=10)
            
            if js_resp.status_code == 200:
                content = js_resp.text
                
                # Save raw JS
                with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("Saved.", end=" ")

                # Check for keywords
                hits = []
                if "Harmonious Farmer" in content:
                    hits.append("BLOOD_TYPE")
                if "The Leader" in content and "Innovation" in content:
                    hits.append("NUMEROLOGY")
                if "Myers-Briggs" in content or "INTJ" in content:
                    hits.append("MBTI")
                    
                if hits:
                    print(f" MATCH! ({', '.join(hits)})")
                    found_intel = True
                else:
                    print("Clean.")
            else:
                print(f"Failed ({js_resp.status_code})")
                
        except Exception as e:
            print(f"Error: {e}")
            
    if not found_intel:
        print("[-] No static intelligence found in JS chunks.")
    else:
        print("[+] Intelligence potentially found in JS dump.")

if __name__ == "__main__":
    mine_local_index()
