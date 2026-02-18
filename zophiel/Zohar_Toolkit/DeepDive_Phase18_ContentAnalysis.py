import os
import requests
import re
import json
import sys

# Ensure HiveMind is accessible
sys.path.append(os.path.join(os.path.dirname(__file__), 'HiveMind'))
try:
    from HiveMind import HiveMind
except ImportError:
    # Fallback for different execution contexts
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'HiveMind'))
    from HiveMind import HiveMind

class Phase18_ContentAnalysis:
    def __init__(self):
        self.brain = HiveMind()
        self.target_url = "https://chatgpt.com/features/deep-research/"
        self.output_dir = os.path.join("Intelligence_Database", "OpenAI", "Bug_Bounty")
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_content(self):
        print(f"[*] Phase 18: Fetching content from {self.target_url} using curl (WAF Bypass)...")
        # Try base URL and known bypass params
        targets = [
            self.target_url,
            f"{self.target_url}?bypass=true",
            f"{self.target_url}?preview=true"
        ]
        
        import subprocess
        
        for url in targets:
            print(f"[*] Trying {url}...")
            try:
                # Construct curl command with realistic headers to bypass WAF
                cmd = [
                    "curl", "-s", "-L", "--ssl-no-revoke",
                    "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "-H", "Accept-Language: en-US,en;q=0.5",
                    url
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                
                if result.returncode == 0 and result.stdout:
                    # Check if we got a real page or a block page
                    if "<html" in result.stdout and "Just a moment" not in result.stdout:
                        print(f"[+] Success! Content fetched from {url}. Length: {len(result.stdout)} bytes.")
                        return result.stdout
                    else:
                        print(f"[-] Blocked or empty response from {url} (Cloudflare challenge?).")
            except Exception as e:
                print(f"[!] Error fetching content with curl: {e}")
                
        return None

    def analyze_content(self, html_content):
        print("[*] Analyzing content for sensitive data leaks...")
        
        findings = {
            "internal_codenames": [],
            "feature_flags": [],
            "js_bundles": [],
            "api_endpoints": [],
            "config_dumps": []
        }

        # 1. Search for Internal Codenames (Sahara, Deep Research, etc.)
        if "sahara" in html_content.lower():
            findings["internal_codenames"].append("sahara")
        if "deep research" in html_content.lower():
            findings["internal_codenames"].append("deep-research")

        # 2. Extract JS Bundles (Potential Source Code Leak)
        # Regex for <script src="...">
        src_scripts = re.findall(r'src="([^"]+\.js)"', html_content)
        
        # Regex for ES Module imports: import * as route1 from "/cdn/assets/..."
        import_scripts = re.findall(r'from\s+"(/cdn/assets/[^"]+\.js)"', html_content)
        
        # Regex for dynamic imports: import("/cdn/assets/...")
        dynamic_imports = re.findall(r'import\("(/cdn/assets/[^"]+\.js)"\)', html_content)
        
        all_scripts = list(set(src_scripts + import_scripts + dynamic_imports))
        
        for script in all_scripts:
            findings["js_bundles"].append(script)
            # Add to HiveMind for future processing
            self.brain.add_target(script, description="JS Bundle found in Deep Research Landing")

        # 3. Look for Remix/Next.js Context Dumps (Configuration Leaks)
        # Often found in window.__remixContext or similar
        remix_context = re.search(r'window\.__remixContext\s*=\s*({.*?});', html_content, re.DOTALL)
        if remix_context:
            print("[!] CRITICAL: Found window.__remixContext dump!")
            findings["config_dumps"].append("window.__remixContext")
            # Save the dump for deeper inspection
            dump_path = os.path.join(self.output_dir, "DeepResearch_Config_Dump.json")
            with open(dump_path, "w", encoding="utf-8") as f:
                f.write(remix_context.group(1))

        # 4. Save the raw HTML for the Bug Bounty Report
        html_path = os.path.join(self.output_dir, "DeepResearch_Landing.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return findings

    def generate_report_snippet(self, findings):
        report_path = os.path.join(self.output_dir, "Analysis_Log_Phase18.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== Phase 18: Content Analysis Findings ===\n")
            f.write(f"Target: {self.target_url}\n\n")
            
            f.write("[+] Internal Codenames Found:\n")
            for name in findings["internal_codenames"]:
                f.write(f" - {name}\n")
            
            f.write("\n[+] JS Bundles (Source Code Candidates):\n")
            for js in findings["js_bundles"]:
                f.write(f" - {js}\n")
            
            f.write("\n[+] Configuration/State Dumps:\n")
            for config in findings["config_dumps"]:
                f.write(f" - {config} (Saved to file)\n")

        print(f"[*] Analysis complete. Log saved to {report_path}")

    def run(self):
        content = self.fetch_content()
        if content:
            findings = self.analyze_content(content)
            self.generate_report_snippet(findings)

if __name__ == "__main__":
    scanner = Phase18_ContentAnalysis()
    scanner.run()
