import requests
from bs4 import BeautifulSoup
import json
import re

# EXTENDED TARGET LIST
TARGETS = [
    "https://www.winible.com/securedpicks",
    "https://www.winible.com/elitepickz",
    "https://www.winible.com/elitepickzdfs",
    "https://www.winible.com/moneylinehacks",
    "https://www.winible.com/trupalocks",
]

def extract_social_links(soup):
    socials = []
    for a in soup.find_all('a', href=True):
        href = a['href'].lower()
        if any(x in href for x in ['twitter.com', 'x.com', 'instagram.com', 'discord.gg', 't.me', 'tiktok.com']):
            socials.append(a['href'])
    return list(set(socials))

def extract_pricing(text):
    # Regex to find prices like $10, $49.99, etc.
    prices = re.findall(r'\$\d+(?:\.\d{2})?', text)
    return list(set(prices))

def extract_marketing_triggers(text):
    triggers = []
    keywords = [
        "guaranteed", "lock", "whale", "max bet", "100%", "risk free", "risk-free",
        "lambo", "millionaire", "banned", "vegas", "insider", "fixed"
    ]
    text_lower = text.lower()
    for kw in keywords:
        if kw in text_lower:
            triggers.append(kw)
    return list(set(triggers))

def audit_url(url):
    print(f"[*] Auditing: {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # EXTRACT FROM JSON ONLY (More Reliable for Next.js)
            script_tag = soup.find('script', id='__NEXT_DATA__')
            
            socials = []
            prices = []
            triggers = []
            integrity_status = "UNKNOWN"
            
            if script_tag:
                try:
                    data = json.loads(script_tag.string)
                    # DEBUG: Print structure for the first target
                    if "securedpicks" in url:
                        print(f"DEBUG: Keys in data: {list(data.keys())}")
                        if 'props' in data:
                            print(f"DEBUG: Keys in props: {list(data['props'].keys())}")
                            if 'pageProps' in data['props']:
                                print(f"DEBUG: Keys in pageProps: {list(data['props']['pageProps'].keys())}")
                                # Save raw JSON to inspect
                                with open("debug_winible.json", "w") as f:
                                    json.dump(data, f, indent=2)
                    
                    props = data.get('props', {}).get('pageProps', {})
                    store = props.get('store', {})
                    
                    # 1. Social Graph (JSON)
                    social_keys = ['twitterUrl', 'instagramUrl', 'tiktokUrl', 'discordUrl', 'telegramUrl', 'youtubeUrl', 'personalSiteUrl']
                    for k in social_keys:
                        if store.get(k):
                            socials.append(store[k])
                    
                    # 2. Pricing (JSON)
                    # Often not in 'store' object but in 'plans' array within pageProps or fetched dynamically
                    # We will check pageProps.plans if it exists
                    plans = props.get('plans', [])
                    if not plans and 'plans' in store:
                        plans = store['plans']
                        
                    for plan in plans:
                        price = plan.get('price')
                        name = plan.get('name')
                        interval = plan.get('interval', 'one_time')
                        prices.append(f"{name}: ${price} ({interval})")
                        
                    # 3. Triggers (Bio + BrandVoice)
                    bio = store.get('bio', '')
                    brand_voice = store.get('brandVoice', '')
                    full_text = f"{bio} {brand_voice}"
                    triggers = extract_marketing_triggers(full_text)
                    
                    # 4. Integrity
                    profit = store.get('profit', 0)
                    win_rate = store.get('winPercentage', None)
                    verify_status = store.get('verifyStatus', 'UNKNOWN')
                    
                    if profit == 0 and win_rate is None:
                        integrity_status = f"FAIL (Status: {verify_status} | Profit: 0)"
                    else:
                        integrity_status = f"PASS (Profit: {profit})"
                        
                    # 5. User Enumeration
                    username = store.get('user', {}).get('username', 'UNKNOWN')
                    if username:
                         triggers.append(f"Username: {username}")
                        
                except Exception as e:
                    integrity_status = f"JSON Error: {e}"
            
            return {
                "url": url,
                "status": "ALIVE",
                "socials": socials,
                "prices": prices,
                "triggers": triggers,
                "integrity": integrity_status
            }
        else:
            return {"url": url, "status": f"DEAD ({response.status_code})"}
            
    except Exception as e:
        return {"url": url, "status": f"ERROR ({str(e)})"}

def run():
    print(">>> ZOPHIEL V4: DEEP DIG PROTOCOL INITIATED <<<")
    results = []
    for target in TARGETS:
        result = audit_url(target)
        results.append(result)
        
    print("\n>>> V4 INTELLIGENCE SUMMARY <<<")
    for r in results:
        if r['status'] == "ALIVE":
            print(f"\nTARGET: {r['url'].split('/')[-1]}")
            print(f"  [+] Social Graph: {len(r['socials'])} found ({', '.join(r['socials'][:3])}...)")
            print(f"  [+] Pricing Tiers: {r['prices']}")
            print(f"  [+] Predatory Triggers: {r['triggers']}")
            print(f"  [!] Integrity Check: {r['integrity']}")
        else:
            print(f"TARGET: {r['url'].split('/')[-1]} -> {r['status']}")

if __name__ == "__main__":
    run()
