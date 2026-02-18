import requests
import re
import os
import json
from bs4 import BeautifulSoup
import warnings

# Suppress insecure request warnings
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

TARGET_URL = "https://openai-team.forum.openai.com"
OUTPUT_REPORT = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\OpenAI\Reports\DEEP_DIVE_PHASE3_FORUM.md"

def fetch_scripts(url):
    print(f"[+] Fetching scripts from {url}...")
    try:
        response = requests.get(url, verify=False, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = []
        
        # 1. External Scripts
        for script in soup.find_all('script'):
            if script.get('src'):
                src = script.get('src')
                if src.startswith('/'):
                    src = url + src
                elif not src.startswith('http'):
                    src = url + '/' + src
                scripts.append({"type": "external", "url": src, "content": None})
        
        # 2. Inline Scripts (often contain hydration data/JSON)
        for script in soup.find_all('script'):
            if not script.get('src') and script.string:
                scripts.append({"type": "inline", "url": "inline", "content": script.string})
                
        print(f"  Found {len(scripts)} scripts.")
        return scripts
    except Exception as e:
        print(f"  [!] Failed to fetch main page: {e}")
        return []

def analyze_script(script):
    findings = {
        "emails": [],
        "names": [],
        "usernames": [],
        "messages": [],
        "groups": [],
        "api_keys": []
    }
    
    content = ""
    if script['type'] == 'external':
        try:
            print(f"  Downloading {script['url']}...")
            r = requests.get(script['url'], verify=False, timeout=10)
            content = r.text
        except:
            print(f"    [!] Failed to download.")
            return findings
    else:
        content = script['content']
        
    if not content: return findings

    # 1. Emails (High Confidence)
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@openai\.com", content)
    if emails: findings['emails'].extend(emails)
    
    # 2. Usernames (Heuristic: "username":"x" or @username)
    # Look for JSON keys "username", "handle", "login"
    usernames = re.findall(r'["\'](username|handle|login)["\']\s*:\s*["\']([a-zA-Z0-9_.-]+)["\']', content)
    for u in usernames:
        if len(u[1]) > 3: findings['usernames'].append(u[1])
        
    # 3. Names (Heuristic: "firstName":"x", "lastName":"y", or "name":"x y")
    names = re.findall(r'["\'](fullName|displayName|name)["\']\s*:\s*["\']([a-zA-Z0-9\s]+)["\']', content)
    for n in names:
        if len(n[1]) > 3 and " " in n[1] and len(n[1]) < 30: # Avoid long strings
            findings['names'].append(n[1])

    # 4. Group Chats / Channels (Heuristic: "channelName", "roomName")
    groups = re.findall(r'["\'](channelName|roomName|groupName)["\']\s*:\s*["\']([a-zA-Z0-9\s_-]+)["\']', content)
    for g in groups:
        findings['groups'].append(g[1])
        
    # 5. Messages (Heuristic: "messageString", "content", "text" but very noisy)
    # Let's look for "messageString":"..." which we saw in the GraphQL fragment
    msgs = re.findall(r'["\']messageString["\']\s*:\s*["\']([^"\']+)["\']', content)
    for m in msgs:
        findings['messages'].append(m)
        
    return findings

def generate_report(all_findings):
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("# PHASE 3: FORUM PII ANALYSIS\n")
        f.write(f"Target: {TARGET_URL}\n\n")
        
        # Aggregate
        agg = {k: set() for k in ["emails", "names", "usernames", "messages", "groups", "api_keys"]}
        
        for f_dict in all_findings:
            for k in agg:
                if k in f_dict:
                    agg[k].update(f_dict[k])
                    
        # Write
        for category, items in agg.items():
            f.write(f"## {category.upper()} ({len(items)})\n")
            if not items:
                f.write("  - None found in static analysis.\n")
            else:
                for item in sorted(list(items))[:50]: # Limit to 50
                    f.write(f"  - `{item}`\n")
                if len(items) > 50:
                    f.write(f"  - ... ({len(items)-50} more)\n")
            f.write("\n")
            
    print(f"\n[+] Report saved to {OUTPUT_REPORT}")

if __name__ == "__main__":
    scripts = fetch_scripts(TARGET_URL)
    all_findings = []
    
    for s in scripts:
        f = analyze_script(s)
        all_findings.append(f)
        
    generate_report(all_findings)
