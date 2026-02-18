import os
import re
import sys
import json
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Ensure Zohar_Toolkit root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.Stealth_Manager import StealthSession

class Raziel_API_Siphon:
    """
    RAZIEL: The Keeper of Secrets.
    A sophisticated API discovery and scraping tool that combines:
    1. Stealth Mode (Proxy/User-Agent rotation)
    2. Static Analysis (JS Bundle Regex Scanning)
    3. Active Probing (Endpoint Verification)
    """
    
    def __init__(self, target_url, output_dir="Intelligence_Database/Raziel_Reports"):
        self.target_url = target_url
        self.domain = urlparse(target_url).netloc
        
        # Robustly locate proxies.txt
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        proxy_path = os.path.join(base_dir, "proxies.txt")
        if not os.path.exists(proxy_path):
             # Fallback to current directory
             proxy_path = "proxies.txt"
             
        self.stealth = StealthSession(proxy_file=proxy_path)
        self.output_dir = output_dir
        self.js_files = set()
        self.discovered_endpoints = set()
        self.vulnerable_endpoints = []
        self.source_repos_found = [] # Track for Law 7 Compliance
        self.comms_channels_found = [] # Track for Law 9 Compliance
        
        # Expanded Regex Patterns
        self.patterns = {
            'api_route': r'["\'](/backend-api/[a-zA-Z0-9-_/]+|/public-api/[a-zA-Z0-9-_/]+|/v1/[a-zA-Z0-9-_/]+|/api/[a-zA-Z0-9-_/]+)["\']',
            'deep_research': r'["\'](/[a-zA-Z0-9-_/]*deep-research[a-zA-Z0-9-_/]*)["\']',
            'supabase_key': r'sb-[a-zA-Z0-9-]{20,}',
            'generic_key': r'(?i)(api_key|access_token|secret)["\']?\s*[:=]\s*["\']([a-zA-Z0-9-_]{20,})["\']',
            'feature_gate': r'["\']([a-zA-Z0-9-_]*gate[a-zA-Z0-9-_]*)["\']',
            'source_repo': r'https?://(github\.com|gitlab\.com|bitbucket\.org)/[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+',
            'slack_webhook': r'https://hooks\.slack\.com/services/[A-Z0-9]+/[A-Z0-9]+/[a-zA-Z0-9]+',
            'discord_invite': r'(?:https?://)?(?:www\.)?(?:discord\.gg|discord\.com/invite)/[a-zA-Z0-9]+',
            'teams_webhook': r'https://[a-zA-Z0-9]+\.webhook\.office\.com/[a-zA-Z0-9/-]+',
            'internal_email': r'[a-zA-Z0-9._%+-]+@openai\.com'
        }

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def log(self, message, level="INFO"):
        print(f"[{level}] {message}")

    def crawl_js_bundles(self):
        """Fetches the main page and extracts JS bundle URLs."""
        self.log(f"Initiating Stealth Scan on {self.target_url}...", "RAZIEL")
        try:
            response = self.stealth.get(self.target_url)
            if response.status_code != 200:
                self.log(f"Failed to fetch main page: {response.status_code}", "ERROR")
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script', src=True)
            
            self.log(f"Found {len(scripts)} script tags.", "INFO")
            
            for script in scripts:
                src = script['src']
                full_url = urljoin(self.target_url, src)
                if self.domain in full_url or 'cdn' in full_url: # Focus on internal or CDN scripts
                    self.js_files.add(full_url)
            
            self.log(f"Identified {len(self.js_files)} unique JS bundles for analysis.", "INFO")
            
        except Exception as e:
            self.log(f"Crawl failed: {e}", "ERROR")

    def analyze_bundles(self):
        """Downloads and regex-scans each JS bundle."""
        self.log("Beginning Static Analysis of JS Bundles...", "RAZIEL")
        
        for js_url in self.js_files:
            try:
                self.log(f"Scanning: {js_url.split('/')[-1]}", "SCAN")
                response = self.stealth.get(js_url)
                if response.status_code == 200:
                    content = response.text
                    
                    # Scan for all patterns
                    for name, pattern in self.patterns.items():
                        matches = re.findall(pattern, content)
                        for match in matches:
                            # Handle tuple returns from groups
                            if isinstance(match, tuple):
                                match = match[0]
                            
                            # Clean up quotes if captured
                            match = match.strip('"\'')
                            
                            if name == 'api_route' or name == 'deep_research':
                                full_endpoint = urljoin(self.target_url, match)
                                self.discovered_endpoints.add(full_endpoint)
                                self.log(f"Discovered Endpoint: {match}", "DISCOVERY")
                            elif name == 'source_repo':
                                self.source_repos_found.append(match)
                                self.log(f"SOURCE CODE REPO FOUND: {match}", "CRITICAL")
                            elif name in ['slack_webhook', 'discord_invite', 'teams_webhook', 'internal_email']:
                                self.comms_channels_found.append(match)
                                self.log(f"INTERNAL COMMS FOUND ({name}): {match}", "CRITICAL")
                            elif name == 'supabase_key' or name == 'generic_key':
                                self.log(f"POTENTIAL KEY: {match}", "SECRET")
                            elif name == 'feature_gate':
                                self.log(f"Feature Gate: {match}", "GATE")
                                
            except Exception as e:
                self.log(f"Failed to analyze {js_url}: {e}", "WARN")

        self.log(f"Static Analysis Complete. Found {len(self.discovered_endpoints)} unique endpoints.", "SUCCESS")

    def active_probe(self):
        """Probes discovered endpoints to check for access."""
        self.log("Initiating Active Probing (The Siphon)...", "RAZIEL")
        
        for endpoint in self.discovered_endpoints:
            # Construct full URL
            # Handle relative paths carefully
            if endpoint.startswith('http'):
                full_url = endpoint
            else:
                full_url = urljoin(self.target_url, endpoint)

            try:
                # Random sleep to avoid flooding
                time.sleep(0.5) 
                
                # Using GET instead of HEAD often yields more accurate results for APIs
                response = self.stealth.get(full_url)
                
                status = response.status_code
                size = len(response.content)
                
                if status == 200:
                    self.log(f"OPEN (LEAK): {endpoint} [Size: {size}b]", "VULN")
                    self.vulnerable_endpoints.append({
                        "url": full_url,
                        "status": status,
                        "size": size,
                        "type": "OPEN_ACCESS"
                    })
                    
                    # DUAL FILE PROTOCOL IMPLEMENTATION
                    # 1. Save Original Content
                    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', endpoint)
                    loot_dir = os.path.join(self.output_dir, "Loot")
                    if not os.path.exists(loot_dir):
                        os.makedirs(loot_dir)
                        
                    raw_filename = os.path.join(loot_dir, f"{safe_name}_RAW.txt")
                    with open(raw_filename, 'wb') as f:
                        f.write(response.content)
                        
                    # 2. Save Human English Translation (Static Analysis)
                    analysis_filename = os.path.join(loot_dir, f"{safe_name}_ANALYSIS.md")
                    self.create_human_translation(analysis_filename, endpoint, response.content, response.headers)
                    
                elif status in [401, 403]:
                    self.log(f"SECURED: {endpoint}", "INFO")
                elif status in [301, 302]:
                    self.log(f"REDIRECT: {endpoint}", "INFO")
                else:
                    self.log(f"Status {status}: {endpoint}", "DEBUG")
                    
            except Exception as e:
                pass # Squelch errors during probing to keep output clean

    def create_human_translation(self, filename, endpoint, content, headers):
        """Generates a human-readable analysis of the leaked content."""
        try:
            text_content = content.decode('utf-8', errors='ignore')
            is_json = False
            json_keys = []
            
            # Check if JSON
            try:
                json_data = json.loads(text_content)
                is_json = True
                if isinstance(json_data, dict):
                    json_keys = list(json_data.keys())
                elif isinstance(json_data, list) and len(json_data) > 0 and isinstance(json_data[0], dict):
                    json_keys = list(json_data[0].keys())
            except:
                pass

            # Extract interesting strings (emails, URLs, keys)
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_content)
            urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text_content)
            potential_keys = re.findall(r'(?i)(key|token|secret|password)[\"\'\s]*[:=][\"\'\s]*([a-zA-Z0-9-_]{20,})', text_content)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Analysis Report: {endpoint}\n")
                f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Content-Type:** {headers.get('Content-Type', 'Unknown')}\n")
                f.write(f"**Size:** {len(content)} bytes\n\n")
                
                f.write("## 1. Executive Summary\n")
                if is_json:
                    f.write(f"The file contains structured JSON data. It appears to define **{len(json_keys)} top-level fields** including: `{', '.join(json_keys[:5])}`.\n")
                else:
                    f.write("The file contains unstructured text or binary data. It may be source code, HTML, or an encrypted blob.\n")
                    
                f.write("\n## 2. Key Findings (English Translation)\n")
                
                # Law 7: Source Code Discovery
                repo_links = re.findall(r'https?://(?:github\.com|gitlab\.com|bitbucket\.org)/[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+', text_content)
                if repo_links:
                     f.write(f"- **SOURCE CODE DETECTED:** {len(repo_links)} repositories found (Law 7 Violation).\n")
                     for r in repo_links[:5]:
                         f.write(f"  - {r}\n")
                
                # Law 9: Internal Comms
                comms_links = []
                comms_links.extend(re.findall(r'https://hooks\.slack\.com/services/[A-Z0-9]+/[A-Z0-9]+/[a-zA-Z0-9]+', text_content))
                comms_links.extend(re.findall(r'(?:https?://)?(?:www\.)?(?:discord\.gg|discord\.com/invite)/[a-zA-Z0-9]+', text_content))
                if comms_links:
                     f.write(f"- **INTERNAL COMMS LEAKED:** {len(comms_links)} channels found (Law 9 Violation).\n")
                     for c in comms_links[:5]:
                         f.write(f"  - {c}\n")

                if emails:
                    f.write(f"- **Contacts Found:** {len(emails)} email addresses identified (e.g., {emails[0]}).\n")
                if urls:
                    f.write(f"- **External Links:** {len(urls)} URLs found (e.g., {urls[0]}).\n")
                if potential_keys:
                    f.write(f"- **Secrets Detected:** {len(potential_keys)} potential API keys or tokens found.\n")
                    
                f.write("\n## 3. Data Structure / Schema\n")
                if is_json:
                    f.write("```json\n")
                    # Write a small sample of the structure
                    if isinstance(json_data, dict):
                        f.write(json.dumps({k: str(type(v).__name__) for k, v in json_data.items()}, indent=2))
                    elif isinstance(json_data, list):
                        f.write("Array of Objects: \n")
                        if len(json_data) > 0:
                            f.write(json.dumps({k: str(type(v).__name__) for k, v in json_data[0].items()}, indent=2))
                    f.write("\n```\n")
                else:
                    f.write("No JSON structure detected.\n")

                f.write("\n## 4. Raw Preview (First 500 chars)\n")
                f.write("```\n")
                f.write(text_content[:500])
                f.write("\n```\n")
                
        except Exception as e:
            with open(filename, 'w') as f:
                f.write(f"Analysis Failed: {str(e)}")

    def generate_report(self):
        report_file = os.path.join(self.output_dir, f"Raziel_Report_{self.domain}.json")
        
        data = {
            "target": self.target_url,
            "scan_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": {
                "js_bundles_scanned": len(self.js_files),
                "endpoints_discovered": len(self.discovered_endpoints),
                "vulnerable_endpoints": len(self.vulnerable_endpoints)
            },
            "vulnerabilities": self.vulnerable_endpoints,
            "all_endpoints": list(self.discovered_endpoints)
        }
        
        with open(report_file, 'w') as f:
            json.dump(data, f, indent=4)
            
        self.log(f"Report saved to {report_file}", "SUCCESS")

    def run(self):
        self.crawl_js_bundles()
        self.analyze_bundles()
        if self.discovered_endpoints:
            self.active_probe()
        self.generate_report()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Raziel API Siphon")
    parser.add_argument("--url", help="Target URL", required=True)
    args = parser.parse_args()
    
    raziel = Raziel_API_Siphon(args.url)
    raziel.run()
