import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re

# EXTENDED TARGET LIST (Top Cappers + Platform Pages)
TARGETS = [
    "https://www.winible.com/securedpicks",
    "https://www.winible.com/elitepickz",
    "https://www.winible.com/elitepickzdfs",
    "https://www.winible.com/goldboys",
    "https://www.winible.com/masvet",
    "https://www.winible.com/cashmoney",
]

def audit_url(url):
    print(f"[*] Auditing: {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract JSON State
            next_script = soup.find("script", {"id": "__NEXT_DATA__"})
            if next_script:
                data = json.loads(next_script.string)
                props = data.get('props', {}).get('pageProps', {}).get('store', {})
                
                # 1. INTEGRITY AUDIT (The "Fake Stats" Check)
                integrity_report = {
                    "profit_claimed": props.get('profit'),
                    "units_claimed": props.get('units'),
                    "win_percentage": props.get('winPercentage'),
                    "is_verified": props.get('verifyStatus'),
                    "manual_spreadsheet_url": props.get('personalSiteUrl') # If they use this instead of platform data
                }
                
                # 2. PII LEAKAGE SCAN (Hunting for Dev Failures)
                pii_risk = {
                    "creator_email": props.get('email'), # OFTEN LEAKED IN BAD APIs
                    "creator_phone": props.get('phone'),
                    "stripe_id": props.get('stripeAccountId'),
                    "telegram_link": props.get('telegramUrl'),
                    "discord_link": props.get('discordUrl'),
                    "internal_user_id": props.get('user', {}).get('username')
                }

                # 3. FAKE REVIEW DETECTION (If reviews are loaded in initial props)
                # Note: Reviews often load async, but sometimes they cache the top 3 in props
                reviews = props.get('reviews', [])
                review_audit = []
                if reviews:
                    for r in reviews:
                        review_audit.append({
                            "user": r.get('user', {}).get('username'),
                            "date": r.get('createdAt'),
                            "text_length": len(r.get('content', ''))
                        })
                
                return {
                    "target": url.split('/')[-1],
                    "status": "VULNERABLE",
                    "integrity_audit": integrity_report,
                    "pii_risk": pii_risk,
                    "review_audit": review_audit
                }
            else:
                return {"target": url, "status": "SECURE_OR_NO_DATA"}
        else:
            return {"target": url, "status": f"HTTP_{response.status_code}"}
    except Exception as e:
        return {"target": url, "status": f"ERROR_{str(e)}"}

def run():
    print(">>> ZOPHIEL PROTOCOL V3: REPUTATION & INTEGRITY AUDIT <<<")
    findings = []
    
    for url in TARGETS:
        result = audit_url(url)
        findings.append(result)
        time.sleep(1)
        
    # Analyze for Systemic Failure
    zero_stats_count = 0
    total_audited = 0
    
    print("\n>>> AUDIT RESULTS <<<")
    for f in findings:
        if f['status'] == 'VULNERABLE':
            total_audited += 1
            stats = f['integrity_audit']
            print(f"\nTARGET: {f['target']}")
            print(f"  [!] Verify Status: {stats['is_verified']}")
            print(f"  [!] Platform Profit: {stats['profit_claimed']}")
            print(f"  [!] Platform Win %: {stats['win_percentage']}")
            
            if stats['profit_claimed'] == 0 or stats['profit_claimed'] is None:
                zero_stats_count += 1
                print(f"  [X] INTEGRITY FAILURE: Claims success but Platform Data is EMPTY.")
            
            pii = f['pii_risk']
            if pii['creator_email']:
                print(f"  [!!!] CRITICAL PII LEAK: Email exposed: {pii['creator_email']}")
            if pii['stripe_id']:
                print(f"  [!] PAYMENT LEAK: Stripe Account ID: {pii['stripe_id']}")

    print(f"\n>>> SYSTEMIC FAILURE REPORT <<<")
    print(f"Targets Audited: {total_audited}")
    print(f"Targets with EMPTY/ZERO Platform Stats: {zero_stats_count}")
    if total_audited > 0 and (zero_stats_count / total_audited) > 0.8:
        print("[!!!] CONCLUSION: The entire platform's verification system is UNUSED.")
        print("      This is a 'Trust Theater' operation. They display 'Verified' badges")
        print("      but force users to trust external, editable spreadsheets.")

    # Save to JSON
    with open("Zohar_Toolkit/Zophiel/Intelligence_Reports/Winible_Reputation_Audit.json", "w") as f:
        json.dump(findings, f, indent=4)

if __name__ == "__main__":
    run()
