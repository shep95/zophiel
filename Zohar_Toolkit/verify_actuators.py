import requests
import json
import urllib3
import concurrent.futures

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load the findings
with open(r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\X_Corp\Reports\CONFIG_FUZZ_FINDINGS.json", "r") as f:
    findings = json.load(f)

targets = []
for domain, paths in findings.items():
    if "/actuator/env" in paths:
        targets.append(paths["/actuator/env"])
    if "/server-status" in paths:
        targets.append(paths["/server-status"])

print(f"[*] Verifying {len(targets)} potential sensitive endpoints...")

valid_findings = []

def verify_target(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, verify=False, timeout=10)
        content_type = resp.headers.get("Content-Type", "").lower()
        
        # Check for Spring Boot Actuator
        if "actuator/env" in url:
            if "application/json" in content_type or "vnd.spring-boot" in content_type:
                # Double check if it looks like actuator data
                if "activeProfiles" in resp.text or "propertySources" in resp.text:
                    return f"[CRITICAL] Spring Boot Actuator Exposed: {url}"
                else:
                    return f"[Suspicious] JSON at {url} (Size: {len(resp.text)})"
            elif "json" in content_type:
                 return f"[Suspicious] JSON content at {url}"
            else:
                # Likely HTML false positive
                pass

        # Check for Server Status
        if "server-status" in url:
            if "Apache Server Status" in resp.text:
                return f"[HIGH] Apache Server Status Exposed: {url}"
            
    except Exception as e:
        pass
    return None

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(verify_target, url) for url in targets]
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            print(result)
            valid_findings.append(result)

if not valid_findings:
    print("[-] All actuator/status endpoints appear to be false positives (HTML/Redirects).")
else:
    print(f"[+] Found {len(valid_findings)} verified endpoints.")
