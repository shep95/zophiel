"""
ZOPHIEL - The Spy of God
Intelligence Gathering Module for Zohar Toolkit

This module performs advanced people intelligence gathering using 
the 'duckduckgo-search' library (DDGS) for robust, API-like access.

It now includes DEEP SCRAPING capabilities to visit identified URLs
and extract full text for PII analysis.

UPDATED v2.3.0:
- Separates "Confirmed Intelligence" from "Unverified Leads".
- Implements Confidence Scoring based on keyword triangulation.

Author: Zohar Toolkit
Version: 2.3.0 (Confidence Scoring & Sectioned Reporting)
"""

import time
import random
import json
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from duckduckgo_search import DDGS
from fake_useragent import UserAgent

class ZophielEngine:
    def __init__(self):
        self.ddgs = DDGS()
        self.ua = UserAgent()
        
        # Regex for US Phone Numbers
        self.phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        # Regex for potential Zip Codes
        self.zip_pattern = re.compile(r'\b\d{5}(?:-\d{4})?\b')
        # Regex for Emails
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    def _random_delay(self, min_s=1.0, max_s=2.0):
        """Injects human-like latency."""
        time.sleep(random.uniform(min_s, max_s))

    def search(self, query, max_results=5):
        """
        Executes a search query using DDGS.
        """
        print(f"[*] Zophiel Eye Scanning: {query}")
        self._random_delay()
        
        results = []
        try:
            ddg_gen = self.ddgs.text(query, region='us-en', max_results=max_results)
            for r in ddg_gen:
                results.append({
                    'title': r.get('title'),
                    'url': r.get('href'),
                    'snippet': r.get('body'),
                    'scraped_data': None # Placeholder
                })
        except Exception as e:
            print(f"[-] Search error: {e}")
        
        return results

    def _scrape_url(self, url):
        """
        Visits a URL and extracts visible text content.
        """
        print(f"    -> Deep Scraping: {url}...")
        try:
            headers = {'User-Agent': self.ua.random}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove scripts and styles
                for script in soup(["script", "style"]):
                    script.extract()
                
                # Get text
                text = soup.get_text(separator=' ')
                
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                clean_text = ' '.join(chunk for chunk in chunks if chunk)
                
                return clean_text
            else:
                print(f"       [x] Failed to access (Status: {response.status_code})")
                return None
        except Exception as e:
            print(f"       [x] Scraping error: {e}")
            return None

    def _extract_pii(self, text):
        """Scans text for PII patterns."""
        if not text:
            return {'phones': [], 'emails': []}
            
        phones = list(set(self.phone_pattern.findall(text)))
        emails = list(set(self.email_pattern.findall(text)))
        
        return {
            'phones': phones,
            'emails': emails
        }

    def _calculate_confidence(self, result, target_name, location=None):
        """
        Calculates a confidence score (0-100) for a result.
        """
        score = 0
        content = (result.get('title', '') + " " + result.get('snippet', '') + " " + str(result.get('scraped_content_preview', ''))).lower()
        
        name_parts = target_name.lower().split()
        
        # 1. Full Name Match (High Value)
        if target_name.lower() in content:
            score += 50
        # 2. Partial Name Match
        elif all(part in content for part in name_parts):
            score += 30
            
        # 3. Location Match (Critical Context)
        if location and location.lower() in content:
            score += 30
            
        # 4. Context Keywords (Family, Phone, Address)
        context_keywords = ["relative", "associate", "phone", "address", "age", "born", "aka"]
        if any(kw in content for kw in context_keywords):
            score += 10

        return min(score, 100)

    def _analyze_timeline(self, text, title):
        """
        Extracts years and potential life events from text.
        """
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
        events = []
        for year in set(years):
            # Find context around the year
            # Simple regex to get 5 words before and after
            try:
                snippet = re.search(r'((?:\S+\s+){0,10}' + year + r'(?:\s+\S+){0,10})', text)
                if snippet:
                    events.append({
                        "year": int(year),
                        "event": snippet.group(1).strip(),
                        "source": title
                    })
            except:
                pass
        return events

    def _calculate_cross_links(self, report):
        """
        Analyzes confirmed intelligence to find cross-link connections (e.g. shared usernames).
        """
        # Simple username extraction from URLs (e.g. facebook.com/username)
        usernames = []
        for item in report['confirmed_intelligence']:
            url = item.get('url', '')
            # Regex to find username-like patterns in URLs
            match = re.search(r'facebook\.com/([^/?]+)|twitter\.com/([^/?]+)|instagram\.com/([^/?]+)|linkedin\.com/in/([^/?]+)', url)
            if match:
                # Get the first non-None group
                username = next((g for g in match.groups() if g is not None), None)
                if username:
                    usernames.append({'username': username, 'source': item['title'], 'url': url})
        
        # Check for shared usernames across different platforms
        username_counts = {}
        for u in usernames:
            if u['username'] not in username_counts:
                username_counts[u['username']] = []
            username_counts[u['username']].append(u['source'])
            
        cross_links = []
        for user, sources in username_counts.items():
            if len(sources) > 1:
                cross_links.append({
                    'type': 'Shared Username',
                    'value': user,
                    'connected_sources': sources,
                    'significance': 'High - Indicates same individual across platforms'
                })
        
        return cross_links

    def _analyze_sentiment(self, text):
        """
        Basic sentiment/behavioral analysis on text.
        Returns a dictionary of detected traits.
        """
        traits = []
        text_lower = text.lower()
        
        # Behavioral keywords
        if any(w in text_lower for w in ['passionate', 'dedicated', 'advocate', 'volunteer']):
            traits.append('Community Oriented')
        if any(w in text_lower for w in ['entrepreneur', 'founder', 'ceo', 'owner']):
            traits.append('Business/Leadership')
        if any(w in text_lower for w in ['arrest', 'charged', 'court', 'lawsuit']):
            traits.append('Legal History')
        if any(w in text_lower for w in ['academic', 'university', 'research', 'published']):
            traits.append('Academic/Intellectual')
            
        return list(set(traits))

    def _generate_network_graph(self, report):
        """
        Generates a node-link structure for visualization.
        """
        nodes = []
        links = []
        added_nodes = set()
        
        # 1. Central Node (Target)
        target = report['target']
        nodes.append({"id": target, "group": "target", "radius": 20})
        added_nodes.add(target)
        
        # 2. PII Nodes
        for email in report['extracted_pii']['emails']:
            if email not in added_nodes:
                nodes.append({"id": email, "group": "email", "radius": 10})
                added_nodes.add(email)
            links.append({"source": target, "target": email, "value": 5})
            
        for phone in report['extracted_pii']['phones']:
            if phone not in added_nodes:
                nodes.append({"id": phone, "group": "phone", "radius": 10})
                added_nodes.add(phone)
            links.append({"source": target, "target": phone, "value": 5})
            
        # 3. Cross-Link Nodes (Usernames)
        for link in report['cross_links']:
            username = link['value']
            if username not in added_nodes:
                nodes.append({"id": username, "group": "username", "radius": 12})
                added_nodes.add(username)
            links.append({"source": target, "target": username, "value": 8})
            
            # Link username to source URLs
            for source in link['connected_sources']:
                # Truncate source for display
                source_short = (source[:30] + '..') if len(source) > 30 else source
                if source_short not in added_nodes:
                    nodes.append({"id": source_short, "group": "source", "radius": 5})
                    added_nodes.add(source_short)
                links.append({"source": username, "target": source_short, "value": 2})

        return {"nodes": nodes, "links": links}

    def ignite(self, target_name, location=None, employer=None):
        """
        Main Intelligence Gathering Sequence.
        Supports 'Comprehensive Investigation' parameters.
        """
        report = {
            "target": target_name,
            "location_context": location,
            "timestamp": datetime.now().isoformat(),
            "confirmed_intelligence": [], # High confidence (>70)
            "unverified_leads": [],       # Low confidence (<70)
            "extracted_pii": {
                "phones": [],
                "emails": []
            },
            "timeline": [],
            "cross_links": [],
            "behavioral_profile": [],
            "network_graph": {}
        }

        print(f"\n>>> ZOPHIEL PROTOCOL INITIATED FOR: {target_name}")
        
        # --- DEFINE SECTORS (Mapped from Master Prompt) ---
        sectors = {
            # 0. DEEP FILE HUNTER (Echelon Level)
            "file_hunter": f'"{target_name}" filetype:pdf OR "{target_name}" filetype:docx OR "{target_name}" filetype:xlsx OR "{target_name}" filetype:pptx',
            
            # 0.5 DARK WEB INDEX (Simulation via Clearweb Proxies)
            "dark_web_index": f'"{target_name}" site:onion.link OR "{target_name}" site:tor2web.org OR "{target_name}" "index of" onion OR "{target_name}" "hidden service"',

            # 0.6 LEAK & BREACH LOOKUP (Paste Sites)
            "leak_lookup": f'"{target_name}" site:pastebin.com OR "{target_name}" site:ghostbin.com OR "{target_name}" "password" filetype:txt OR "{target_name}" "dump" filetype:sql',

            # 1. Personal Background & Origins
            "background_origin": f'"{target_name}" biography OR "{target_name}" born in OR "{target_name}" early life OR "{target_name}" family background',
            
            # 2. Residential History
            "residential": f'"{target_name}" "{location}" address resident OR "{target_name}" property records OR "{target_name}" current address',
            
            # 3. Educational Background
            "education": f'"{target_name}" "{location}" school student graduate OR "{target_name}" alumni OR "{target_name}" university',
            
            # 4. Employment & Professional Ventures
            "employment": f'"{target_name}" "{location}" job title employer resume linkedin OR "{target_name}" business owner OR "{target_name}" founder',
            
            # 4.5 Global Business & Corporate Records (LLC/Inc)
            "global_business": f'"{target_name}" LLC OR "{target_name}" Ltd OR "{target_name}" Inc OR "{target_name}" Director OR "{target_name}" Shareholder OR "{target_name}" "registered agent"',

            # 5. Criminal & Legal Records
            "legal_criminal": f'"{target_name}" arrest mugshot court record "{location}" OR "{target_name}" lawsuit OR "{target_name}" criminal record',
            
            # 6. Financial Records (Public Mentions)
            "financial": f'"{target_name}" "{location}" bankrupt judgment lien tax OR "{target_name}" net worth',
            
            # 7. Social Media & Online Presence (PERMANENTLY DISABLED PER DIRECTIVE)
            # "social_media": f'"{target_name}" "{location}" site:instagram.com OR site:facebook.com OR site:twitter.com OR site:tiktok.com OR "{target_name}" site:youtube.com',
            
            # 8. Community Involvement & Reputation
            "community_reputation": f'"{target_name}" "{location}" volunteer church club member OR "{target_name}" controversy OR "{target_name}" scandal OR "{target_name}" achievement',
            
            # 9. Health (Public Mentions)
            "medical_public": f'"{target_name}" "{location}" hospital patient donor gofundme',
            
            # 10. Data Brokers (Targeted)
            "data_brokers": f'"{target_name}" "{location}" site:fastpeoplesearch.com OR site:truepeoplesearch.com OR site:familytreenow.com OR site:cyberbackgroundchecks.com',
            
            # 11. Image Search (Facial Rec via Context)
            "image_context": f'"{target_name}" "{location}" photo OR "{target_name}" "{location}" image OR "{target_name}" mugshot',

            # 12. BURIED INTELLIGENCE (Deep Web / Archives / Leaks)
            "buried_secrets": f'"{target_name}" site:pastebin.com OR "{target_name}" site:ghostproject.fr OR "{target_name}" site:doxbin.com OR "{target_name}" "index of" "parent directory" filetype:txt OR filetype:sql OR filetype:db',

            # 13. LEGAL & COURT ARCHIVES (Hard Records)
            "legal_archives": f'"{target_name}" site:courtlistener.com OR "{target_name}" site:justia.com OR "{target_name}" site:trellis.law OR "{target_name}" plaintiff OR "{target_name}" defendant OR "{target_name}" docket OR "{target_name}" judgment',

            # 14. PROPERTY & ASSET TRACING (Specific)
            "asset_tracing": f'"{target_name}" "property tax" OR "{target_name}" "deed" OR "{target_name}" "assessment" OR "{target_name}" "parcel id"'
        }

        # --- EXECUTE SCAN & SCRAPE ---
        all_results = []
        
        for sector, query in sectors.items():
            print(f"\n[+] Processing Sector: {sector.upper()}")
            # 1. Search
            results = self.search(query, max_results=3) 
            
            # 2. Scrape & Analyze
            for i, res in enumerate(results):
                self._random_delay(min_s=0.5, max_s=1.5)
                
                # Scrape
                scraped_text = self._scrape_url(res['url'])
                if scraped_text:
                    res['scraped_content_preview'] = scraped_text[:2000] 
                    
                    # Extract PII
                    pii = self._extract_pii(scraped_text)
                    if pii['phones'] or pii['emails']:
                        res['extracted_pii'] = pii
                        report['extracted_pii']['phones'].extend(pii['phones'])
                        report['extracted_pii']['emails'].extend(pii['emails'])
                
                # 3. Calculate Confidence
                confidence = self._calculate_confidence(res, target_name, location)
                res['confidence_score'] = confidence
                res['sector'] = sector
                
                # 3.5 Timeline Analysis
                if scraped_text:
                    timeline_events = self._analyze_timeline(scraped_text, res['title'])
                    report['timeline'].extend(timeline_events)
                    
                    # 3.6 Behavioral Analysis
                    traits = self._analyze_sentiment(scraped_text)
                    report['behavioral_profile'].extend(traits)

                # 4. Sort into Categories
                if confidence >= 70:
                    report['confirmed_intelligence'].append(res)
                else:
                    report['unverified_leads'].append(res)

        # --- CROSS-LINK ANALYSIS ---
        report['cross_links'] = self._calculate_cross_links(report)
        report['behavioral_profile'] = list(set(report['behavioral_profile']))

        # --- RECURSIVE INTELLIGENCE (The "Spider") ---
        # If we found phone numbers or emails, we hunt them down.
        unique_phones = list(set(report['extracted_pii']['phones']))
        unique_emails = list(set(report['extracted_pii']['emails']))
        
        if unique_phones or unique_emails:
            print(f"\n[!] RECURSIVE SPIDER ACTIVATED: Hunting {len(unique_phones)} phones and {len(unique_emails)} emails...")
            
            recursive_targets = unique_phones[:3] + unique_emails[:3] # Limit to avoid bans
            
            for target in recursive_targets:
                print(f"    -> Spidering: {target}")
                r_results = self.search(f'"{target}"', max_results=2)
                for r in r_results:
                     r['confidence_score'] = 95 # High confidence because it matched PII
                     r['sector'] = "recursive_pii_trace"
                     report['confirmed_intelligence'].append(r)
                     self._random_delay()

        # --- DEDUPLICATE GLOBAL PII ---
        report['extracted_pii']['phones'] = list(set(report['extracted_pii']['phones']))
        report['extracted_pii']['emails'] = list(set(report['extracted_pii']['emails']))

        # --- GENERATE NETWORK GRAPH ---
        report['network_graph'] = self._generate_network_graph(report)

        self._generate_report(report)
        self._save_json_report(report)
        return report

    def _generate_report(self, report):
        print(f"\n{'='*60}")
        print(f"ZOPHIEL INTELLIGENCE REPORT: {report['target']}")
        print(f"LOCATION CONTEXT: {report['location_context']}")
        print(f"{'='*60}")
        
        print(f"\n[***] CONFIRMED INTELLIGENCE (High Confidence Matches)")
        if not report['confirmed_intelligence']:
            print("    (None found)")
        for i, res in enumerate(report['confirmed_intelligence']):
            print(f"    {i+1}. [{res['confidence_score']}%] {res['title']}")
            print(f"       -> {res['url']}")
            if 'extracted_pii' in res:
                 print(f"       [!] PII: {res['extracted_pii']}")

        print(f"\n[?] UNVERIFIED LEADS (Requires Manual Verification)")
        print(f"    (Total: {len(report['unverified_leads'])} leads archived in JSON)")
        # Only show top 3 unverified to keep output clean
        for i, res in enumerate(report['unverified_leads'][:3]):
             print(f"    {i+1}. [{res['confidence_score']}%] {res['title']}")
             print(f"       -> {res['url']}")
        
        print(f"\n{'='*60}")
        print("[*] Scan Complete. The Eye Closes.")
        
        self._save_json_report(report)
        return report

    def _save_json_report(self, report):
        safe_name = report['target'].replace(" ", "_")
        filename = f"{safe_name}_Intel_Verified.json"
        
        # Ensure reports directory exists
        reports_dir = os.path.join(os.path.dirname(__file__), "Intelligence_Reports")
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
            
        print(f"[+] Report Archived: {filepath}")

if __name__ == "__main__":
    # Interactive Mode support or CLI args
    import sys
    if len(sys.argv) > 1:
        # CLI Mode: python zophiel_core.py "Name" "Loc" "Emp"
        name = sys.argv[1]
        loc = sys.argv[2] if len(sys.argv) > 2 else None
        emp = sys.argv[3] if len(sys.argv) > 3 else None
        
        engine = ZophielEngine()
        engine.ignite(name, loc, emp)
    else:
        # Interactive
        print("ZOPHIEL | People Intelligence Module")
        name = input("Target Name: ")
        loc = input("Location (Optional): ")
        emp = input("Employer (Optional): ")
        
        engine = ZophielEngine()
        engine.ignite(name, loc, emp)
