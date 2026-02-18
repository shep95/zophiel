import requests
from bs4 import BeautifulSoup
import os
import time
import random

# Target URLs identified as "Elite" or containing "Hidden Knowledge"
TARGET_URLS = [
    # DEATH & LONGEVITY: 64th Navamsa & 22nd Drekkana
    "https://medium.com/thoughts-on-jyotish/timing-through-graha-s-nakshatra-pada-transits-part-2-64th-navamsa-68cbbe39cf3f",
    "https://saptarishisshop.com/usage-of-64th-navamsa-and-22nd-drekkana-in-prashna/",
    
    # WEALTH & POWER: Indu Lagna & Yogada
    "https://astrosanhita.com/indu-lagna-dhana-lagna-reservoir-of-wealth-and-prosperity/",
    "https://www.decodingvedicwisdom.com/indu-lagna-keys-to-hidden-prosperity-in-the-horoscope",
    
    # MARRIAGE & SOULMATE: Upapada Lagna (UL)
    "https://shrifreedom.org/vedic-astrology/upapada-lagna/",
    "https://astrologylover.com/upapada-lagna/",
    
    # CHILDREN & FERTILITY: Beeja & Kshetra Sphuta
    "https://www.eastrovedica.com/html/vedic_astrologylesson52.asp",
    "https://planetarypositions.com/astro-remedies/2015/07/04/beeja-sphuta-kshetra-sphuta/",
    
    # PRECISE TIMING: Tithi Pravesha (True Vedic Birthday)
    "https://srath.com/jyoti%E1%B9%A3a/tithi-pravesa/tithi-pravesha/",
    "https://blog.cosmicinsights.net/importance-tithi-pravesha-real-vedic-birthday/"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def clean_text(text):
    """Cleans extracted text to remove excessive whitespace."""
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return '\n'.join(chunk for chunk in chunks if chunk)

import urllib3

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_site(url):
    print(f"[*] Deep Scraping: {url}")
    try:
        time.sleep(random.uniform(1.5, 3.0)) # Polite delay
        # Disable SSL verification to bypass certificate errors
        response = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove junk elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            element.decompose()
            
        # Attempt to find main content to avoid menu noise
        # Common content classes/ids
        main_content = None
        selectors = ['article', 'main', '.post-content', '.entry-content', '#content', '.blog-post']
        
        for selector in selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.body
            
        if not main_content:
            return None
            
        # Extract title
        title = soup.title.string if soup.title else "Unknown Title"
        
        # Extract text
        text = clean_text(main_content.get_text(separator='\n'))
        
        return {
            "title": title,
            "url": url,
            "content": text
        }
        
    except Exception as e:
        print(f"[-] Failed to scrape {url}: {e}")
        return None

def generate_report():
    report_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'VEDIC_ELITE_DEEP_DIVE.txt')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    print("==================================================")
    print("   ZOPHIEL: DEEP KNOWLEDGE EXTRACTION PROTOCOL")
    print("==================================================")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("ZOPHIEL INTELLIGENCE REPORT: ELITE VEDIC KNOWLEDGE DEEP DIVE\n")
        f.write("CLASSIFICATION: TOP SECRET / OCCULT\n")
        f.write(f"DATE: {time.strftime('%Y-%m-%d')}\n")
        f.write("OBJECTIVE: TOTAL KNOWLEDGE EXTRACTION FROM TARGET NODES\n")
        f.write("==================================================\n\n")
        
        for url in TARGET_URLS:
            data = scrape_site(url)
            if data:
                f.write(f"SOURCE NODE: {data['title']}\n")
                f.write(f"URL: {data['url']}\n")
                f.write("-" * 50 + "\n")
                f.write(data['content'])
                f.write("\n\n" + "=" * 50 + "\n\n")
                print(f"[+] Extracted {len(data['content'])} bytes from {data['title']}")
            else:
                f.write(f"SOURCE NODE: FAILED TO EXTRACT\n")
                f.write(f"URL: {url}\n")
                f.write("-" * 50 + "\n")
                f.write("ACCESS DENIED OR CONTENT UNREADABLE\n")
                f.write("\n\n" + "=" * 50 + "\n\n")
                
    print(f"\n[+] Deep Dive complete. Intelligence saved to: {report_path}")

if __name__ == "__main__":
    generate_report()
