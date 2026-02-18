import requests
import json
import concurrent.futures
import re
from urllib3.exceptions import InsecureRequestWarning

# Suppress warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class Hades:
    """
    HADES: God of the Underworld.
    Module for Deep Probing of Subdomain Shards.
    Checks reachability, bypasses WAFs, and scrapes for keywords on alive hosts.
    """
    def __init__(self, oracle=None):
        self.oracle = oracle
        self.findings = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.keywords = [
            "strawberry", "orion", "arrakis", "q-star", "feathers", 
            "gpt-5", "gpt-4.5", "internal", "admin", "key", "token", "secret"
        ]

    def clean_target(self, target):
        """Removes wildcards and protocols for clean probing"""
        target = target.replace("https://", "").replace("http://", "")
        if target.startswith("*."):
            target = target[2:]
        return target

    def probe_host(self, host):
        """Probes a single host for status and content"""
        url = f"https://{host}"
        try:
            # Short timeout for speed
            response = requests.get(url, headers=self.headers, verify=False, timeout=5)
            status = response.status_code
            length = len(response.text)
            title = "N/A"
            
            # Extract title if HTML
            if "<title>" in response.text:
                title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
            
            result = {
                "url": url,
                "status": status,
                "length": length,
                "title": title,
                "interesting_content": []
            }

            # Check for WAF blocks (403/406) vs potential access (200, 401, 404, 500)
            if status not in [403, 503]:
                print(f"  [+] ALIVE: {url} [{status}] - {title}")
                
                if self.oracle:
                    self.oracle.add_alive_host(url, status, response.headers.get("Server"))
                
                # Scan content for keywords
                for kw in self.keywords:
                    if kw.lower() in response.text.lower():
                        result["interesting_content"].append(kw)
                        print(f"    [!] FOUND KEYWORD: {kw} in {url}")
                
                return result
            else:
                # WAF Blocked
                return None

        except Exception:
            return None

    def torture(self, subdomains, max_threads=20):
        """
        Mass probes the list of subdomains.
        """
        print(f"\n[HADES] Unleashing {max_threads} demons to probe {len(subdomains)} targets...")
        
        cleaned_targets = set()
        for s in subdomains:
            cleaned_targets.add(self.clean_target(s))
            # Also try 'api' prefix for unified gateways if not present
            clean = self.clean_target(s)
            if "unified" in clean and not clean.startswith("api."):
                 cleaned_targets.add(f"api.{clean}")
                 cleaned_targets.add(f"dev.{clean}")

        print(f"  [*] Expanded target list to {len(cleaned_targets)} endpoints.")
        
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_url = {executor.submit(self.probe_host, target): target for target in cleaned_targets}
            for future in concurrent.futures.as_completed(future_to_url):
                data = future.result()
                if data:
                    results.append(data)
        
        self.findings = results
        print(f"[HADES] Probe complete. Found {len(results)} accessible endpoints.")
        return results
