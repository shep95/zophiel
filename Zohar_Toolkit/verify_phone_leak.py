import requests
import re
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

URL = "https://x.com/i/flow/device_login"

def check():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    resp = requests.get(URL, headers=headers, verify=False)
    
    # Save for manual review if needed
    with open("device_login_source.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
        
    print(f"[*] Response Length: {len(resp.text)}")
    
    # Check what the "phone" numbers are
    # The regex was \b\+?[1-9]\d{1,14}\b
    matches = re.findall(r"\b\+?[1-9]\d{1,14}\b", resp.text)
    
    print("[*] Sample matches:")
    for m in matches[:10]:
        print(f"  - {m}")
        
    # Check context
    if "abs.twimg.com" in resp.text:
        print("[*] Contains static asset links (Likely false positives from version numbers in URLs)")

if __name__ == "__main__":
    check()
