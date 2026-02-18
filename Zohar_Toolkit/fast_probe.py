import json
import requests
import concurrent.futures
import os
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def load_subdomains():
    path = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\ORACLE_KNOWLEDGE_BASE.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    subs = []
    if "domains" in data:
        for domain, info in data["domains"].items():
            if "subdomains" in info:
                subs.extend(info["subdomains"])
                
    return list(set(subs))

def probe(domain):
    # Try HTTPS then HTTP
    urls = [f"https://{domain}", f"http://{domain}"]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=3, verify=False)
            if resp.status_code in [200, 301, 302, 401, 403]:
                return url
        except:
            pass
    return None

def run():
    subdomains = load_subdomains()
    print(f"[*] Loaded {len(subdomains)} subdomains from Oracle.")
    print(f"[*] Probing for ALIVE hosts (50 threads)...")
    
    alive = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_domain = {executor.submit(probe, d): d for d in subdomains}
        for future in concurrent.futures.as_completed(future_to_domain):
            result = future.result()
            if result:
                print(f"  [+] ALIVE: {result}")
                alive.append(result)
                
    print(f"\n[*] Total Alive: {len(alive)}")
    
    # Save
    with open("alive_recovered.json", "w") as f:
        json.dump(alive, f, indent=2)
        
    return alive

if __name__ == "__main__":
    run()
