import requests
from bs4 import BeautifulSoup
import re
import json

def analyze_site(url):
    print(f"[*] Analyzing {url}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # 1. Headers Analysis
        r = requests.get(url, headers=headers)
        print(f"\n[+] Status Code: {r.status_code}")
        print("\n[+] Response Headers:")
        for k, v in r.headers.items():
            print(f"    {k}: {v}")
            
        # 2. Content Analysis
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Meta Tags
        print("\n[+] Meta Generator/Tech:")
        for meta in soup.find_all('meta'):
            if meta.get('name') in ['generator', 'application-name', 'viewport']:
                print(f"    {meta.get('name')}: {meta.get('content')}")
                
        # Scripts (Tech Stack & Endpoints)
        print("\n[+] JavaScript Analysis:")
        scripts = soup.find_all('script')
        js_sources = [s.get('src') for s in scripts if s.get('src')]
        
        print(f"    Found {len(js_sources)} external scripts.")
        
        # Look for interesting keywords in inline scripts
        keywords = ['api_key', 'token', 'auth', 'user_id', 'admin', 'internal', 'staging', 'dev']
        for script in scripts:
            if not script.get('src') and script.string:
                content = script.string.lower()
                for kw in keywords:
                    if kw in content:
                        snippet = content[max(0, content.find(kw)-20):min(len(content), content.find(kw)+50)]
                        print(f"    [!] Potential interesting keyword '{kw}' found in inline script: ...{snippet.strip()}...")

        # 3. Link Analysis (Subdomains)
        print("\n[+] Subdomain Recon (from links):")
        links = soup.find_all('a', href=True)
        subdomains = set()
        for link in links:
            href = link['href']
            if 'palantir.com' in href:
                # Extract subdomain
                match = re.search(r'https?://([^/]+)\.palantir\.com', href)
                if match:
                    subdomains.add(match.group(1))
        
        for sub in sorted(subdomains):
            print(f"    - {sub}.palantir.com")

    except Exception as e:
        print(f"[-] Error: {e}")

def check_bot_defenses(url):
    print(f"\n[*] Testing Bot Defenses for {url}...")
    
    # Test 1: WAF Fingerprinting via Headers
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        headers = r.headers
        
        waf_signatures = {
            'Cloudflare': ['cf-ray', '__cfduid', 'cf-cache-status'],
            'AWS WAF': ['x-amzn-requestid', 'x-amz-cf-id'],
            'Akamai': ['x-akamai-transformed', 'akamai-origin-hop'],
            'Fastly': ['x-served-by', 'fastly-client-ip', 'x-fastly-request-id'],
            'Incapsula': ['x-iinfo', 'incap-ses']
        }
        
        detected_wafs = []
        for waf, sigs in waf_signatures.items():
            for sig in sigs:
                if any(h.lower() == sig for h in headers.keys()):
                    detected_wafs.append(waf)
                    break
        
        if detected_wafs:
            print(f"[!] DETECTED WAF/CDN: {', '.join(detected_wafs)}")
        else:
            print("[?] No standard WAF headers detected (Possible hidden WAF or custom solution).")
            
        if 'varnish' in headers.get('via', '').lower():
            print("[!] Varnish Cache Detected (Likely Fastly or Custom Varnish)")

    except Exception as e:
        print(f"[-] WAF Check Error: {e}")

    # Test 2: Client-Side Challenges (JS/Captcha)
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        html_content = r.text.lower()
        
        challenges = []
        if 'recaptcha' in html_content: challenges.append('Google reCAPTCHA')
        if 'hcaptcha' in html_content: challenges.append('hCaptcha')
        if 'turnstile' in html_content: challenges.append('Cloudflare Turnstile')
        if 'challenge-platform' in html_content: challenges.append('Cloudflare JS Challenge')
        if 'perimeterx' in html_content or '_px' in html_content: challenges.append('PerimeterX')
        
        if challenges:
            print(f"[!] ACTIVE CHALLENGES FOUND: {', '.join(challenges)}")
        else:
            print("[-] No explicit JS challenges (Captcha/Turnstile) found on homepage.")

    except Exception as e:
        print(f"[-] Challenge Check Error: {e}")

    # Test 3: User-Agent Blocking (The Canon Check)
    print("\n[*] Testing User-Agent Permissiveness...")
    ua_tests = {
        'Standard Browser': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Python Default': 'python-requests/2.26.0',
        'Empty UA': '',
        'Googlebot': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }
    
    for name, ua in ua_tests.items():
        try:
            r = requests.get(url, headers={'User-Agent': ua}, timeout=5)
            status = r.status_code
            if status == 200:
                result = "ALLOWED"
            elif status == 403:
                result = "BLOCKED (403)"
            elif status == 429:
                result = "RATE LIMITED (429)"
            else:
                result = f"Status {status}"
            print(f"    - {name}: {result}")
        except Exception as e:
            print(f"    - {name}: FAILED ({e})")

if __name__ == "__main__":
    analyze_site("https://www.palantir.com/")
    check_bot_defenses("https://www.palantir.com/")
