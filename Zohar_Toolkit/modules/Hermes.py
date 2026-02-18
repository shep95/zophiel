import requests
import json
import re

class Hermes:
    """
    HERMES: The Messenger.
    Module for Subdomain Enumeration via Certificate Transparency Logs.
    Finds the 'underground' paths (subdomains) without touching the target directly.
    """
    def __init__(self, oracle=None):
        self.oracle = oracle
        self.crt_sh_url = "https://crt.sh/?q=%.{}&output=json"
        self.hackertarget_url = "https://api.hackertarget.com/hostsearch/?q={}"

    def scout(self, domain):
        print(f"\n[HERMES] Flying through Certificate Transparency logs for {domain}...")
        subdomains = set()
        
        # Primary Source: crt.sh
        try:
            url = self.crt_sh_url.format(domain)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            
            # Increased timeout to 45s
            response = requests.get(url, headers=headers, timeout=45)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    for entry in data:
                        name_value = entry['name_value']
                        lines = name_value.split('\n')
                        for line in lines:
                            if '*' not in line: 
                                subdomains.add(line.strip().lower())
                except json.JSONDecodeError:
                    print("  [!] crt.sh JSON parse error. Falling back to regex.")
                    found = re.findall(r'<TD>([a-zA-Z0-9.-]+\.' + re.escape(domain) + r')</TD>', response.text, re.IGNORECASE)
                    subdomains.update([f.lower() for f in found])
            else:
                print(f"  [!] crt.sh inaccessible: {response.status_code}")

        except Exception as e:
            print(f"  [!] Hermes Wing Broken (crt.sh): {e}")

        # Secondary Source: HackerTarget (Fallback)
        if len(subdomains) == 0:
            print("  [!] Engaging secondary thrusters (HackerTarget)...")
            try:
                url = self.hackertarget_url.format(domain)
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    lines = response.text.split('\n')
                    for line in lines:
                        # Format is usually: hostname,IP
                        if ',' in line:
                            host = line.split(',')[0]
                            if domain in host:
                                subdomains.add(host.strip().lower())
                else:
                     print(f"  [!] HackerTarget inaccessible: {response.status_code}")
            except Exception as e:
                print(f"  [!] Hermes Wing Broken (HackerTarget): {e}")
        
        sorted_subs = sorted(list(subdomains))
        print(f"  [+] Discovered {len(sorted_subs)} subdomains via CT Logs.")
        
        if self.oracle:
            self.oracle.add_subdomains(domain, sorted_subs)
            
        return sorted_subs
