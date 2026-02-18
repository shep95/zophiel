import requests
import re
import json
import os
import concurrent.futures

# We focus on Grok and main App bundles
TARGETS = [
    "https://grok.x.com",
    "https://x.com",
    "https://analytics.x.com"
]

# Keywords to find AI/Backend structure
KEYWORDS = {
    "Models": [r"grok-[\w\d]+", r"gpt-[\w\d]+", r"claude", r"llama", r"model_name", r"inference"],
    "Endpoints": [r"\/i\/api\/[\w\d\/]+", r"graphql", r"grpc"],
    "Internal": [r"internal-static-assets", r"admin", r"dashboard", r"employee"],
    "Auth": [r"auth_token", r"bearer", r"oauth", r"sso"]
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_js_urls(url):
    js_links = set()
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        # Simple regex for src="..."
        matches = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', resp.text)
        for match in matches:
            if match.startswith("//"):
                js_links.add("https:" + match)
            elif match.startswith("/"):
                js_links.add(url.rstrip("/") + match)
            elif match.startswith("http"):
                js_links.add(match)
    except:
        pass
    return list(js_links)

def scan_bundle(js_url):
    findings = {"url": js_url, "matches": {}}
    try:
        resp = requests.get(js_url, headers=HEADERS, timeout=10, verify=False)
        text = resp.text
        
        for category, patterns in KEYWORDS.items():
            for pat in patterns:
                matches = re.findall(pat, text, re.IGNORECASE)
                if matches:
                    if category not in findings["matches"]:
                        findings["matches"][category] = []
                    findings["matches"][category].extend(list(set(matches[:5]))) # Limit to 5 per pattern
    except:
        pass
    return findings

def map_backend():
    print("[*] Mapping Backend & AI Architecture...")
    
    all_findings = {}
    
    for target in TARGETS:
        print(f"[*] Fetching bundles for {target}...")
        js_urls = fetch_js_urls(target)
        print(f"    Found {len(js_urls)} JS bundles.")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(scan_bundle, url): url for url in js_urls}
            
            target_data = []
            for future in concurrent.futures.as_completed(future_to_url):
                res = future.result()
                if res["matches"]:
                    target_data.append(res)
            
            all_findings[target] = target_data
            
    # Save results
    with open("backend_map.json", "w", encoding="utf-8") as f:
        json.dump(all_findings, f, indent=2)
        
    print("[*] Backend Map saved to backend_map.json")
    
    # Generate Mermaid Diagram source
    generate_diagram(all_findings)

def generate_diagram(data):
    mermaid = ["graph TD"]
    mermaid.append("    User[User/Client] --> X_LB[X Load Balancer]")
    
    for target, bundles in data.items():
        clean_target = target.replace("https://", "").replace(".", "_")
        mermaid.append(f"    X_LB --> {clean_target}[{target}]")
        
        for bundle in bundles:
            # Check for AI models
            if "Models" in bundle["matches"]:
                for model in bundle["matches"]["Models"]:
                    model_id = re.sub(r"[^a-zA-Z0-9]", "_", model)
                    mermaid.append(f"    {clean_target} -.-> {model_id}(AI Model: {model})")
            
            # Check for Endpoints
            if "Endpoints" in bundle["matches"]:
                for ep in bundle["matches"]["Endpoints"]:
                    ep_id = re.sub(r"[^a-zA-Z0-9]", "_", ep)
                    mermaid.append(f"    {clean_target} --> {ep_id}(API: {ep})")

    with open("backend_architecture.mmd", "w", encoding="utf-8") as f:
        f.write("\n".join(mermaid))
    print("[*] Mermaid Diagram saved to backend_architecture.mmd")

if __name__ == "__main__":
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    map_backend()
