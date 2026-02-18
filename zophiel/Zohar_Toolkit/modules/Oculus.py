import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import warnings

# Suppress insecure request warnings
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

class Oculus:
    """
    OCULUS: The All-Seeing Eye.
    Module for scanning client-side JavaScript for exposed secrets and API keys.
    Enforces Law 1 of The Canon: "The Sanctity of Secrets".
    """
    def __init__(self, target_url, oracle=None):
        self.target_url = target_url
        self.oracle = oracle
        self.base_url = target_url # Initialize base_url for relative paths
        self.session = requests.Session()
        self.findings = {}
        # Common headers to mimic a browser
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    def gaze(self):
        """
        Scans the target dashboard for JavaScript bundles and extracts secrets.
        """
        print(f"\n[OCULUS] Gazing into the abyss of {self.target_url}...")
        
        # Ensure findings structure exists
        self.findings.setdefault('keys', [])
        
        try:
            # Enhanced headers for WAF bypass
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0"
            }
            
            response = requests.get(self.target_url, headers=headers, verify=False, timeout=15)
            if response.status_code != 200:
                print(f"  [!] Failed to reach target: {response.status_code}")
                # Try to look at the text anyway if it's 403, sometimes WAFs return partial content
                if response.status_code == 403:
                    print("  [!] WAF detected. Attempting to parse whatever is returned...")
                else:
                    return self.findings

            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = []

            # Strategy 1: Vite/Standard/Next.js
            for script in soup.find_all('script'):
                if script.get('src'):
                    src = script.get('src')
                    # Handle relative paths
                    if src.startswith('/'):
                        src = self.base_url + src
                    elif not src.startswith('http'):
                        src = self.base_url + '/' + src
                    
                    # Filter relevant scripts (Relaxed for Deep Dive)
                    # We want practically everything local or CDN based, not just "main" or "app"
                    # But we exclude analytics trackers to save time
                    if any(x in src for x in ['google-analytics', 'gtm', 'facebook', 'ads']):
                        continue
                    scripts.append(src)
            
            # Strategy 2: Inline Scripts (Next.js often puts build manifests in inline scripts)
            for script in soup.find_all('script'):
                if not script.get('src') and script.string:
                    # Quick scan of inline scripts for blatant keys
                    self.analyze_content(script.string, "inline_script")

            print(f"  [+] Found {len(scripts)} potential script vectors.")
            
            for script_url in scripts:
                self.analyze_script(script_url)

        except Exception as e:
            print(f"  [!] Oculus Malfunction: {e}")
            
        return self.findings

    def analyze_script(self, script_url):
        print(f"  [>] Analyzing: {script_url.split('/')[-1]}...")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            js_content = requests.get(script_url, headers=headers, verify=False, timeout=10).text
            self.analyze_content(js_content, script_url)

        except Exception as e:
            print(f"    [x] Failed to read script: {e}")

    def analyze_content(self, content, source):
        # Regex Patterns
        patterns = {
            "supabase_url": r"https://[a-z0-9]+\.supabase\.co",
            "supabase_key": r"eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+",
            "google_api": r"AIza[0-9A-Za-z-_]{35}",
            "algolia_key": r"Algolia\s*:\s*['\"]([a-zA-Z0-9]+)['\"]",
            "aws_key": r"AKIA[0-9A-Z]{16}",
            "openai_sk": r"sk-[a-zA-Z0-9]{48}",
            "internal_codename": r"(strawberry|orion|arrakis|gpt-5|gpt-4.5|q-star|feathers)", 
            "feature_flag": r"feature_gates\s*:\s*\{([^}]+)\}",
            "github_link": r"github\.com\/([a-zA-Z0-9\-]+)",
            "openai_email": r"[a-zA-Z0-9._%+-]+@openai\.com",
            "developer_comment": r"(TODO|FIXME|HACK|Author|Created by|Dev|Maintainer)[:\s]+(.*?)(?=\n|$)"
        }
        
        for key, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                unique_matches = list(set(matches))
                print(f"    [!] DETECTED {key.upper()} in {source}: {len(unique_matches)} instances.")
                if key not in self.findings: self.findings[key] = []
                self.findings[key].extend(unique_matches)
                
                if self.oracle:
                    for m in unique_matches:
                        self.oracle.add_secret(key, m, source)

                # Map to generic 'keys' for backend compatibility if it's a key type
                if 'key' in key or 'sk' in key or 'api' in key:
                     self.findings['keys'].extend(unique_matches)


