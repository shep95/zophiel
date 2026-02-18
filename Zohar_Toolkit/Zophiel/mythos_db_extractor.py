import requests
from bs4 import BeautifulSoup
import os
import time
import random
import re
import json
import urllib3

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.mythoshub.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'MYTHOS_DB')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(url, headers=HEADERS, verify=False, timeout=10)
        if response.status_code == 200:
            return response
        return None
    except Exception as e:
        print(f"[-] Error fetching {url}: {e}")
        return None

def get_sitemap():
    print("[*] Fetching Sitemap...")
    sitemap_url = f"{BASE_URL}/sitemap.xml"
    response = fetch(sitemap_url)
    urls = []
    if response:
        # Simple regex for xml tags since we just want URLs
        urls = re.findall(r'<loc>(.*?)</loc>', response.text)
        print(f"[+] Found {len(urls)} URLs in sitemap.")
        with open(os.path.join(OUTPUT_DIR, 'sitemap_urls.txt'), 'w') as f:
            for u in urls:
                f.write(u + '\n')
    else:
        print("[-] Sitemap not found or inaccessible.")
    return urls

def analyze_homepage_for_api():
    print("[*] Analyzing Homepage for API/Data signatures...")
    response = fetch(BASE_URL)
    if not response:
        return

    # Save raw HTML for inspection
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(response.text)

    # 1. Look for Next.js Data
    next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response.text)
    if next_data:
        print("[!] FOUND __NEXT_DATA__ JSON BLOB!")
        data = json.loads(next_data.group(1))
        with open(os.path.join(OUTPUT_DIR, 'next_data.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("[+] Dumped Next.js data to next_data.json")
    
    # 2. Look for JS files that might contain API routes
    scripts = re.findall(r'src="(/_next/static/chunks/[^"]+)"', response.text)
    print(f"[*] Found {len(scripts)} JS chunks. Scanning for API routes...")
    
    api_routes = set()
    for script_path in scripts:
        full_script_url = BASE_URL + script_path
        # print(f"    Scanning {script_path}...")
        js_resp = fetch(full_script_url)
        if js_resp:
            # Look for /api/ patterns
            found = re.findall(r'["\'](/api/[^"\']+)["\']', js_resp.text)
            for route in found:
                api_routes.add(route)
    
    if api_routes:
        print(f"[+] Discovered {len(api_routes)} potential API endpoints:")
        with open(os.path.join(OUTPUT_DIR, 'api_routes.txt'), 'w') as f:
            for route in api_routes:
                print(f"    - {route}")
                f.write(route + '\n')
    else:
        print("[-] No obvious API routes found in JS chunks.")

def scrape_all_urls(urls):
    print(f"[*] Attempting to scrape {len(urls)} pages...")
    full_db_path = os.path.join(OUTPUT_DIR, 'FULL_MYTHOS_DB.txt')
    
    with open(full_db_path, 'w', encoding='utf-8') as db_file:
        for i, url in enumerate(urls):
            print(f"[{i+1}/{len(urls)}] Scraping: {url}")
            resp = fetch(url)
            if resp:
                soup = BeautifulSoup(resp.content, 'html.parser')
                
                # Try to get main content
                content = ""
                main = soup.find('main')
                if main:
                    content = main.get_text(separator='\n', strip=True)
                else:
                    content = soup.get_text(separator='\n', strip=True)
                
                db_file.write(f"ID: {i}\nURL: {url}\nCONTENT:\n{content}\n" + "="*80 + "\n\n")
            
            if i > 50: # Safety break for now
                print("[!] Stopping after 50 pages to prevent timeout.")
                break

if __name__ == "__main__":
    urls = get_sitemap()
    analyze_homepage_for_api()
    if urls:
        scrape_all_urls(urls)
    else:
        # Fallback to manual list if sitemap fails
        scrape_all_urls([
            "https://www.mythoshub.com/numerology",
            "https://www.mythoshub.com/mbti",
            "https://www.mythoshub.com/blood-type",
            "https://www.mythoshub.com/codex"
        ])
