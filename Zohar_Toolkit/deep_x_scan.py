import os
import re
import json
import sys

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from Oculus import Oculus

def load_alive_targets():
    report_path = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\X_Corp\Reports\INTELLIGENCE_REPORT_X_CORP.md"
    if not os.path.exists(report_path):
        print(f"[!] Report not found at {report_path}")
        return []
        
    print(f"[*] Parsing targets from {report_path}...")
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract URLs from the list items
    # Format: - **https://url** [200]
    pattern = r"- \*\*(https?://[a-zA-Z0-9.\-]+)\*\* \[[0-9]+\]"
    targets = re.findall(pattern, content)
    
    # Filter out 404s if the report included them (though the section header says Alive)
    # The regex matches the format in the "Alive Endpoints" section.
    
    print(f"[*] Loaded {len(targets)} alive targets.")
    return list(set(targets))

def deep_scan():
    targets = load_alive_targets()
    
    all_findings = {}
    
    print(f"\n[*] Starting Deep Oculus Scan on {len(targets)} targets...")
    print("[*] Mode: AGGRESSIVE (New Regex + Full Script Download)\n")
    
    for i, url in enumerate(targets):
        print(f"[{i+1}/{len(targets)}] Gazing at: {url}")
        try:
            oculus = Oculus(url)
            findings = oculus.gaze()
            
            if findings:
                # Filter out empty lists
                valid_findings = {k: v for k, v in findings.items() if v}
                if valid_findings:
                    all_findings[url] = valid_findings
                    print(f"  [!!!] HITS FOUND: {list(valid_findings.keys())}")
                    
        except KeyboardInterrupt:
            print("\n[!] Scan interrupted by user.")
            break
        except Exception as e:
            print(f"  [x] Error: {e}")
            
    # Save results
    output_path = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\X_Corp\Reports\DEEP_SCAN_FINDINGS.json"
    with open(output_path, "w") as f:
        json.dump(all_findings, f, indent=2)
        
    print(f"\n[*] Deep Scan Complete. Results saved to {output_path}")
    
    # Print Summary
    count = sum(len(v) for v in all_findings.values())
    if count > 0:
        print(f"\n[!] TOTAL VULNERABILITIES/SECRETS FOUND: {count}")
        for url, data in all_findings.items():
            print(f"\n--- {url} ---")
            for k, v in data.items():
                print(f"  {k}: {len(v)} items")
                # Print first 3 items as preview
                for item in v[:3]:
                    print(f"    - {item[:100]}...")
    else:
        print("\n[-] No sensitive secrets found with enhanced patterns.")

if __name__ == "__main__":
    deep_scan()
