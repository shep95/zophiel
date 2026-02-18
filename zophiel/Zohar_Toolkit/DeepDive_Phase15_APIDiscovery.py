import os
import re
import sys
import json

# Ensure Zohar_Toolkit is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HiveMind.HiveMind import HiveMind

class Phase15_APIDiscovery:
    def __init__(self):
        self.js_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Intelligence_Database", "OpenAI", "Backend_Code", "Frontend_JS_Bundles")
        self.brain = HiveMind()
        self.api_endpoints = set()

    def scan(self):
        print(f"[*] Scanning {self.js_dir} for API endpoints...")
        
        if not os.path.exists(self.js_dir):
            print(f"[!] Error: {self.js_dir} does not exist!")
            return

        files = [f for f in os.listdir(self.js_dir) if f.endswith('.js')]
        print(f"[*] Found {len(files)} JS files to scan.")
        
        # Regex for API paths
        # Looking for strings that look like /backend-api/..., /public-api/..., or /v1/...
        api_pattern = r'["\'](/backend-api/[a-zA-Z0-9-_/]+|/public-api/[a-zA-Z0-9-_/]+|/v1/[a-zA-Z0-9-_/]+)["\']'
        
        # Regex for deep-research specifically
        dr_pattern = r'["\'](/[a-zA-Z0-9-_/]*deep-research[a-zA-Z0-9-_/]*)["\']'

        for file in files:
            path = os.path.join(self.js_dir, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Find general APIs
                    matches = re.findall(api_pattern, content)
                    for m in matches:
                        self.api_endpoints.add(m)
                        
                    # Find DR specific
                    dr_matches = re.findall(dr_pattern, content)
                    for m in dr_matches:
                        self.api_endpoints.add(m)
                        
            except Exception as e:
                print(f"[!] Error reading {file}: {e}")

        self.report()

    def report(self):
        print(f"\n[+] Found {len(self.api_endpoints)} unique API endpoints.")
        
        dr_endpoints = [e for e in self.api_endpoints if "deep-research" in e]
        
        if dr_endpoints:
            print(f"\n[!] DEEP RESEARCH ENDPOINTS FOUND:")
            for e in dr_endpoints:
                print(f"  - {e}")
                # Add to brain
                self.brain.add_target(f"https://chatgpt.com{e}", "Deep Research API Endpoint")
        else:
            print("\n[-] No specific 'deep-research' API endpoints found in regex scan.")

        # Save all to a file for review
        with open("Intelligence_Database/OpenAI/Backend_Code/discovered_api_endpoints.txt", "w") as f:
            for e in sorted(self.api_endpoints):
                f.write(e + "\n")
                
        print("\n[*] Saved full list to Intelligence_Database/OpenAI/Backend_Code/discovered_api_endpoints.txt")

if __name__ == "__main__":
    scanner = Phase15_APIDiscovery()
    scanner.scan()
