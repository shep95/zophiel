import json
import requests
import os
import sys
import re

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from Oculus import Oculus

# Configuration
TARGET_TOKEN = "eYjN4xNLgOM0w5re.CutMbyYAEjFyki.O2sTwhRwydecdmZ9"
OUTPUT_REPORT = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\OpenAI\Reports\DEEP_DIVE_PHASE2.md"

TARGETS = [
    "https://dev.admin.unified-6.api.openai.com",
    "https://openai-team.forum.openai.com"
]

def validate_token_aggressive(token):
    print(f"\n[!] AGGRESSIVE TOKEN VALIDATION: {token}")
    
    # Expanded list of endpoints, including internal-sounding ones
    endpoints = [
        "https://api.openai.com/v1/models",
        "https://api.openai.com/v1/engines",
        "https://api.openai.com/dashboard/billing/usage",
        "https://api.openai.com/v1/me",
        "https://api.openai.com/v1/organizations",
        # Try probing the unified shard directly with the token
        "https://api.unified-6.api.openai.com/v1/models", 
        "https://dev.admin.unified-6.api.openai.com/health"
    ]
    
    headers_variations = [
        {"Authorization": f"Bearer {token}"},
        {"Authorization": f"Bearer {token}", "OpenAI-Organization": "org-internal"},
        {"X-OpenAI-Internal-Token": token} # Guessing internal headers
    ]
    
    results = []
    
    for url in endpoints:
        for headers in headers_variations:
            try:
                # Short timeout
                resp = requests.get(url, headers=headers, timeout=5, verify=False)
                
                status = resp.status_code
                print(f"  {url} | {list(headers.keys())[0]} -> [{status}]")
                
                if status == 200:
                    results.append(f"SUCCESS: {url} with headers {headers}")
                    try:
                        results.append(f"  DATA: {str(resp.json())[:200]}")
                    except:
                        results.append(f"  DATA: {resp.text[:200]}")
                elif status in [401, 403]:
                    # Don't log every failure, just significant ones
                    pass
                else:
                    results.append(f"INTERESTING: {url} -> {status}")
                    
            except Exception as e:
                pass
                
    if not results:
        results.append("Token failed all aggressive validation checks (401/403/ConnectionError).")
        
    return results

def surgical_scan(targets):
    print(f"\n[!] SURGICAL SCANNING TARGETS")
    all_findings = {}
    
    for url in targets:
        print(f"Targeting: {url}")
        try:
            oculus = Oculus(url)
            # Oculus.gaze() returns findings dict
            findings = oculus.gaze()
            
            # Additional custom scraping for Forum specific things
            try:
                resp = requests.get(url, verify=False, timeout=10)
                if resp.status_code == 200:
                    # Look for emails specifically in the raw text again just in case
                    emails = re.findall(r"[a-zA-Z0-9._%+-]+@openai\.com", resp.text)
                    if emails:
                        if 'emails' not in findings: findings['emails'] = []
                        findings['emails'].extend(emails)
                        
                    # Look for names (simple heuristic: Capitalized words near "Author" or "By")
                    # This is noisy, so let's just dump the title
                    if "<title>" in resp.text:
                        title = resp.text.split("<title>")[1].split("</title>")[0]
                        findings['page_title'] = [title]
            except:
                pass

            if findings:
                all_findings[url] = findings
        except Exception as e:
            print(f"Failed to scan {url}: {e}")
            
    return all_findings

def generate_phase2_report(token_results, scan_findings):
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("# PHASE 2 INTELLIGENCE: SPECIFIC TARGETS\n\n")
        
        f.write("## 1. AGGRESSIVE TOKEN VALIDATION\n")
        f.write(f"Token: `{TARGET_TOKEN}`\n")
        for res in token_results:
            f.write(f"- {res}\n")
            
        f.write("\n## 2. TARGET RECONNAISSANCE\n")
        
        for url, findings in scan_findings.items():
            f.write(f"\n### Target: {url}\n")
            
            # Check if empty
            if not any(findings.values()):
                f.write("  - No significant findings (WAF or empty response).\n")
                continue
                
            for key, values in findings.items():
                if values:
                    f.write(f"- **{key.upper()}**:\n")
                    unique_vals = list(set(values))
                    for v in unique_vals[:20]: # Limit to 20 items per category to avoid bloat
                        f.write(f"  - `{v}`\n")
                    if len(unique_vals) > 20:
                        f.write(f"  - ... ({len(unique_vals)-20} more)\n")

    print(f"\n[+] Phase 2 Report generated at {OUTPUT_REPORT}")

if __name__ == "__main__":
    # 1. Validate
    token_results = validate_token_aggressive(TARGET_TOKEN)
    
    # 2. Scan
    scan_findings = surgical_scan(TARGETS)
    
    # 3. Report
    generate_phase2_report(token_results, scan_findings)
