import sys
import os
import requests
import json
import spacy
from bs4 import BeautifulSoup
from collections import Counter
import subprocess

# Ensure Zohar_Toolkit root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SEO_Entity_Mapper:
    """
    RAZIEL MODULE: SEO ENTITY MAPPER
    Reverse-engineers the semantic entity strategy of a target URL.
    Uses NLP to extract Entities (People, Places, Orgs) and Schema Markup.
    """
    
    def __init__(self):
        self.nlp = self._load_spacy_model()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        }

    def _load_spacy_model(self):
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            print("[*] Downloading Spacy Model (en_core_web_sm)...")
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            return spacy.load("en_core_web_sm")

    def fetch_page(self, url):
        try:
            print(f"[*] Fetching {url}...")
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[!] Error fetching URL: {e}")
            return None

    def analyze(self, url):
        html = self.fetch_page(url)
        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Clean Text Extraction
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        
        # 2. NLP Processing
        doc = self.nlp(text[:100000]) # Limit to 100k chars to prevent memory issues
        
        # 3. Entity Extraction
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "PRODUCT", "EVENT", "WORK_OF_ART"]:
                entities.append({"text": ent.text, "label": ent.label_})
        
        # Count top entities
        entity_counts = Counter([f"{e['text']} ({e['label']})" for e in entities])
        
        # 4. Schema Extraction (JSON-LD)
        schemas = []
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                schemas.append(json.loads(script.string))
            except:
                continue

        # 5. Heading Structure
        headings = {
            "H1": [h.get_text(strip=True) for h in soup.find_all('h1')],
            "H2": [h.get_text(strip=True) for h in soup.find_all('h2')],
            "H3": [h.get_text(strip=True) for h in soup.find_all('h3')]
        }

        # 6. Generate Report
        report = {
            "target": url,
            "title": soup.title.string if soup.title else "No Title",
            "meta_description": soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else "No Description",
            "top_entities": entity_counts.most_common(20),
            "heading_structure": headings,
            "schema_markup_count": len(schemas),
            "schemas": schemas
        }
        
        return report

    def save_report(self, report):
        if not report:
            return
            
        filename = f"SEO_Report_{report['target'].replace('https://', '').replace('/', '_')[:30]}.json"
        save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Intelligence_Database", filename)
        
        # Ensure dir exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
            
        print(f"\n[+] Analysis Complete. Report saved to: {save_path}")
        print("\n=== TOP ENTITIES DETECTED ===")
        for ent, count in report['top_entities']:
            print(f"{count}x : {ent}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python SEO_Entity_Mapper.py <url>")
        sys.exit(1)
        
    target_url = sys.argv[1]
    mapper = SEO_Entity_Mapper()
    report = mapper.analyze(target_url)
    mapper.save_report(report)
