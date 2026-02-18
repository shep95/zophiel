import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_text(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    try:
        print(f"[*] Fetching {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Kill script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            # Break into lines and remove leading/trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
        else:
            return f"Error: Status {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# Target 1: The Insurance Fraud Case
url_case = "https://www.insurancejournal.com/news/east/2003/12/04/34694.htm"
print("\n=== INSURANCE JOURNAL ARTICLE ===")
print(get_text(url_case)[:3000]) # Print first 3000 chars

# Target 2: The Business Structure
url_biz = "https://whop.com/discover/gg33-academy/"
print("\n=== WHOP GG33 ACADEMY ===")
print(get_text(url_biz)[:3000])
