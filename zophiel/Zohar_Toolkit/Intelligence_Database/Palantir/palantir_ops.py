import requests
from bs4 import BeautifulSoup
import re
import time
import json

class PalantirOps:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.tech_intel = []
        self.target_intel = []

    def scrape_architecture(self):
        print("[*] Infiltrating Documentation for Software Mechanics...")
        # Key technical pages identified in previous sitemap scan
        urls = [
            "https://www.palantir.com/docs/foundry/aip/aip-features/",
            "https://www.palantir.com/docs/foundry/aip/aip-security/",
            "https://www.palantir.com/docs/foundry/aip/bring-your-own-model/",
            "https://www.palantir.com/docs/foundry/data-integration/architecture/" # Guessing common paths
        ]
        
        for url in urls:
            try:
                print(f"    - Analyzing: {url}")
                r = requests.get(url, headers=self.headers)
                if r.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Extract Technical Concepts (Headings + Paragraphs)
                content_block = soup.find('main') or soup.find('article') or soup.find('body')
                text = content_block.get_text(" ", strip=True)
                
                # Regex for interesting technical keywords
                patterns = {
                    "Protocols": r'(gRPC|REST|GraphQL|OData|JDBC)',
                    "Auth Methods": r'(OAuth|SAML|OIDC|Kerberos|mTLS)',
                    "Data Formats": r'(Parquet|Avro|JSON|Delta Lake)',
                    "Internal Components": r'(Magritte|Foundry|Gotham|Apollo|Rubix|Phonograph)',
                    "Infrastructure": r'(Kubernetes|Spark|Flink|Postgres|Cassandra)'
                }
                
                findings = {k: set(re.findall(p, text, re.IGNORECASE)) for k, p in patterns.items()}
                
                # Extract specific "How it works" snippets
                # Look for sentences containing "architecture", "pipeline", "connects to"
                sentences = re.split(r'(?<=[.!?]) +', text)
                mechanics = [s for s in sentences if any(x in s.lower() for x in ['architecture', 'data flow', 'pipeline', 'connects to', 'ingests'])][:3]
                
                self.tech_intel.append({
                    "url": url,
                    "findings": findings,
                    "mechanics": mechanics
                })
                
            except Exception as e:
                print(f"[-] Error scraping {url}: {e}")

    def investigate_melissa(self):
        print("\n[*] Initiating Targeted OSINT: melissam@palantir.com")
        target = "melissam"
        email = "melissam@palantir.com"
        
        # 1. Passive Dork Generation (Simulating what we would search)
        dorks = [
            f'site:linkedin.com "palantir" "melissa"',
            f'site:github.com "{email}"',
            f'site:twitter.com "{target}"',
            f'"{email}" filetype:pdf',
            f'"{email}" filetype:txt',
            f'site:pastebin.com "{email}"'
        ]
        
        print("    [+] Generated Hunter Dorks (Manual Check Recommended):")
        for d in dorks:
            print(f"      - {d}")

        # 2. Username Enumeration (Common Tech Platforms)
        # Checking if 'melissam' exists on major platforms (High false positive rate for common names, but worth checking)
        platforms = [
            ("GitHub", f"https://github.com/{target}"),
            ("Twitter", f"https://twitter.com/{target}"),
            ("Medium", f"https://medium.com/@{target}")
        ]
        
        print(f"\n    [+] Checking username handle '{target}':")
        for name, url in platforms:
            try:
                r = requests.get(url, headers=self.headers, timeout=5)
                if r.status_code == 200:
                    print(f"      - [POSSIBLE MATCH] {name}: {url}")
                else:
                    print(f"      - {name}: Not found ({r.status_code})")
            except:
                print(f"      - {name}: Error")

    def find_subdomains(self):
        print("\n[*] Starting Subdomain Discovery (Brute-force)...")
        # Common enterprise and Palantir-specific subdomains
        subs = [
            "www", "dev", "staging", "prod", "api", "auth", "login", "sso", "vpn", 
            "mail", "remote", "portal", "dashboard", "foundry", "gotham", "apollo", 
            "rubix", "magritte", "docs", "support", "jira", "confluence", 
            "gitlab", "github", "jenkins", "ci", "learn", "blog", "investors",
            "start", "signup", "register", "status", "jobs", "careers"
        ]
        
        found_domains = []
        for sub in subs:
            domain = f"https://{sub}.palantir.com"
            try:
                # Fast timeout to avoid hanging
                r = requests.get(domain, headers=self.headers, timeout=3, allow_redirects=True)
                print(f"    [+] Found: {domain} [{r.status_code}] - {r.url}")
                found_domains.append({"domain": domain, "status": r.status_code, "final_url": r.url})
            except requests.exceptions.RequestException:
                pass # Silent fail for non-existent
        
        self.tech_intel.append({"type": "subdomains", "data": found_domains})

    def scan_js_secrets(self):
        print("\n[*] Scanning JavaScript Bundles for Secrets (The Canon Law 1)...")
        try:
            r = requests.get("https://www.palantir.com", headers=self.headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
            
            # Filter for internal JS only
            internal_scripts = [s for s in scripts if 'palantir.com' in s or s.startswith('/')]
            
            print(f"    - Found {len(internal_scripts)} JS files to analyze.")
            
            api_key_pattern = r'(?i)(api_key|apikey|secret|token|auth)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})["\']?'
            endpoint_pattern = r'https?://[a-zA-Z0-9.-]+\.palantir\.com/[a-zA-Z0-9/_.-]*'
            
            for script in internal_scripts:
                if script.startswith('/'):
                    url = f"https://www.palantir.com{script}"
                else:
                    url = script
                    
                print(f"    - Fetching: {url}")
                try:
                    js_r = requests.get(url, headers=self.headers, timeout=5)
                    content = js_r.text
                    
                    # Scan for keys
                    keys = re.findall(api_key_pattern, content)
                    if keys:
                        print(f"      [!] POTENTIAL SECRET in {url}: {keys}")
                    
                    # Scan for internal endpoints
                    endpoints = set(re.findall(endpoint_pattern, content))
                    if endpoints:
                        print(f"      [i] Discovered Endpoints in {url}:")
                        for e in list(endpoints)[:5]: # Show top 5
                            print(f"        - {e}")
                            
                except Exception as e:
                    print(f"      [-] Error reading JS: {e}")
                    
        except Exception as e:
            print(f"[-] Error in JS Scan: {e}")

    def generate_deep_report(self):
        filename = "Palantir_Deep_Dive.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# PALANTIR DEEP DIVE: ARCHITECTURE & TARGET\n")
            f.write(f"**Date:** {time.strftime('%Y-%m-%d')}\n\n")
            
            f.write("## 1. SOFTWARE MECHANICS (AIP & FOUNDRY)\n")
            for item in self.tech_intel:
                if item.get("type") == "subdomains":
                    f.write("\n### DISCOVERED SUBDOMAINS (Active Brute-Force)\n")
                    for sub in item["data"]:
                        f.write(f"- {sub['domain']} [{sub['status']}] -> {sub['final_url']}\n")
                    continue

                f.write(f"### Source: {item['url']}\n")
                
                f.write("**Technical Stack Detected:**\n")
                for cat, values in item['findings'].items():
                    if values:
                        f.write(f"- {cat}: {', '.join(values)}\n")
                
                f.write("\n**Operational Mechanics (Snippets):**\n")
                for mech in item['mechanics']:
                    f.write(f"> ...{mech}...\n")
                f.write("\n---\n")
            
            f.write("\n## 2. TARGET: MELISSA M (melissam@palantir.com)\n")
            f.write("**Profile Analysis:**\n")
            f.write("- **Email Pattern:** Firstname + Last Initial (Standard Corporate).\n")
            f.write("- **Role Hypothesis:** Likely PR/Comms/HR given the public exposure of the email.\n")
            f.write("- **Username Reuse:** 'melissam' is a very common handle. Direct username matches are likely False Positives unless corroborated by Palantir context.\n")
            
            f.write("\n**Recommended Search Vectors (Dorks):**\n")
            f.write("Run these to find direct footprints:\n")
            f.write("1. `site:linkedin.com \"Palantir\" \"Melissa\"`\n")
            f.write("2. `\"melissam@palantir.com\"`\n")
            
        print(f"\n[+] Deep Dive Report Generated: {filename}")

if __name__ == "__main__":
    ops = PalantirOps()
    ops.find_subdomains()     # Run Subdomain Scan
    ops.scan_js_secrets()     # Run JS Scan
    ops.scrape_architecture() # Run Doc Scan
    ops.investigate_melissa() # Run Target Scan
    ops.generate_deep_report()
    ops.generate_deep_report()
