import os
import re
import json
import requests
import subprocess
from urllib.parse import urljoin

class Phase19_SecretMiner:
    def __init__(self):
        self.base_dir = os.path.join("Intelligence_Database", "OpenAI", "Bug_Bounty")
        self.artifacts_dir = os.path.join(self.base_dir, "Leaked_Assets")
        self.landing_page = os.path.join(self.base_dir, "DeepResearch_Landing.html")
        os.makedirs(self.artifacts_dir, exist_ok=True)
        
        # Regex patterns for high-value secrets
        self.patterns = {
            "api_key": r'(sk-[a-zA-Z0-9]{20,})',
            "internal_url": r'(https?://[a-zA-Z0-9.-]*internal[a-zA-Z0-9.-]*)',
            "backend_api": r'(/backend-api/[a-zA-Z0-9/_.-]+)',
            "feature_gate": r'([a-zA-Z0-9_-]*gate[a-zA-Z0-9_-]*)',
            "jwt": r'(eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,})',
            "email": r'([a-zA-Z0-9._%+-]+@openai\.com)',
            "sso_url": r'(https?://sso\.[a-zA-Z0-9.-]+)'
        }

    def download_asset(self, url):
        filename = url.split("/")[-1]
        filepath = os.path.join(self.artifacts_dir, filename)
        
        if os.path.exists(filepath):
            print(f"[*] Skipping {filename} (already exists)")
            return filepath
            
        print(f"[*] Downloading {url}...")
        try:
            # Use curl to bypass WAF if needed
            cmd = [
                "curl", "-s", "-L", "--ssl-no-revoke",
                "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "-o", filepath,
                url
            ]
            subprocess.run(cmd, check=True)
            return filepath
        except Exception as e:
            print(f"[!] Failed to download {url}: {e}")
            return None

    def scan_file(self, filepath):
        print(f"[*] Scanning {os.path.basename(filepath)} for secrets...")
        findings = {}
        
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            for key, pattern in self.patterns.items():
                matches = re.findall(pattern, content)
                if matches:
                    findings[key] = list(set(matches))
                    
            return findings
        except Exception as e:
            print(f"[!] Error scanning file: {e}")
            return {}

    def parse_landing_page(self):
        print("[*] Parsing DeepResearch_Landing.html for assets...")
        assets = []
        
        if not os.path.exists(self.landing_page):
            print("[!] Landing page not found. Run Phase 18 first.")
            return []
            
        with open(self.landing_page, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract JS URLs
        # 1. src="/cdn/assets/..."
        # 2. from "/cdn/assets/..."
        # 3. import("/cdn/assets/...")
        
        matches = re.findall(r'["\'](/cdn/assets/[^"\']+\.js)["\']', content)
        for m in matches:
            full_url = f"https://chatgpt.com{m}"
            assets.append(full_url)
            
        return list(set(assets))

    def generate_report(self, all_findings):
        report_path = os.path.join(self.base_dir, "Secrets_Report.md")
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Phase 19: Deep Research Secrets Report\n\n")
            f.write("**Status:** Automated Scan Complete\n")
            f.write("**Target:** Leaked JS Bundles from /features/deep-research/\n\n")
            
            for filename, findings in all_findings.items():
                f.write(f"## File: {filename}\n")
                if not findings:
                    f.write("*No secrets found matching patterns.*\n\n")
                    continue
                    
                for category, items in findings.items():
                    f.write(f"### {category.replace('_', ' ').title()}\n")
                    for item in items:
                        f.write(f"- `{item}`\n")
                    f.write("\n")
                    
        print(f"[*] Report generated at {report_path}")

    def check_source_maps(self, assets):
        print("[*] Checking for Source Maps (.map)...")
        found_maps = []
        
        for url in assets:
            map_url = f"{url}.map"
            print(f"[*] Probing {map_url}...")
            
            cmd = [
                "curl", "-s", "-I", "-L", "--ssl-no-revoke",
                "-H", "User-Agent: Mozilla/5.0",
                map_url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if "200 OK" in result.stdout:
                print(f"[+] FOUND SOURCE MAP: {map_url}")
                found_maps.append(map_url)
            else:
                pass # Silent on failure
                
        return found_maps

    def run(self):
        assets = self.parse_landing_page()
        print(f"[*] Found {len(assets)} assets to scan.")
        
        all_findings = {}
        
        # 1. Download and Scan Assets
        for url in assets:
            filepath = self.download_asset(url)
            if filepath:
                findings = self.scan_file(filepath)
                if findings:
                    all_findings[os.path.basename(filepath)] = findings
                    
        # 2. Check Source Maps
        maps = self.check_source_maps(assets)
        if maps:
            all_findings["Source_Maps"] = {"exposed_maps": maps}
            
        # 3. Generate Report
        self.generate_report(all_findings)

if __name__ == "__main__":
    miner = Phase19_SecretMiner()
    miner.run()
