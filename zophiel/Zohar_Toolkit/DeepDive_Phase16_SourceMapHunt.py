import os
import re
import sys
import subprocess
import time

# Ensure Zohar_Toolkit is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HiveMind.HiveMind import HiveMind

class Phase16_SourceMapHunt:
    def __init__(self):
        self.brain = HiveMind()
        self.html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Intelligence_Database", "OpenAI", "Backend_Code", "Source_HTML", "chatgpt_source.html")
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Intelligence_Database", "OpenAI", "Backend_Code", "Source_Maps")
        self.base_url = "https://chatgpt.com" # Or cdn.openai.com, we will see from the source
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def extract_js_urls(self):
        if not os.path.exists(self.html_path):
            print(f"[!] Source HTML not found at {self.html_path}")
            return []

        with open(self.html_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Regex to find .js files
        # Updated Pattern: src="/cdn/assets/..." or similar
        pattern = r'src="(/cdn/assets/[^"]+\.js)"'
        matches = re.findall(pattern, content)
        
        # Also check for import * as ... from "..."
        import_pattern = r'from "(/cdn/assets/[^"]+\.js)"'
        matches.extend(re.findall(import_pattern, content))
        
        # And dynamic imports import("...")
        dyn_pattern = r'import\("(/cdn/assets/[^"]+\.js)"\)'
        matches.extend(re.findall(dyn_pattern, content))

        return list(set(matches)) # Deduplicate

    def download_map(self, relative_path):
        # Construct .map URL
        # If relative_path is /_next/static/chunks/main-123.js
        # Map is /_next/static/chunks/main-123.js.map
        
        map_url = f"{self.base_url}{relative_path}.map"
        filename = os.path.basename(relative_path) + ".map"
        output_path = os.path.join(self.output_dir, filename)
        
        print(f"[*] Probing {map_url} ...", end="\r")
        
        # Use curl to avoid python blocking
        cmd = [
            "curl", "-s", "-k", "--ssl-no-revoke",
            "-o", output_path,
            "-w", "%{http_code}",
            map_url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            status_code = result.stdout.strip()
            
            if status_code == "200":
                # Check if it's actually a map file (sometimes they return 200 with HTML)
                with open(output_path, 'r', errors='ignore') as f:
                    head = f.read(100)
                    if "version" in head and "sources" in head:
                        print(f"\n[+] FOUND SOURCE MAP: {filename}")
                        self.brain.add_target(map_url, "Source Map Exposure (Source Code Leak)")
                        return True
                    else:
                        # False positive
                        os.remove(output_path)
                        return False
            else:
                # Cleanup empty file if curl created it
                if os.path.exists(output_path):
                    os.remove(output_path)
                return False
                
        except Exception as e:
            print(f"\n[!] Error: {e}")
            return False

    def run(self):
        print("[*] Starting Phase 16: Source Map Hunt...")
        urls = self.extract_js_urls()
        print(f"[*] Found {len(urls)} JS references in source HTML.")
        
        found_count = 0
        for url in urls:
            if self.download_map(url):
                found_count += 1
            time.sleep(0.2) # Polite delay
            
        print(f"\n[*] Hunt Complete. Found {found_count} valid .map files.")
        if found_count > 0:
            print("[!] CRITICAL: Source Maps exposed. This allows full reconstruction of frontend source code.")
            print(f"    Files saved to: {self.output_dir}")
        else:
            print("[-] No source maps found (likely disabled in production build).")

if __name__ == "__main__":
    hunter = Phase16_SourceMapHunt()
    hunter.run()
