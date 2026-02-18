import requests
import re
import os
import time
from urllib.parse import urljoin, urlparse

# Base URL for probing
BASE_URL = "https://www.midjourney.com"

# Standard Next.js paths to probe
PROBE_PATHS = [
    "/_next/static/buildManifest.js",
    "/_next/static/chunks/main.js",
    "/_next/static/chunks/webpack.js",
    "/_next/static/chunks/pages/_app.js",
    "/_next/static/chunks/pages/index.js",
    "/js/main.js",
    "/static/js/main.js"
]

OUTPUT_DIR = r"c:\Users\kille\Documents\trae_projects\osint_links\Zohar_Toolkit\Midjourney"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Referer": "https://www.midjourney.com/",
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def probe_and_scan():
    ensure_dir(OUTPUT_DIR)
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    found_files = []

    print(f"[*] Probing Next.js assets on {BASE_URL}...")
    
    for path in PROBE_PATHS:
        url = BASE_URL + path
        print(f"    -> Checking {url}...")
        try:
            r = session.get(url, timeout=5)
            if r.status_code == 200:
                print(f"       [+] FOUND! ({len(r.text)} bytes)")
                filename = os.path.basename(path)
                local_path = os.path.join(OUTPUT_DIR, filename)
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(r.text)
                found_files.append(local_path)
                
                # If we found buildManifest, parse it for more files
                if "buildManifest" in filename:
                    parse_manifest(r.text, session)
            else:
                print(f"       [-] Status: {r.status_code}")
        except Exception as e:
            print(f"       [!] Error: {e}")

    # Scan anything we found
    for filepath in found_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        scan_file(filepath, content)

def parse_manifest(content, session):
    print(f"[*] Parsing buildManifest...")
    # Look for paths inside the manifest: "static/chunks/..."
    # Pattern: "static/chunks/[^"]+\.js"
    matches = re.findall(r'static/chunks/[a-zA-Z0-9\-\.]+\.js', content)
    unique_matches = list(set(matches))
    
    print(f"    -> Found {len(unique_matches)} additional chunks.")
    
    for match in unique_matches:
        url = f"{BASE_URL}/_next/{match}"
        filename = os.path.basename(match)
        local_path = os.path.join(OUTPUT_DIR, filename)
        
        print(f"    -> Downloading {filename}...")
        try:
            r = session.get(url, timeout=5)
            if r.status_code == 200:
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(r.text)
                # Quick scan immediately
                scan_file(local_path, r.text)
            else:
                 print(f"       [-] Failed: {r.status_code}")
        except Exception as e:
            print(f"       [!] Error: {e}")

def scan_file(filepath, content):
    keywords = [
        "api_key", "secret", "token", "auth", "admin", "internal", 
        "stripe", "payment", "billing", "graphql", "mutation", 
        "feature_flag", "experiment", "debug", "api.midjourney.com",
        "cdn.midjourney.com", "discord"
    ]
    
    print(f"       [*] Scanning {os.path.basename(filepath)}...")
    
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

if __name__ == "__main__":
    probe_and_scan()
