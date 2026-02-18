import requests
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.mythoshub.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

def get_links(url):
    print(f"[*] Crawling {url} for links...")
    try:
        resp = requests.get(url, headers=HEADERS, verify=False, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/'):
                href = BASE_URL + href
            if BASE_URL in href:
                links.add(href)
        
        print(f"    Found {len(links)} links.")
        return links
    except Exception as e:
        print(f"    Error: {e}")
        return set()

def check_url(url):
    try:
        resp = requests.get(url, headers=HEADERS, verify=False, timeout=5)
        if resp.status_code == 200:
            return True, len(resp.content)
        return False, 0
    except:
        return False, 0

def discover_deep_pages():
    # 1. Crawl main pages
    main_pages = [
        "https://www.mythoshub.com/numerology",
        "https://www.mythoshub.com/blood-type",
        "https://www.mythoshub.com/mbti"
    ]
    
    all_links = set()
    for page in main_pages:
        links = get_links(page)
        all_links.update(links)

    # 2. Filter for interesting sub-pages
    potential_deep_pages = []
    for link in all_links:
        # We want sub-pages like /numerology/1 or /blood-type/a-positive
        if any(x in link for x in ['/numerology/', '/blood-type/', '/mbti/']) and link not in main_pages:
            potential_deep_pages.append(link)

    # 3. If crawling failed to find them (SPA), try brute-forcing common patterns
    print("[*] Brute-forcing potential URL patterns...")
    patterns = [
        # Numerology
        "https://www.mythoshub.com/numerology/1",
        "https://www.mythoshub.com/numerology/life-path-1",
        "https://www.mythoshub.com/numerology/number-1",
        "https://www.mythoshub.com/numerology/meaning/1",
        
        # Blood Type
        "https://www.mythoshub.com/blood-type/a",
        "https://www.mythoshub.com/blood-type/a-positive",
        "https://www.mythoshub.com/blood-type/type-a",
        
        # MBTI
        "https://www.mythoshub.com/mbti/intj",
        "https://www.mythoshub.com/mbti/type/intj",
        "https://www.mythoshub.com/mbti/16-types/intj"
    ]
    
    for url in patterns:
        exists, size = check_url(url)
        if exists:
            print(f"    [+] FOUND: {url} (Size: {size})")
            potential_deep_pages.append(url)
        else:
            print(f"    [-] Failed: {url}")

    return list(set(potential_deep_pages))

if __name__ == "__main__":
    pages = discover_deep_pages()
    print("\n[=] DISCOVERED DEEP PAGES:")
    for p in pages:
        print(p)
