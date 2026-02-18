import requests
import re
import warnings
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Suppress insecure request warnings
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Configuration
KEYWORDS = {
    "Strawberry": r"(?i)\b(project\s+)?strawberry\b",
    "Orion": r"(?i)\b(project\s+)?orion\b",
    "Q*": r"(?i)q\*",
    "Arrakis": r"(?i)\barrakis\b",
    "Gobi": r"(?i)\bgobi\b",
    "Sahara": r"(?i)\bsahara\b",
    "GPT-5": r"(?i)\bgpt-5\b",
    "GPT-6": r"(?i)\bgpt-6\b",
    "Sora": r"(?i)\bsora\b",
    "Voice Engine": r"(?i)voice\s+engine",
    "Feather": r"(?i)\bfeather\b",
    "Operator": r"(?i)\boperator\b",
    "SearchGPT": r"(?i)\bsearchgpt\b",
    "Stargate": r"(?i)\bstargate\b",
    "Cactus": r"(?i)\bcactus\b",
    "Mallard": r"(?i)\bmallard\b"
}

TARGETS = [
    "https://cookbook.openai.com",
    "https://openai-team.forum.openai.com",
    "https://help.openai.com",
    "https://platform.openai.com",
    "https://cdn.openai.com",
    "https://research.openai.com",
    "https://openai.com",
    "https://api.openai.com",
    # Add a few shards if reachable (often 404, but might leak in error pages or specific paths)
    "https://unified-6.api.openai.com", 
    "https://unified-4.api.openai.com"
]

OUTPUT_FILE = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\OpenAI\Reports\DEEP_DIVE_PHASE4_KEYWORDS.md"

def fetch_url(url):
    try:
        response = requests.get(url, verify=False, timeout=10)
        return response.text
    except Exception as e:
        return ""

def extract_js_links(url, html):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = []
    for script in soup.find_all('script'):
        src = script.get('src')
        if src:
            if src.startswith('/'):
                src = url + src
            elif not src.startswith('http'):
                src = url + '/' + src
            scripts.append(src)
    return list(set(scripts))

def analyze_content(url, content, findings_list):
    for name, pattern in KEYWORDS.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end].replace('\n', ' ')
            findings_list.append({
                "keyword": name,
                "url": url,
                "context": context.strip()
            })

def process_target(url):
    print(f"[+] Scanning {url}...")
    html = fetch_url(url)
    if not html:
        return []
    
    findings = []
    analyze_content(url, html, findings)
    
    # Scan JS files
    js_links = extract_js_links(url, html)
    print(f"  - Found {len(js_links)} JS files on {url}")
    
    for js_link in js_links:
        js_content = fetch_url(js_link)
        if js_content:
            analyze_content(js_link, js_content, findings)
            
    return findings

def main():
    print("[-] Starting Phase 4: Keyword Hunt for Future Projects...")
    
    all_findings = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(process_target, TARGETS)
        for res in results:
            all_findings.extend(res)
            
    # Generate Report
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# PHASE 4: FUTURE PROJECT KEYWORD SCAN\n")
        f.write("Targets: " + ", ".join(TARGETS) + "\n\n")
        
        if not all_findings:
            f.write("No significant keywords found in public assets.\n")
        else:
            # Group by keyword
            grouped = {}
            for item in all_findings:
                k = item['keyword']
                if k not in grouped:
                    grouped[k] = []
                grouped[k].append(item)
            
            for k, items in grouped.items():
                f.write(f"## {k.upper()} ({len(items)} hits)\n")
                seen_contexts = set()
                for item in items:
                    # Deduplicate by context roughly
                    if item['context'] in seen_contexts:
                        continue
                    seen_contexts.add(item['context'])
                    
                    f.write(f"- **Source**: `{item['url']}`\n")
                    f.write(f"  - Context: \"...{item['context']}...\"\n\n")

    print(f"\n[+] Scan Complete. Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
