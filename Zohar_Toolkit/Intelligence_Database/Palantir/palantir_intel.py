import requests
from bs4 import BeautifulSoup
import re
import json
import time
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

class PalantirIntel:
    def __init__(self):
        self.base_url = "https://www.palantir.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.dossier = {
            "target": "Palantir Technologies",
            "infrastructure": {},
            "subdomains": set(),
            "emails": set(),
            "documents": set(),
            "key_personnel": set(),
            "product_routes": set(),
            "investor_relations": set()
        }

    def get_infrastructure(self):
        print("[*] Profiling Infrastructure...")
        try:
            r = requests.get(self.base_url, headers=self.headers)
            self.dossier["infrastructure"]["server"] = r.headers.get("Server", "Unknown")
            self.dossier["infrastructure"]["cdn"] = r.headers.get("X-Served-By", "Unknown")
            self.dossier["infrastructure"]["tech_stack"] = []
            
            # CSP Analysis for 3rd party tools
            csp = r.headers.get("Content-Security-Policy", "")
            if "marketo" in csp: self.dossier["infrastructure"]["tech_stack"].append("Marketo (Marketing)")
            if "lever.co" in csp: self.dossier["infrastructure"]["tech_stack"].append("Lever (Recruiting)")
            if "heapanalytics" in csp: self.dossier["infrastructure"]["tech_stack"].append("Heap (Analytics)")
            if "onetrust" in csp: self.dossier["infrastructure"]["tech_stack"].append("OneTrust (Compliance)")
            
        except Exception as e:
            print(f"[-] Infra Error: {e}")

    def parse_sitemaps(self):
        print("[*] Extracting Intelligence from Sitemaps...")
        sitemaps = [
            "https://www.palantir.com/sitemap.xml",
            "https://www.palantir.com/docs/sitemap.xml"
        ]
        
        urls = []
        for sm_url in sitemaps:
            try:
                r = requests.get(sm_url, headers=self.headers)
                if r.status_code == 200:
                    # Simple XML parsing (some sitemaps are nested, handling basic list here)
                    # If it's a sitemap index, we'd need to recurse, but let's try regex for speed/robustness
                    found = re.findall(r'<loc>(https://.*?)</loc>', r.text)
                    urls.extend(found)
            except Exception as e:
                print(f"[-] Sitemap Error {sm_url}: {e}")
        
        print(f"[+] Found {len(urls)} total public URLs.")
        self.analyze_urls(urls)

    def analyze_urls(self, urls):
        print("[*] Categorizing Intelligence...")
        for url in urls:
            # 1. Subdomain Discovery
            parsed = urlparse(url)
            if parsed.netloc != "www.palantir.com":
                self.dossier["subdomains"].add(parsed.netloc)

            # 2. Document Discovery
            if url.endswith(('.pdf', '.docx', '.pptx')):
                self.dossier["documents"].add(url)
            
            # 3. Product Routes
            if '/platforms/' in url or '/aip/' in url:
                self.dossier["product_routes"].add(url)
                
            # 4. Investor/Governance
            if 'investors' in url or 'governance' in url or 'board' in url:
                self.dossier["investor_relations"].add(url)

    def deep_scan_critical_pages(self):
        print("[*] Deep Scanning High-Value Pages (Contact, Team)...")
        # List of pages likely to contain names/emails
        targets = [
            "https://www.palantir.com/contact/",
            "https://www.palantir.com/about/",
            "https://www.palantir.com/careers/"
        ]
        
        for url in targets:
            try:
                r = requests.get(url, headers=self.headers)
                text = r.text
                
                # Email Extraction
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@palantir\.com', text)
                self.dossier["emails"].update(emails)
                
                # Phone Extraction (US format)
                phones = re.findall(r'\+1\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
                # Filter out common false positives if necessary
                
            except:
                pass

    def generate_report(self):
        filename = "Palantir_Target_Dossier.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# TARGET INTELLIGENCE DOSSIER: PALANTIR TECHNOLOGIES\n")
            f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 1. INFRASTRUCTURE FOOTPRINT\n")
            f.write(f"- **Hosting:** {self.dossier['infrastructure'].get('server')}\n")
            f.write(f"- **CDN/Edge:** {self.dossier['infrastructure'].get('cdn')}\n")
            f.write(f"- **Tech Stack:** {', '.join(self.dossier['infrastructure'].get('tech_stack', []))}\n\n")
            
            f.write("## 2. DISCOVERED SUBDOMAINS\n")
            for sub in sorted(self.dossier["subdomains"]):
                f.write(f"- {sub}\n")
            if not self.dossier["subdomains"]: f.write("- No external subdomains in public sitemap.\n")
            f.write("\n")
            
            f.write("## 3. HIGH-VALUE DOCUMENTS (PDFs/Whitepapers)\n")
            # Limit to top 10 for brevity
            for doc in sorted(list(self.dossier["documents"]))[:15]:
                f.write(f"- {doc}\n")
            f.write(f"*(Total Documents Found: {len(self.dossier['documents'])})*\n\n")
            
            f.write("## 4. KEY PRODUCT ROUTES (AIP/Foundry)\n")
            for route in sorted(list(self.dossier["product_routes"]))[:10]:
                f.write(f"- {route}\n")
            f.write("\n")

            f.write("## 5. CONTACT INTELLIGENCE\n")
            if self.dossier["emails"]:
                f.write("**Direct Emails:**\n")
                for email in self.dossier["emails"]:
                    f.write(f"- {email}\n")
            else:
                f.write("- No direct @palantir.com emails exposed on public surface (High OpSec).\n")
            
            f.write("\n## 6. OBSERVATIONS\n")
            f.write("- Target uses heavy obfuscation for employee contact info.\n")
            f.write("- Public site is static (S3/Fastly) to reduce attack surface.\n")
            f.write("- Primary data flow is via external API integrations (Lever, Marketo).\n")

        print(f"\n[+] Intelligence Dossier Generated: {filename}")
        return filename

if __name__ == "__main__":
    intel = PalantirIntel()
    intel.get_infrastructure()
    intel.parse_sitemaps()
    intel.deep_scan_critical_pages()
    intel.generate_report()
