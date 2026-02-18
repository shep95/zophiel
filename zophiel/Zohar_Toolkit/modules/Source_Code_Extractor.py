import os
import re
import sys
import json
import time
import requests
import jsbeautifier
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Ensure Zohar_Toolkit root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.Stealth_Manager import StealthSession

class Source_Code_Extractor:
    """
    RAZIEL MODULE: SOURCE CODE EXTRACTOR
    A specialized tool to download, beautify, and analyze JS bundles.
    It attempts to reconstruct the original source code logic from minified bundles.
    """
    
    def __init__(self, target_url, output_dir="Intelligence_Database/Notion/Source_Code"):
        self.target_url = target_url
        self.domain = urlparse(target_url).netloc
        
        # Robustly locate proxies.txt
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        proxy_path = os.path.join(base_dir, "proxies.txt")
        if not os.path.exists(proxy_path):
             proxy_path = "proxies.txt"
             
        self.stealth = StealthSession(proxy_file=proxy_path)
        self.output_dir = output_dir
        self.js_files = set()
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def log(self, message, level="INFO"):
        print(f"[{level}] {message}")

    def crawl_js_bundles(self):
        """Fetches the main page and extracts JS bundle URLs."""
        self.log(f"Initiating Source Extraction on {self.target_url}...", "RAZIEL")
        try:
            response = self.stealth.session.get(self.target_url, timeout=10)
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
            
            self.log(f"Identified {len(self.js_files)} unique JS bundles for extraction.", "INFO")
            
        except Exception as e:
            self.log(f"Crawl failed: {e}", "ERROR")

    def download_and_beautify(self):
        """Downloads each JS bundle and beautifies it."""
        self.log("Beginning Download & Beautification Protocol...", "RAZIEL")
        
        for js_url in self.js_files:
            try:
                filename = js_url.split('/')[-1]
                # Sanitize filename
                filename = re.sub(r'[^\w\-_\.]', '_', filename)
                if not filename.endswith(".js"):
                    filename += ".js"
                
                self.log(f"Extracting: {filename}", "DOWNLOAD")
                
                # Check for Source Map first (The Holy Grail)
                map_url = js_url + ".map"
                map_response = self.stealth.session.get(map_url, timeout=5)
                
                has_map = False
                if map_response.status_code == 200:
                    self.log(f"  [!] SOURCE MAP FOUND: {filename}.map", "CRITICAL")
                    map_path = os.path.join(self.output_dir, filename + ".map")
                    with open(map_path, "w", encoding="utf-8") as f:
                        f.write(map_response.text)
                    has_map = True
                
                # Download JS
                response = self.stealth.session.get(js_url, timeout=10)
                if response.status_code == 200:
                    raw_content = response.text
                    
                    # Beautify
                    self.log(f"  [-] Beautifying...", "PROCESS")
                    beautified_code = jsbeautifier.beautify(raw_content)
                    
                    # Save Beautified
                    save_path = os.path.join(self.output_dir, "beautified_" + filename)
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(f"// SOURCE: {js_url}\n")
                        f.write(f"// EXTRACTED: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        if has_map:
                            f.write(f"// NOTE: Source Map was also recovered.\n")
                        f.write("\n" + beautified_code)
                    
                    self.log(f"  [+] Saved to {save_path}", "SUCCESS")
                    
            except Exception as e:
                self.log(f"Failed to process {js_url}: {e}", "ERROR")

    def run(self):
        self.crawl_js_bundles()
        self.download_and_beautify()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Raziel Source Code Extractor")
    parser.add_argument("--url", help="Target URL", required=True)
    args = parser.parse_args()
    
    extractor = Source_Code_Extractor(args.url)
    extractor.run()
