import requests
import re
import os
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class HeaderHunter:
    def __init__(self):
        self.base_url = "https://chatgpt.com" # Main entry point, often redirects to chat-new logic
        self.assets_dir = "Zohar_Toolkit/loot/js_assets"
        self.headers_found = set()
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def fetch_main_page(self):
        print(f"[*] Fetching main page: {self.base_url}")
        try:
            resp = requests.get(self.base_url, headers={"User-Agent": self.ua}, verify=False)
            if resp.status_code != 200:
                print(f"[-] Failed to fetch main page: {resp.status_code}")
                return ""
            return resp.text
        except Exception as e:
            print(f"[-] Error fetching main page: {e}")
            return ""

    def extract_js_links(self, html):
        # Look for _next/static/... .js files
        # Pattern: src="/_next/static/chunks/..."
        patterns = [
            r'src="(/_next/static/chunks/[^"]+\.js)"',
            r'src="(/_next/static/[^"]+\.js)"',
            r'"(/_next/static/chunks/[^"]+\.js)"' # Sometimes in JSON blobs
        ]
        
        links = set()
        for p in patterns:
            matches = re.findall(p, html)
            for m in matches:
                full_url = urljoin(self.base_url, m)
                links.add(full_url)
        
        print(f"[*] Found {len(links)} JS bundles.")
        return list(links)

    def scan_js_for_headers(self, js_url):
        try:
            print(f"[*] Scanning: {js_url.split('/')[-1]}")
            resp = requests.get(js_url, headers={"User-Agent": self.ua}, verify=False)
            content = resp.text
            
            # Regex for headers
            # Common patterns: 'X-OpenAI-...', "X-OpenAI-..."
            header_pattern = r'["\'](X-OpenAI-[a-zA-Z0-9-]+)["\']'
            matches = re.findall(header_pattern, content, re.IGNORECASE)
            
            # Also look for Authorization patterns or other secrets
            # secret_pattern = r'["\'](sk-[a-zA-Z0-9]{20,})["\']'
            
            if matches:
                for m in matches:
                    if m not in self.headers_found:
                        print(f"    [!!!] FOUND HEADER: {m}")
                        self.headers_found.add(m)
            
            return content
        except Exception as e:
            print(f"[-] Error scanning JS: {e}")
            return ""

    def run(self):
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)
            
        html = self.fetch_main_page()
        js_links = self.extract_js_links(html)
        
        # Prioritize main chunks (often 'main', 'app', or similar)
        # But scanning all is safer
        for link in js_links:
            self.scan_js_for_headers(link)
            
        print("\n=== HEADER HUNT RESULTS ===")
        for h in self.headers_found:
            print(f"- {h}")

        # Save to loot
        with open("Zohar_Toolkit/loot/discovered_headers.txt", "w") as f:
            for h in self.headers_found:
                f.write(h + "\n")

if __name__ == "__main__":
    hunter = HeaderHunter()
    hunter.run()
