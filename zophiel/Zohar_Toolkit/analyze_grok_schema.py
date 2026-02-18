import json
import re
from colorama import Fore, init

init(autoreset=True)

SCHEMA_FILE = "grok_schema.json"

def analyze_schema():
    print(f"{Fore.MAGENTA}=== Analyzing Grok GraphQL Schema for 'Deep' Endpoints ===")
    
    try:
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to load schema: {e}")
        return

    # Navigate to types
    types = data.get("__schema", {}).get("types", [])
    
    keywords = ["Deep", "Research", "Internal", "Admin", "Debug", "Flag", "Money", "Transaction", "Secret"]
    
    findings = []
    
    for t in types:
        name = t.get("name", "")
        if not name: continue
        
        # Check type name
        for k in keywords:
            if k.lower() in name.lower():
                findings.append(f"Type: {name}")
        
        # Check fields
        fields = t.get("fields")
        if fields:
            for field in fields:
                field_name = field.get("name", "")
                for k in keywords:
                    if k.lower() in field_name.lower():
                        findings.append(f"Field: {name}.{field_name}")

    if findings:
        print(f"{Fore.GREEN}[+] Found {len(findings)} 'Deep' indicators:")
        for f in findings[:50]: # Limit output
            print(f"    - {f}")
    else:
        print("[-] No 'Deep' indicators found in schema.")

if __name__ == "__main__":
    analyze_schema()
