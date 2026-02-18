import requests
from bs4 import BeautifulSoup
import os
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.mythoshub.com"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'MYTHOS_JS_DUMP')
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

def mine_js():
    print("[*] Mining MythosHub JS Chunks...")
    
    # 1. Get Homepage
    resp = requests.get(BASE_URL, headers=HEADERS, verify=False)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    scripts = []
    for s in soup.find_all('script'):
        if s.get('src'):
            scripts.append(s['src'])
            
    print(f"[+] Found {len(scripts)} script tags.")
    
    # 2. Download and Scan
    # We are looking for the definitions.
    # Let's look for "The Leader" AND "Innovation" in close proximity, or "Harmonious Farmer".
    
    found_intel = False
    
    for script_url in scripts:
        if script_url.startswith('/'):
            script_url = BASE_URL + script_url
        
        filename = script_url.split('/')[-1]
        print(f"    Scanning {filename}...", end=" ")
        
        try:
            js_resp = requests.get(script_url, headers=HEADERS, verify=False)
            content = js_resp.text
            
            # Save raw JS
            with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
                f.write(content)
                
            # Check for keywords
            # "Harmonious Farmer" is a specific string from Blood Type
            # "The Leader" is Numerology
            
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
                
                # Try to extract the JSON-like objects
                # Look for typical React props: {archetype:"The Leader",keywords:"..."}
                # Regex to find JSON-like structures containing our keywords
                # This is messy but we just need the text.
                
            else:
                print("Clean.")
                
        except Exception as e:
            print(f"Error: {e}")
            
    if not found_intel:
        print("[-] No static intelligence found in JS chunks. Data might be server-side only.")
    else:
        print("[+] Intelligence potentially found. Check the output directory.")

if __name__ == "__main__":
    mine_js()
