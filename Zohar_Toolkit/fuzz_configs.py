import json
import requests
import concurrent.futures
import os
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def load_targets():
    path = "alive_recovered.json"
    if not os.path.exists(path):
        return []
        
    with open(path, "r") as f:
        urls = json.load(f)
        
    # Filter for X/Twitter
    targets = [u for u in urls if "x.com" in u or "twitter.com" in u]
    return list(set(targets))

def fuzz(url):
    paths = [
        "/.env",
        "/.git/HEAD",
        "/config.js",
        "/robots.txt",
        "/sitemap.xml",
        "/actuator/env",
        "/server-status",
        "/.ds_store"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    findings = {}
    
    for p in paths:
        target = url.rstrip("/") + p
        try:
            resp = requests.get(target, headers=headers, timeout=3, verify=False, allow_redirects=False)
            
            # Criteria for "Found"
            if resp.status_code == 200:
                # False positive check for .env (sometimes returns HTML)
                if p == "/.env" and "<html" in resp.text.lower():
                    continue
                if p == "/.git/HEAD" and "refs/heads" not in resp.text:
                    continue
                    
                print(f"  [!] FOUND: {target} [{len(resp.content)} bytes]")
                findings[p] = target
                
        except:
            pass
            
    return url, findings

def run():
    targets = load_targets()
    print(f"[*] Fuzzing {len(targets)} X Corp targets for sensitive files...")
    
    all_findings = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_url = {executor.submit(fuzz, url): url for url in targets}
        for future in concurrent.futures.as_completed(future_to_url):
            url, results = future.result()
            if results:
                all_findings[url] = results

    # Save findings
    output_path = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\X_Corp\Reports\CONFIG_FUZZ_FINDINGS.json"
    with open(output_path, "w") as f:
        json.dump(all_findings, f, indent=2)
        
    print(f"\n[*] Fuzzing Complete. Findings saved to {output_path}")
    
    # Print Summary
    print("\n--- SUMMARY OF EXPOSED FILES ---")
    for url, files in all_findings.items():
        for ftype, link in files.items():
            print(f"{ftype}: {link}")

if __name__ == "__main__":
    run()
