import requests
import re
import json
import os
import concurrent.futures
from urllib.parse import urljoin, urlparse
import argparse

# Configuration
parser = argparse.ArgumentParser(description="Extract API routes from JS files.")
parser.add_argument("--input", default=os.path.join(os.path.dirname(__file__), "..", "..", "osint_links", "Zohar_Toolkit", "temp_alive_x.json"), help="Input JSON file with URLs.")
parser.add_argument("--output", default=os.path.join("output", "api_routes.json"), help="Output JSON file for the routes.")
args = parser.parse_args()

INPUT_FILE = args.input
OUTPUT_FILE = args.output
MAX_WORKERS = 20

# Regex Patterns
JS_FILE_PATTERN = re.compile(r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)["\']', re.IGNORECASE)
# Matches paths that start with / and look like API routes or interesting paths
# We filter for specific keywords or structure to reduce noise
ROUTE_PATTERNS = [
    re.compile(r'["\'](\/api\/[a-zA-Z0-9_\-\/]+)["\']'),
    re.compile(r'["\'](\/i\/[a-zA-Z0-9_\-\/]+)["\']'),
    re.compile(r'["\'](\/v\d+\/[a-zA-Z0-9_\-\/]+)["\']'),
    re.compile(r'["\'](\/graphql[a-zA-Z0-9_\-\/]*)["\']'),
    re.compile(r'["\'](\/internal\/[a-zA-Z0-9_\-\/]+)["\']'),
    re.compile(r'["\'](\/admin\/[a-zA-Z0-9_\-\/]+)["\']'),
]

# Headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def load_targets():
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Input file not found: {INPUT_FILE}")
        return []
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return list(data.keys())
    return []

def fetch_js_urls(url):
    js_links = set()
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        if resp.status_code == 200:
            matches = JS_FILE_PATTERN.findall(resp.text)
            for match in matches:
                full_url = urljoin(url, match)
                js_links.add(full_url)
    except Exception as e:
        pass # Silently fail for now
    return list(js_links)

def scan_js_for_routes(js_url):
    found_routes = set()
    try:
        resp = requests.get(js_url, headers=HEADERS, timeout=10, verify=False)
        if resp.status_code == 200:
            content = resp.text
            for pattern in ROUTE_PATTERNS:
                matches = pattern.findall(content)
                for match in matches:
                    # Basic noise filtering
                    if len(match) < 100 and " " not in match and "<" not in match:
                        found_routes.add(match)
    except Exception:
        pass
    return list(found_routes)

def process_target(url):
    print(f"[*] Scanning {url}...")
    results = {}
    js_urls = fetch_js_urls(url)
    
    all_routes = set()
    for js_url in js_urls:
        routes = scan_js_for_routes(js_url)
        if routes:
            all_routes.update(routes)
            
    if all_routes:
        results[url] = {
            "js_files_scanned": len(js_urls),
            "routes": sorted(list(all_routes))
        }
        print(f"[+] Found {len(all_routes)} routes in {url}")
        return results
    return None

def main():
    targets = load_targets()
    print(f"[*] Loaded {len(targets)} targets.")
    
    final_results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(process_target, url): url for url in targets}
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                final_results.update(result)
                
    # Save results
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2)
        
    print(f"[*] Scan complete. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()
