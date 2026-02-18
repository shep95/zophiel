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
    "https://tracxn.com/d/companies/winible/__lIo6giwk4R4ih35Vtg2AfYbXiKrptaIIFw-8VJIakaU",
    "https://www.linkedin.com/company/winible-inc"
]

def scrape_url(url):
    print(f"[*] Digging into: {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Kill scripts
            for s in soup(["script", "style"]):
                s.extract()
            
            text = soup.get_text(separator=' ')
            clean_text = ' '.join(text.split())
            
            # Extract specific intel
            intel = extract_intel(clean_text)
            
            return {
                "url": url,
                "status": "success",
                "intel": intel,
                "raw_text_preview": clean_text[:500]
            }
        else:
            return {"url": url, "status": f"failed_{response.status_code}"}
    except Exception as e:
        return {"url": url, "status": f"error_{str(e)}"}

def extract_intel(text):
    intel = {
        "financial_triggers": [],
        "scam_markers": [],
        "tech_stack": []
    }
    
    text_lower = text.lower()
    
    # Financial Triggers
    if "afterpay" in text_lower: intel["financial_triggers"].append("AfterPay")
    if "klarna" in text_lower: intel["financial_triggers"].append("Klarna")
    if "financing" in text_lower: intel["financial_triggers"].append("Financing")
    
    # Scam Markers
    scam_keywords = ["guaranteed", "lambo", "banned from", "video proof", "easy money", "risk free", "profit", "win rate"]
    for sk in scam_keywords:
        if sk in text_lower:
            intel["scam_markers"].append(sk)
            
    # Tech Stack (very basic detection in text)
    if "vercel" in text_lower: intel["tech_stack"].append("Vercel")
    if "discord" in text_lower: intel["tech_stack"].append("Discord_Integration")
    if "telegram" in text_lower: intel["tech_stack"].append("Telegram_Integration")
    
    return intel

def run():
    print(">>> ZOPHIEL DEEP LINK DIGGER INITIATED <<<")
    results = []
    
    for url in TARGETS:
        data = scrape_url(url)
        results.append(data)
        time.sleep(1) # Be polite
        
    # Save Report
    report_path = "Zohar_Toolkit/Zophiel/Intelligence_Reports/Winible_Deep_Scan.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"\n[+] Deep Dig Complete. Report saved to {report_path}")

if __name__ == "__main__":
    run()
