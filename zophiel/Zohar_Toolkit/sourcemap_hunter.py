import requests
import re
import os
import sys
from urllib.parse import urljoin, urlparse
from data_models import Finding, FindingType
from enum import Enum
import json

import logging

# Disable warnings
import urllib3
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Finding):
            from dataclasses import asdict
            return asdict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

parser = argparse.ArgumentParser(description="Hunt for source maps.")
parser.add_argument("--report", default=os.path.join(os.path.dirname(__file__), "..", "..", "osint_links", "Intelligence_Database", "X_Corp", "Reports", "INTELLIGENCE_REPORT_X_CORP.md"), help="Path to the intelligence report.")
parser.add_argument("--output", default=os.path.join("output", "sourcemaps"), help="Directory to save the source maps.")
args = parser.parse_args()

def load_alive_targets():
    report_path = args.report
    if not os.path.exists(report_path):
        return []
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"- \*\*(https?://[a-zA-Z0-9.\-]+)\*\* \[[0-9]+\]"
    return list(set(re.findall(pattern, content)))

def hunt():
    targets = load_alive_targets()
    print(f"[*] Hunting Source Maps on {len(targets)} targets...")
    
    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    found_maps = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for i, url in enumerate(targets):
        print(f"[{i+1}/{len(targets)}] Probing {url}...")
        try:
            resp = requests.get(url, headers=headers, verify=False, timeout=5)
            if resp.status_code != 200:
                continue
                
            # Extract JS
            scripts = re.findall(r'src=["\'](.*?.js)["\']', resp.text)
            
            for script in scripts:
                # Normalize URL
                if script.startswith("//"):
                    full_js_url = "https:" + script
                elif script.startswith("/"):
                    full_js_url = urljoin(url, script)
                elif not script.startswith("http"):
                    full_js_url = urljoin(url, script)
                else:
                    full_js_url = script
                    
                # Construct Map URL
                map_url = full_js_url + ".map"
                
                # Check for map
                try:
                    map_resp = requests.head(map_url, headers=headers, verify=False, timeout=3)
                    if map_resp.status_code == 200:
                        print(f"  [+] FOUND MAP: {map_url}")
                        finding = Finding(
                            value=map_url,
                            type=FindingType.ENDPOINT,
                            source_module="sourcemap_hunter",
                            target=url,
                            confidence=1.0,
                            metadata={"js_source": full_js_url}
                        )
                        found_maps.append(finding)
                        
                        # Download it
                        filename = map_url.split("/")[-1]
                        # prevent path traversal/long names
                        safe_name = re.sub(r'[^a-zA-Z0-9\-\.]', '_', filename)
                        if len(safe_name) > 50: safe_name = safe_name[-50:]
                        
                        with open(os.path.join(output_dir, safe_name), "wb") as f:
                            # Stream download
                            r = requests.get(map_url, stream=True, verify=False)
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk: f.write(chunk)
                except Exception as e:
                    logging.warning(f"  [!] Error checking for map {map_url}: {e}")
                    
        except Exception as e:
            logging.error(f"  [x] Error probing {url}: {e}")

    # Save findings
    with open(os.path.join(output_dir, "found_maps.json"), "w") as f:
        json.dump(found_maps, f, indent=2, cls=EnhancedJSONEncoder)

    if found_maps:
        print(f"\n[!] SUCCESS: Found {len(found_maps)} Source Maps!")
        print(f"[*] Saved to {output_dir}")
    else:
        print("\n[-] No Source Maps found exposed publicly.")

if __name__ == "__main__":
    hunt()
