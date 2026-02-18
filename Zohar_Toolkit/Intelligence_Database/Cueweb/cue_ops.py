import requests
from bs4 import BeautifulSoup
import re
import time
import json
import os

class CueOps:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.base_url = "https://cuewebapp.com"
        self.intel = {
            "subdomains": [],
            "endpoints": [],
            "secrets": [],
            "tech_stack": []
        }
        self.known_keys = [
            "qymjm336fz4hbt34deurnogd", # Legacy Free
            "l65k2ccw4vwfbh8zti6dd5i6", # Legacy Cue+
            "tog6oq50adr4yxwuzu8vxndh"  # Legacy Lifetime
        ]

    def scan_subdomains(self):
        print("[*] Verifying Infrastructure (Subdomains)...")
        subs = ["www", "api", "cms", "staging", "admin", "dev", "test", "dashboard", "app"]
        
        for sub in subs:
            domain = f"https://{sub}.cuewebapp.com"
            try:
                r = requests.get(domain, headers=self.headers, timeout=5, verify=False) # Verify=False for staging SSL issues
                status = r.status_code
                print(f"    [+] {domain}: {status}")
                self.intel["subdomains"].append({
                    "domain": domain,
                    "status": status,
                    "server": r.headers.get("Server", "Unknown")
                })
            except Exception as e:
                # print(f"    [-] {domain}: Unreachable ({e})")
                pass

    def check_endpoints(self):
        print("\n[*] Validating Critical API Endpoints...")
        # Endpoints from legacy report
        endpoints = [
            f"{self.base_url}/api/v3/profile",
            f"{self.base_url}/api/v2/stripe",
            f"{self.base_url}/api/v2/favorites",
            "https://api.cuewebapp.com/health",
            "https://api.cuewebapp.com/api/v3/profile",
            "https://api.cuewebapp.com/api/v2/stripe"
        ]

        for ep in endpoints:
            try:
                # We use POST for some as they were identified as POST-only
                if "stripe" in ep or "profile" in ep:
                    r = requests.post(ep, headers=self.headers, timeout=5, verify=False)
                else:
                    r = requests.get(ep, headers=self.headers, timeout=5, verify=False)
                
                print(f"    [+] Endpoint: {ep} -> {r.status_code}")
                self.intel["endpoints"].append({
                    "url": ep,
                    "status": r.status_code,
                    "method": "POST" if "stripe" in ep or "profile" in ep else "GET"
                })
                
                # Check specifically for rate limiting on /health
                if "health" in ep and r.status_code == 200:
                    self.check_rate_limit(ep)

            except Exception as e:
                print(f"    [-] Endpoint {ep} failed: {e}")

    def check_rate_limit(self, url):
        print(f"    [*] Testing Rate Limit on {url} (Burst 10)...")
        success = 0
        for _ in range(10):
            try:
                r = requests.get(url, headers=self.headers, timeout=2, verify=False)
                if r.status_code == 200:
                    success += 1
            except:
                pass
        
        if success == 10:
            print("      [!] VULNERABLE: No Rate Limiting detected (10/10 Passed)")
            self.intel["tech_stack"].append("VULNERABLE: No API Rate Limiting")
        else:
            print(f"      [i] Rate Limit active? {success}/10 passed")

    def scan_js_secrets(self):
        print("\n[*] Scanning JavaScript for Secrets & Keys...")
        try:
            r = requests.get(self.base_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Find Next.js data
            next_data = soup.find('script', id='__NEXT_DATA__')
            if next_data:
                print("    [+] Found __NEXT_DATA__ JSON blob. Analyzing...")
                data_str = next_data.string
                # Check for known keys in the blob
                for key in self.known_keys:
                    if key in data_str:
                        print(f"      [!] CONFIRMED LEAK: Legacy Key {key} is still present in frontend!")
                        self.intel["secrets"].append(f"Confirmed Legacy Key: {key}")
                
                # Look for new patterns
                new_keys = re.findall(r'[a-z0-9]{24}', data_str)
                if new_keys:
                    unique_keys = set(new_keys) - set(self.known_keys)
                    if unique_keys:
                        print(f"      [?] Possible NEW Keys found: {list(unique_keys)[:5]}")
                        self.intel["secrets"].extend([f"Possible New Key: {k}" for k in unique_keys])

            # Find JS files
            scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
            print(f"    [i] Analyzing {len(scripts)} script files...")
            
            for script in scripts:
                if script.startswith('/'):
                    script_url = self.base_url + script
                elif script.startswith('http'):
                    script_url = script
                else:
                    continue

                try:
                    js_r = requests.get(script_url, headers=self.headers, timeout=5)
                    content = js_r.text
                    
                    # Regex for generic API keys
                    api_keys = re.findall(r'(?i)(api_key|apikey|secret|token)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})', content)
                    if api_keys:
                        print(f"      [!] Key Pattern in {script_url}: {api_keys}")
                        self.intel["secrets"].append(f"Pattern in {script_url}: {api_keys}")

                except:
                    pass

        except Exception as e:
            print(f"[-] JS Scan Error: {e}")

    def generate_report(self):
        filename = "Cue_Deep_Dive.md"
        print(f"\n[*] Generating Report: {filename}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# CUE WEBAPP INTELLIGENCE DOSSIER\n")
            f.write(f"**Date:** {time.strftime('%Y-%m-%d')}\n")
            f.write(f"**Target:** {self.base_url}\n\n")
            
            f.write("## 1. INFRASTRUCTURE MAP\n")
            for sub in self.intel["subdomains"]:
                f.write(f"- **{sub['domain']}** (Status: {sub['status']}) - Server: {sub['server']}\n")
            
            f.write("\n## 2. API ENDPOINT ANALYSIS\n")
            for ep in self.intel["endpoints"]:
                f.write(f"- `{ep['method']} {ep['url']}` -> {ep['status']}\n")
            
            f.write("\n## 3. SECRET LEAKS & KEYS\n")
            if self.intel["secrets"]:
                for sec in self.intel["secrets"]:
                    f.write(f"- ⚠️ {sec}\n")
            else:
                f.write("- No obvious secrets found in this scan pass.\n")

            f.write("\n## 4. VULNERABILITY SUMMARY\n")
            for vuln in self.intel["tech_stack"]:
                f.write(f"- 🚨 {vuln}\n")

        print("[+] Report generation complete.")

if __name__ == "__main__":
    ops = CueOps()
    ops.scan_subdomains()
    ops.check_endpoints()
    ops.scan_js_secrets()
    ops.generate_report()
