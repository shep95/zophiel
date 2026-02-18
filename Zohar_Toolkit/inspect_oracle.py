import json

path = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\ORACLE_KNOWLEDGE_BASE.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Top level keys:", list(data.keys()))
if "domains" in data:
    print("Domains:", list(data["domains"].keys()))
    if "x.com" in data["domains"]:
        print("x.com keys:", list(data["domains"]["x.com"].keys()))
    if "twitter.com" in data["domains"]:
        print("twitter.com keys:", list(data["domains"]["twitter.com"].keys()))
        
if "intelligence" in data:
    print("Intelligence keys:", list(data["intelligence"].keys()))
    if "alive_endpoints" in data["intelligence"]:
        print("First 5 alive endpoints:", data["intelligence"]["alive_endpoints"][:5])
