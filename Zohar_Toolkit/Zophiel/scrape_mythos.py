import requests
from bs4 import BeautifulSoup
import os
import time
import random
import urllib3

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target URL
TARGET_URLS = [
    "https://www.mythoshub.com/",
    # Add other potential subpages if known, otherwise just the main page
    "https://www.mythoshub.com/numerology",
    "https://www.mythoshub.com/gematria",
    "https://www.mythoshub.com/bazi",
    "https://www.mythoshub.com/mbti",
    "https://www.mythoshub.com/blood-type",
    "https://www.mythoshub.com/astrolab",
    "https://www.mythoshub.com/lunar",
    "https://www.mythoshub.com/vedic",
    "https://www.mythoshub.com/reading",
    "https://www.mythoshub.com/codex",
    "https://www.mythoshub.com/apex-clock",
    "https://www.mythoshub.com/canvas",
    "https://www.mythoshub.com/mythic-identity",
    "https://www.mythoshub.com/blog"
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

def scrape_site(url):
    print(f"[*] Deep Scraping: {url}")
    try:
        time.sleep(random.uniform(1.5, 3.0)) # Polite delay
        # Disable SSL verification to bypass certificate errors
        response = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        
        # Check if the response was successful
        if response.status_code != 200:
            print(f"[-] Failed to access {url} (Status: {response.status_code})")
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove junk elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            element.decompose()
            
        # Attempt to find main content to avoid menu noise
        main_content = None
        selectors = ['article', 'main', '.post-content', '.entry-content', '#content', '.blog-post', '.page-content', 'body']
        
        for selector in selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
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
    report_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'MYTHOS_HUB_INTEL.txt')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    print("==================================================")
    print("   ZOPHIEL: MYTHOS HUB DATA EXTRACTION")
    print("==================================================")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("ZOPHIEL INTELLIGENCE REPORT: MYTHOS HUB\n")
        f.write("CLASSIFICATION: OSINT // METAPHYSICAL\n")
        f.write(f"DATE: {time.strftime('%Y-%m-%d')}\n")
        f.write("OBJECTIVE: EXTRACT DATA FROM MYTHOSHUB.COM\n")
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
                f.write("ACCESS DENIED OR CONTENT UNREADABLE (Might be 404 or blocked)\n")
                f.write("\n\n" + "=" * 50 + "\n\n")
                
    print(f"\n[+] Deep Dive complete. Intelligence saved to: {report_path}")

if __name__ == "__main__":
    generate_report()
