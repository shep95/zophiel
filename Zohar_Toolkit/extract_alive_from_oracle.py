import json
import os

def extract():
    path = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\ORACLE_KNOWLEDGE_BASE.json"
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # The structure seems to be:
    # { "domains": { ... }, "intelligence": { "alive_hosts": [...] } }
    # Let's check "intelligence" key.
    
    alive = []
    if "intelligence" in data and "alive_endpoints" in data["intelligence"]:
        alive = data["intelligence"]["alive_endpoints"]
    
    # Also check hades results if present
    # Or just search the whole structure for any URL that has a 200 status recorded
    
    print(f"Found {len(alive)} alive hosts in Oracle.")
    
    # Filter for X Corp (x.com, twitter.com)
    # The list contains dicts: {'url': '...', ...}
    x_targets = []
    for entry in alive:
        if isinstance(entry, dict) and "url" in entry:
            url = entry["url"]
            if "x.com" in url or "twitter.com" in url:
                x_targets.append(url)
        elif isinstance(entry, str):
            # Fallback if mixed types
            if "x.com" in entry or "twitter.com" in entry:
                x_targets.append(entry)
                
    print(f"Filtered for X Corp: {len(x_targets)}")
    
    return x_targets

if __name__ == "__main__":
    targets = extract()
    with open("temp_alive_x.json", "w") as f:
        json.dump(targets, f, indent=2)
