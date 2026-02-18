import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from urllib.parse import urljoin

def get_soup(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    try:
        print(f"[*] Visiting {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"[!] Error visiting {url}: {e}")
    return None

def scan_palantir():
    base_url = "https://www.palantir.com/"
    soup = get_soup(base_url)
    
    if not soup:
        return

    # Identify Product Links
    products = {
        "Foundry": None,
        "Gotham": None,
        "Apollo": None,
        "AIP": None
    }
    
    # Simple heuristic to find product pages
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        text = a.get_text().lower()
        
        if "foundry" in text or "foundry" in href:
            if not products["Foundry"] and "palantir.com" in full_url:
                products["Foundry"] = full_url
        elif "gotham" in text or "gotham" in href:
            if not products["Gotham"] and "palantir.com" in full_url:
                products["Gotham"] = full_url
        elif "apollo" in text or "apollo" in href:
            if not products["Apollo"] and "palantir.com" in full_url:
                products["Apollo"] = full_url
        elif "aip" in text or "artificial intelligence" in text:
            if not products["AIP"] and "palantir.com" in full_url:
                products["AIP"] = full_url

    print("\n[+] Identified Product Pages:")
    for name, url in products.items():
        print(f"    {name}: {url}")
        
    return products

def deep_scrape(products):
    report_data = {}
    
    for name, url in products.items():
        if not url:
            continue
            
        print(f"\n[*] Deep Scraping {name} at {url}...")
        soup = get_soup(url)
        if soup:
            # Kill script/style
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            text = soup.get_text(separator='\n')
            # Clean up empty lines
            clean_text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
            report_data[name] = clean_text[:10000] # Cap at 10k chars for analysis
            
    return report_data

if __name__ == "__main__":
    products = scan_palantir()
    # Manual overrides if auto-discovery fails (common with landing pages)
    if not products["Foundry"]: products["Foundry"] = "https://www.palantir.com/platforms/foundry/"
    if not products["Gotham"]: products["Gotham"] = "https://www.palantir.com/platforms/gotham/"
    if not products["Apollo"]: products["Apollo"] = "https://www.palantir.com/platforms/apollo/"
    if not products["AIP"]: products["AIP"] = "https://www.palantir.com/platforms/aip/"
    
    data = deep_scrape(products)
    
    # Save raw dump for analysis
    with open("palantir_raw_dump.txt", "w", encoding="utf-8") as f:
        for name, content in data.items():
            f.write(f"\n\n{'='*50}\n{name}\n{'='*50}\n{content}")
