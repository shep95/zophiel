import re
import os
import subprocess
import sys

# Ensure we can import HiveMind
sys.path.append(os.path.join(os.path.dirname(__file__), "HiveMind"))
try:
    from HiveMind import HiveMind
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from HiveMind.HiveMind import HiveMind

class LocalHeaderHunt:
    def __init__(self):
        self.mind = HiveMind()
        self.source_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Intelligence_Database", "OpenAI", "Backend_Code", "Source_HTML", "chatgpt_source.html")
        self.js_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Intelligence_Database", "OpenAI", "Backend_Code", "Frontend_JS_Bundles")
        self.base_url = "https://chatgpt.com"
        
    def extract_links(self):
        if not os.path.exists(self.source_file):
            print("[-] Source file not found.")
            return []
            
        with open(self.source_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Regex for _next/static JS
        # src="/_next/static/chunks/2f043653-b09e0337f7481358.js"
        pattern = r'src="(/_next/static/chunks/[^"]+\.js)"'
        matches = re.findall(pattern, content)
        
        # OpenAI Custom CDN Assets
        # /cdn/assets/93527649-d6uunnbv2hve0bim.js
        pattern_cdn = r'["\'](/cdn/assets/[^"\']+\.js)["\']'
        matches += re.findall(pattern_cdn, content)
        
        # Also build manifest
        pattern_build = r'src="(/_next/static/[^"]+\/_buildManifest\.js)"'
        matches += re.findall(pattern_build, content)
        
        # Also ssg manifest
        pattern_ssg = r'src="(/_next/static/[^"]+\/_ssgManifest\.js)"'
        matches += re.findall(pattern_ssg, content)
        
        unique_links = list(set(matches))
        print(f"[*] Found {len(unique_links)} JS bundles in local source.")
        return unique_links

    def fetch_js_curl(self, relative_path):
        url = self.base_url + relative_path
        filename = relative_path.split("/")[-1]
        local_path = os.path.join(self.js_dir, filename)
        
        if not os.path.exists(self.js_dir):
            os.makedirs(self.js_dir)
            
        print(f"[*] Fetching {filename} via curl...")
        
        # Use the successful curl invocation
        cmd = [
            "curl.exe",
            "--ssl-no-revoke",
            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "-o", local_path,
            url
        ]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return local_path
        except subprocess.CalledProcessError:
            print(f"[-] Failed to download {url}")
            return None

    def scan_file(self, file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # Headers - Broad Search
        # Look for "X-..." or 'X-...'
        header_pattern = r'["\'](X-[a-zA-Z0-9-]+)["\']'
        headers = re.findall(header_pattern, content)
        
        # Secret Keys (sk-proj, etc)
        # sk-[a-zA-Z0-9]{20,}
        key_pattern = r'["\'](sk-[a-zA-Z0-9-_]{20,})["\']'
        keys = re.findall(key_pattern, content)
        
        # OAI- headers specifically
        oai_pattern = r'["\'](OAI-[a-zA-Z0-9-]+)["\']'
        oai_headers = re.findall(oai_pattern, content)

        found_items = []
        found_items.extend(headers)
        found_items.extend(keys)
        found_items.extend(oai_headers)
        
        for item in found_items:
            print(f"    [!] FOUND ARTIFACT: {item}")
            
        return found_items

    def run(self):
        print("=== Zohar Phase 11: Local Header Extraction ===")
        links = self.extract_links()
        
        all_headers = set()
        
        for link in links:
            path = self.fetch_js_curl(link)
            if path:
                found = self.scan_file(path)
                for h in found:
                    all_headers.add(h)
                    
        print("\n=== AGGREGATED HEADERS ===")
        for h in all_headers:
            print(f"- {h}")
            
        # Update Brain
        if all_headers:
            print("[*] Updating HiveMind with new headers...")
            arsenal = self.mind.get_arsenal()
            # Just dump them into a new list for review
            arsenal["discovered_headers"] = list(all_headers)
            self.mind.save_brain()

if __name__ == "__main__":
    hunt = LocalHeaderHunt()
    hunt.run()
