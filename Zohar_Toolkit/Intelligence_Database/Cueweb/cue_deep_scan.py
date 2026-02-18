import requests
from bs4 import BeautifulSoup
import re
import time
import os
import urllib3

# Disable SSL warnings for cleaner output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CueDeepScan:
    def __init__(self):
        self.base_url = "https://cuewebapp.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://cuewebapp.com/'
        }
        self.js_files = []
        self.findings = {
            "secrets": [],
            "emails": [],
            "endpoints": [],
            "dos_vectors": [],
            "exposed_files": []
        }
        
        # Regex Patterns for Secrets
        self.patterns = {
            "Stripe_Key": r"pk_live_[0-9a-zA-Z]{24}",
            "Stripe_Secret": r"sk_live_[0-9a-zA-Z]{24}",
            "AWS_Access_Key": r"AKIA[0-9A-Z]{16}",
            "Firebase_Config": r"firebaseConfig",
            "Google_API": r"AIza[0-9A-Za-z-_]{35}",
            "JWT_Token": r"eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}",
            "Email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "DB_Connection": r"(postgres|mysql|mongodb)://[a-zA-Z0-9:]+@[a-zA-Z0-9.]+:[0-9]+",
            "Private_Key": r"-----BEGIN PRIVATE KEY-----"
        }

    def find_js_bundles(self):
        print(f"[*] Spidering {self.base_url} for JavaScript bundles...")
        try:
            r = requests.get(self.base_url, headers=self.headers, verify=False, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Find all script src
            scripts = soup.find_all('script')
            for script in scripts:
                src = script.get('src')
                if src:
                    if src.startswith('/'):
                        full_url = self.base_url + src
                    elif src.startswith('http'):
                        full_url = src
                    else:
                        continue
                    
                    if full_url not in self.js_files:
                        self.js_files.append(full_url)
                        
            print(f"    [+] Found {len(self.js_files)} JS files.")
            
        except Exception as e:
            print(f"    [!] Error spidering: {e}")

    def scan_js_for_secrets(self):
        print(f"[*] Scanning {len(self.js_files)} JS files for secrets & emails...")
        
        for js_url in self.js_files:
            try:
                # print(f"    [>] Downloading {js_url.split('/')[-1]}...")
                r = requests.get(js_url, headers=self.headers, verify=False, timeout=5)
                content = r.text
                
                # Check all regex patterns
                for name, pattern in self.patterns.items():
                    matches = re.findall(pattern, content)
                    for match in matches:
                        # Filter out common false positives for emails
                        if name == "Email" and ("example.com" in match or "sentry" in match or "react" in match):
                            continue
                        
                        finding = f"[{name}] Found in {js_url.split('/')[-1]}: {match[:50]}..."
                        if finding not in self.findings["secrets"]:
                            self.findings["secrets"].append(finding)
                            print(f"      [!] LEAK: {name} found! -> {match[:30]}...")

                # Extract potential API endpoints
                # Look for "/api/..." strings
                endpoints = re.findall(r'["\'](/api/[a-zA-Z0-9_/-]+)["\']', content)
                for ep in endpoints:
                    if ep not in self.findings["endpoints"]:
                        self.findings["endpoints"].append(ep)

            except Exception as e:
                pass

    def check_sensitive_files(self):
        print("[*] Probing for sensitive configuration files...")
        files_to_check = [
            ".env",
            ".env.local",
            ".git/HEAD",
            "docker-compose.yml",
            "package.json",
            "sitemap.xml",
            "robots.txt",
            "server-status"
        ]
        
        for file in files_to_check:
            url = f"{self.base_url}/{file}"
            try:
                r = requests.get(url, headers=self.headers, verify=False, timeout=3)
                if r.status_code == 200:
                    # Verify it's not a custom 404 page by checking content type or length
                    if "html" not in r.headers.get('Content-Type', '') and len(r.text) < 5000:
                        print(f"    [!] EXPOSED: {url} (Status: 200)")
                        self.findings["exposed_files"].append(url)
                    elif "robots.txt" in file:
                         print(f"    [i] Found robots.txt")
                         self.findings["exposed_files"].append(url)
            except:
                pass

    def verify_dos_vectors(self):
        print("[*] Verifying Denial of Service (DoS) Vectors (Rate Limit Check)...")
        # We test a heavy endpoint or common API endpoint
        targets = [
            "/api/health",
            "/api/v2/stripe", # We know this exists from previous intel
            "/login",
            "/signup"
        ]
        
        for path in targets:
            url = self.base_url + path
            print(f"    [>] Testing {path} (Burst 5 requests)...")
            
            start_time = time.time()
            success_count = 0
            blocked = False
            
            for i in range(5):
                try:
                    r = requests.get(url, headers=self.headers, verify=False, timeout=2)
                    if r.status_code == 429:
                        blocked = True
                        break
                    if r.status_code in [200, 404, 401, 500]: # 404/401 still means the server processed it
                        success_count += 1
                except:
                    pass
            
            if not blocked and success_count == 5:
                print(f"      [!] VULNERABLE: No Rate Limiting detected on {path}")
                self.findings["dos_vectors"].append(f"No Rate Limiting on {path}")
            elif blocked:
                print(f"      [+] Secure: Rate Limiting active on {path}")

    def generate_report(self):
        print("\n[*] Generating Intelligence Report...")
        report_path = os.path.join(os.path.dirname(__file__), "Cue_Vulnerability_Scan.txt")
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("CUE WEBAPP - DEEP VULNERABILITY SCAN\n")
            f.write("====================================\n\n")
            
            f.write("1. SENSITIVE DATA LEAKS (SECRETS/KEYS)\n")
            if self.findings["secrets"]:
                for item in self.findings["secrets"]:
                    f.write(f"- {item}\n")
            else:
                f.write("- No hardcoded secrets found in JS bundles.\n")
            
            f.write("\n2. EXPOSED FILES & INFRASTRUCTURE\n")
            if self.findings["exposed_files"]:
                for item in self.findings["exposed_files"]:
                    f.write(f"- {item}\n")
            else:
                f.write("- No sensitive files exposed.\n")

            f.write("\n3. DENIAL OF SERVICE (DoS) VECTORS\n")
            f.write("These endpoints lack rate limiting and can be flooded to shut down the service:\n")
            if self.findings["dos_vectors"]:
                for item in self.findings["dos_vectors"]:
                    f.write(f"- {item}\n")
            else:
                f.write("- No obvious DoS vectors found (Rate Limiting might be active).\n")
                
            f.write("\n4. DISCOVERED API ENDPOINTS\n")
            for ep in self.findings["endpoints"]:
                f.write(f"- {ep}\n")

        print(f"[+] Report saved to: {report_path}")

if __name__ == "__main__":
    scanner = CueDeepScan()
    scanner.find_js_bundles()
    scanner.scan_js_for_secrets()
    scanner.check_sensitive_files()
    scanner.verify_dos_vectors()
    scanner.generate_report()
