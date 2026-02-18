import requests
import re
import os
import time
from urllib.parse import urljoin, urlparse

# URL list to try
URLS = [
    "https://www.midjourney.com",
    "https://www.midjourney.com/home",
    "https://www.midjourney.com/auth/signin",
    "https://legacy.midjourney.com"
]

OUTPUT_DIR = r"c:\Users\kille\Documents\trae_projects\osint_links\Zohar_Toolkit\Midjourney"

# Mimic a real browser better
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1"
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def fetch_and_scan():
    ensure_dir(OUTPUT_DIR)
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    content = None
    final_url = None

    for url in URLS:
        print(f"[*] Trying {url}...")
        try:
            r = session.get(url, timeout=10)
            if r.status_code == 200:
                print(f"    [+] Success! ({len(r.text)} bytes)")
                content = r.text
                final_url = url
                break
            else:
                print(f"    [-] Status: {r.status_code}")
        except Exception as e:
            print(f"    [!] Error: {e}")
            
    if not content:
        print("[!] All attempts failed.")
        return

    # Save homepage
    with open(os.path.join(OUTPUT_DIR, "home.html"), "w", encoding="utf-8") as f:
        f.write(content)
        
    # Extract script src
    # Look for both src="..." and src='...'
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content)
    
    # Also look for Next.js specific static chunks often embedded in JSON or simple script tags
    # Example: /_next/static/chunks/main-....js
    next_chunks = re.findall(r'/_next/static/chunks/[a-zA-Z0-9\-\.]+\.js', content)
    scripts.extend(next_chunks)
    
    # Deduplicate
    scripts = list(set(scripts))
    
    print(f"[*] Found {len(scripts)} scripts.")
    
    js_files = []
    for s in scripts:
        if s.startswith("/"):
            full_url = urljoin(final_url, s)
        elif s.startswith("http"):
            full_url = s
        else:
            continue
            
        # Filter for likely app bundles
        if ".js" in full_url:
            js_files.append(full_url)

    print(f"[*] Identifying {len(js_files)} JS bundles to download...")
    
    # Download and Scan
    for js_url in js_files:
        filename = os.path.basename(urlparse(js_url).path)
        if not filename.endswith(".js"):
            filename += ".js"
            
        local_path = os.path.join(OUTPUT_DIR, filename)
        
        print(f"    -> Downloading {filename}...")
        try:
            r_js = session.get(js_url, timeout=10)
            if r_js.status_code != 200:
                print(f"       [-] Status: {r_js.status_code}")
                continue
                
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(r_js.text)
                
            # Quick Scan
            scan_file(local_path, r_js.text)
            
        except Exception as e:
            print(f"       [!] Failed: {e}")
        
        time.sleep(0.5)

def scan_file(filepath, content):
    keywords = [
        "api_key", "secret", "token", "auth", "admin", "internal", 
        "stripe", "payment", "billing", "graphql", "mutation", 
        "feature_flag", "experiment", "debug", "api.midjourney.com",
        "cdn.midjourney.com"
    ]
    
    print(f"       [*] Scanning {os.path.basename(filepath)} ({len(content)} bytes)...")
    
    found = False
    for kw in keywords:
        matches = [m.start() for m in re.finditer(re.escape(kw), content, re.IGNORECASE)]
        if matches:
            found = True
            print(f"           [!] Found '{kw}' at {len(matches)} locations")
            # Print context for first match
            start = max(0, matches[0] - 50)
            end = min(len(content), matches[0] + 100)
            snippet = content[start:end].replace("\n", " ")
            print(f"               Context: ...{snippet}...")

    if not found:
        print("           [-] No obvious secrets found.")

if __name__ == "__main__":
    fetch_and_scan()
