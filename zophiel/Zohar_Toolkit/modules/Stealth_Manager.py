import requests
import random
import os
import time
from itertools import cycle

# Standard User Agents to Rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0"
]

class StealthSession:
    def __init__(self, proxy_file="proxies.txt"):
        self.session = requests.Session()
        self.proxies = []
        self.proxy_pool = None
        self.current_ip = self._get_real_ip()
        
        # Load Proxies
        self._load_proxies(proxy_file)
        
        # Initial Configuration
        self._rotate_identity()
        
        print("\n" + "="*50)
        print("          🕵️  STEALTH MODE ACTIVATED  🕵️")
        print("="*50)
        print(f"[+] Initial IP: {self.current_ip}")
        if self.proxies:
            print(f"[+] Loaded {len(self.proxies)} proxies from {proxy_file}")
            print("[+] Traffic will be routed through randomized proxies.")
        else:
            print(f"[!] WARNING: No proxies found in '{proxy_file}'.")
            print("[!] STEALTH MODE is operating in 'Fingerprint Only' mode.")
            print("[!] Your IP Address is NOT hidden. Add proxies to 'proxies.txt' to fix this.")
        print("="*50 + "\n")

    def _get_real_ip(self):
        try:
            return requests.get("https://api.ipify.org", timeout=5).text
        except:
            return "Unknown"

    def _load_proxies(self, proxy_file):
        # Look in current directory or parent directory
        paths = [
            proxy_file,
            os.path.join(os.path.dirname(__file__), "..", proxy_file),
            os.path.join(os.path.dirname(__file__), proxy_file)
        ]
        
        found_path = None
        for p in paths:
            if os.path.exists(p):
                found_path = p
                break
        
        if found_path:
            with open(found_path, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            
            if self.proxies:
                self.proxy_pool = cycle(self.proxies)

    def _rotate_identity(self):
        """Rotates User-Agent and Proxy"""
        # 1. Randomize Headers
        ua = random.choice(USER_AGENTS)
        self.session.headers.update({
            "User-Agent": ua,
            "Accept-Language": "en-US,en;q=0.9",
            "DNT": "1", # Do Not Track
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        })
        
        # 2. Rotate Proxy (if available)
        if self.proxy_pool:
            proxy = next(self.proxy_pool)
            self.session.proxies = {
                "http": proxy,
                "https": proxy
            }
            # print(f"[Stealth] Switched Proxy: {proxy}") # Too verbose for production

    def _request_with_retry(self, method, url, max_retries=5, **kwargs):
        last_exception = None
        
        # Ensure timeout is set to avoid hanging
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10

        for i in range(max_retries):
            self._rotate_identity()
            try:
                if method == 'GET':
                    return self.session.get(url, **kwargs)
                elif method == 'POST':
                    return self.session.post(url, **kwargs)
            except Exception as e:
                last_exception = e
                # Optional: print(f"[Stealth] Proxy failed ({i+1}/{max_retries})... rotating.")
                continue
        
        # If we exhausted retries, raise the last exception
        if last_exception:
            raise last_exception
        
        # Fallback (shouldn't happen)
        return self.session.get(url, **kwargs) if method == 'GET' else self.session.post(url, **kwargs)

    def get(self, url, **kwargs):
        return self._request_with_retry('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self._request_with_retry('POST', url, **kwargs)

    def request(self, method, url, **kwargs):
        self._rotate_identity()
        return self.session.request(method, url, **kwargs)

# Singleton instance for easy import
# stealth = StealthSession() 
