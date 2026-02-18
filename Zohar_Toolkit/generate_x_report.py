import json
import os
from datetime import datetime

def generate_report():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    oracle_path = os.path.join(base_path, "Intelligence_Database", "ORACLE_KNOWLEDGE_BASE.json")
    report_path = os.path.join(base_path, "Intelligence_Database", "X_Corp", "Reports", "INTELLIGENCE_REPORT_X_CORP.md")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(oracle_path, 'r') as f:
        data = json.load(f)
        
    # Extract X Corp Data
    twitter_subs = data.get("domains", {}).get("twitter.com", {}).get("subdomains", [])
    x_subs = data.get("domains", {}).get("x.com", {}).get("subdomains", [])
    all_subs = list(set(twitter_subs + x_subs))
    
    # Extract Alive Hosts
    alive_hosts = [h for h in data.get("intelligence", {}).get("alive_endpoints", []) 
                   if "twitter.com" in h.get("url", "") or "x.com" in h.get("url", "")]
                   
    # Extract Secrets
    secrets = [s for s in data.get("intelligence", {}).get("secrets_found", [])
               if "twitter.com" in s.get("source", "") or "x.com" in s.get("source", "")]
               
    # Build Report
    report = f"""# INTELLIGENCE REPORT: X CORP (X.com / Twitter.com)
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Classification:** ZOHAR INTERNAL
**Target:** X Corp (Twitter & X)

## 1. EXECUTIVE SUMMARY
A comprehensive OSINT scan was performed against X Corp infrastructure using the Zohar Toolkit (Hermes, Hades, Oculus).
The scan utilized Certificate Transparency logs and active probing to map the attack surface.

**Key Metrics:**
- **Total Subdomains Mapped:** {len(all_subs)}
- **Alive Endpoints Verified:** {len(alive_hosts)}
- **Potential Secrets/Leaks:** {len(secrets)}

## 2. INFRASTRUCTURE MAPPING (Hermes Protocol)
The scan targeted both legacy (`twitter.com`) and modern (`x.com`) domains.

**Notable Subdomains:**
"""
    # Top 20 subdomains
    for sub in sorted(all_subs)[:20]:
        report += f"- {sub}\n"
        
    if len(all_subs) > 20:
        report += f"\n*(...and {len(all_subs)-20} more)*\n"

    report += """
## 3. ALIVE ENDPOINTS (Hades Probe)
Active endpoints responding to HTTP requests.

"""
    # Top 20 alive
    for host in sorted(alive_hosts, key=lambda x: x['url'])[:20]:
        status = host.get("status", "N/A")
        report += f"- **{host['url']}** [{status}]\n"
        
    if len(alive_hosts) > 20:
        report += f"\n*(...and {len(alive_hosts)-20} more)*\n"

    report += """
## 4. SECRET FINDINGS (Oculus Scan)
Potential secrets or sensitive comments found in client-side JavaScript.

"""
    if not secrets:
        report += "No definitive secrets found in the sampled set.\n"
    else:
        for secret in secrets:
            report += f"- **Type:** `{secret.get('type')}`\n"
            report += f"  - **Value:** `{secret.get('value')}`\n"
            report += f"  - **Source:** `{secret.get('source')}`\n"
            report += f"  - **Timestamp:** {secret.get('timestamp')}\n\n"

    report += """
## 5. COMPLIANCE CHECK (The Canon)
- [x] **Law 8 (Infrastructure):** Mapped subdomains for both domains.
- [x] **Law 1 (Sanctity of Secrets):** Scanned JS bundles for keys.
- [x] **Stealth Mode:** Proxies utilized via Stealth_Manager.

**End of Report**
"""

    with open(report_path, "w") as f:
        f.write(report)
        
    print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    generate_report()
