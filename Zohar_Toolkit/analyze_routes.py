import json
import os
import re

INPUT_FILE = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\X_Corp\Reports\API_ROUTES.json"

def analyze():
    if not os.path.exists(INPUT_FILE):
        print(f"[-] File not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    interesting_keywords = ["admin", "internal", "beta", "staging", "dev", "dashboard", "tools", "debug", "private", "employee"]
    
    unique_routes = set()
    internal_routes = set()
    
    for url, info in data.items():
        routes = info.get("routes", [])
        for route in routes:
            # Clean up quotes
            route = route.strip('"\'')
            unique_routes.add(route)
            
            # Check for interesting keywords
            if any(keyword in route.lower() for keyword in interesting_keywords):
                internal_routes.add(f"{route} (Found in {url})")

    print(f"[*] Total unique routes found: {len(unique_routes)}")
    print(f"[*] Interesting/Internal routes found: {len(internal_routes)}")
    
    print("\n[+] POTENTIAL INTERNAL/ADMIN ROUTES (Excluding DevCommunity & Login):")
    filtered_routes = [
        r for r in internal_routes 
        if "devcommunity.x.com" not in r 
        and "/i/flow/device_login" not in r
    ]
    
    for r in sorted(filtered_routes)[:50]: # Show top 50
        print(f"  - {r}")
        
    print("\n[+] API VERSIONING (v1/v2):")
    v2_routes = [r for r in unique_routes if "/v2/" in r]
    for r in sorted(v2_routes)[:20]:
        print(f"  - {r}")

    # Save interesting routes to a separate file
    with open("interesting_routes.txt", "w") as f:
        for r in sorted(list(internal_routes)):
            f.write(r + "\n")
            
    print("\n[*] Saved all interesting routes to interesting_routes.txt")

if __name__ == "__main__":
    analyze()
