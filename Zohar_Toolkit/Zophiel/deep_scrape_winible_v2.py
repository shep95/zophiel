import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re

# TARGET URLS TO DIG
TARGETS = [
    "https://www.winible.com/",
    "https://www.winible.com/securedpicks",
    "https://www.winible.com/elitepickz",
    "https://www.winible.com/elitepickzdfs",
]

def scrape_url(url):
    print(f"[*] Deep Digging into: {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. EXTRACT NEXT.JS DATA (The "State" of the app)
            next_data = {}
            next_script = soup.find("script", {"id": "__NEXT_DATA__"})
            if next_script:
                try:
                    next_data = json.loads(next_script.string)
                    print(f"    [+] Found __NEXT_DATA__ JSON blob ({len(str(next_data))} bytes)")
                except:
                    print(f"    [!] Failed to parse __NEXT_DATA__")

            # 2. EXTRACT API KEYS / SECRETS (Regex)
            text = response.text
            keys = extract_keys(text)
            
            # 3. EXTRACT PRICING TIERS (Structured)
            pricing = extract_pricing(soup)

            # 4. EXTRACT REVIEWS / SOCIAL PROOF
            reviews = extract_reviews(soup)
            
            return {
                "url": url,
                "status": "success",
                "next_data_preview": str(next_data)[:500] if next_data else None, # Just preview for log
                "full_next_data": next_data, # Keep full data for analysis
                "exposed_keys": keys,
                "pricing_tiers": pricing,
                "social_proof": reviews
            }
        else:
            return {"url": url, "status": f"failed_{response.status_code}"}
    except Exception as e:
        return {"url": url, "status": f"error_{str(e)}"}

def extract_keys(text):
    keys = {}
    # Stripe Public Keys
    stripe_pk = re.findall(r'pk_live_[a-zA-Z0-9]{20,}', text)
    if stripe_pk: keys['stripe_pk'] = list(set(stripe_pk))
    
    # Google Analytics / Tag Manager
    ga_id = re.findall(r'G-[A-Z0-9]{10}', text)
    if ga_id: keys['google_analytics'] = list(set(ga_id))
    
    # Sentry DSN (Error Tracking - reveals backend structure sometimes)
    sentry = re.findall(r'https://[a-f0-9]+@o[0-9]+\.ingest\.sentry\.io/[0-9]+', text)
    if sentry: keys['sentry_dsn'] = list(set(sentry))
    
    return keys

def extract_pricing(soup):
    tiers = []
    # Look for pricing cards or product lists
    # This is heuristic based on common classes or text
    prices = soup.find_all(string=re.compile(r'\$\d+'))
    for p in prices:
        parent = p.parent
        # Try to find the container
        container = parent.find_parent('div')
        if container:
            text = container.get_text(separator=' | ')
            if len(text) < 500: # limit noise
                tiers.append(text.strip())
    return list(set(tiers))

def extract_reviews(soup):
    reviews = []
    # Look for review stars or common review containers
    # Heuristic: Find text near stars
    stars = soup.find_all(string=re.compile(r'★★★★★|5/5'))
    for s in stars:
        parent = s.parent.parent
        reviews.append(parent.get_text(separator=' ').strip()[:300])
    return list(set(reviews))

def run():
    print(">>> ZOPHIEL DEEP DIG V2: INFRASTRUCTURE & DATA MINING <<<")
    results = []
    
    for url in TARGETS:
        data = scrape_url(url)
        results.append(data)
        time.sleep(1) 
        
    # Save Full Report
    report_path = "Zohar_Toolkit/Zophiel/Intelligence_Reports/Winible_Deep_Tech_Scan.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    # We remove the full next_data from the main JSON to keep it readable, 
    # but we might want to save it separately if it's huge.
    # For now, let's dump it all.
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"\n[+] Tech Scan Complete. Report saved to {report_path}")

    # Analyze findings immediately
    print("\n>>> ANALYSIS OF FINDINGS <<<")
    for r in results:
        if r.get('status') == 'success':
            print(f"\nURL: {r['url']}")
            if r.get('exposed_keys'):
                print(f"  [!] EXPOSED KEYS: {r['exposed_keys']}")
            
            # Analyze Next Data for "Props" (User info, product details)
            nd = r.get('full_next_data', {})
            if nd:
                props = nd.get('props', {}).get('pageProps', {})
                if props:
                    print(f"  [+] NEXT.JS PROPS FOUND: {list(props.keys())}")
                    # Check for specific interesting keys in props
                    if 'creator' in props:
                        c = props['creator']
                        print(f"      -> Creator ID: {c.get('id')}")
                        print(f"      -> Creator Email: {c.get('email')}") # Often null but worth checking
                        print(f"      -> Stripe Connected: {c.get('stripeAccountId')}")
                    if 'products' in props:
                        print(f"      -> Products Found: {len(props['products'])}")
                        for p in props['products'][:3]:
                            print(f"         - {p.get('name')}: ${p.get('price')}")

if __name__ == "__main__":
    run()
