from zophiel_core import ZophielEngine
import json

class BusinessIntelEngine(ZophielEngine):
    def ignite_business_scan(self, target_name, location):
        """
        Specialized scan for Corporate Filings and Legal Business Entities.
        """
        print(f"\n>>> CORPORATE INTELLIGENCE SCAN: {target_name} [{location}]")
        
        # Focused queries for official business records
        sectors = {
            "florida_sunbiz": f'site:search.sunbiz.org "{target_name}" OR site:search.sunbiz.org "GG33"',
            "opencorporates": f'site:opencorporates.com "{target_name}" "{location}"',
            "bizapedia": f'site:bizapedia.com "{target_name}" "{location}"',
            "corporate_wiki": f'site:corporationwiki.com "{target_name}" "{location}"',
            "general_llc": f'"{target_name}" LLC registration "{location}" OR "{target_name}" Inc incorporation',
            "gg33_entity": f'"GG33 Academy" business license OR "GG33" LLC owner',
            "ppp_loans": f'"{target_name}" PPP loan OR "{target_name}" SBA loan'
        }

        report = {
            "target": target_name,
            "scan_type": "Corporate Entity Search",
            "findings": []
        }

        for sector, query in sectors.items():
            print(f"\n[+] Querying Registry: {sector.upper()}")
            results = self.search(query, max_results=4)
            
            for res in results:
                # Scrape for deeper context
                self._random_delay(0.5, 1.0)
                scraped_text = self._scrape_url(res['url'])
                
                # Simple relevance check
                if scraped_text:
                    content_lower = scraped_text.lower()
                    if target_name.lower() in content_lower or "gg33" in content_lower:
                        res['verified_match'] = True
                        res['source_registry'] = sector
                        report['findings'].append(res)
                        print(f"   [!] POTENTIAL MATCH: {res['title']}")
        
        self._save_business_report(report)

    def _save_business_report(self, report):
        filename = f"{report['target'].replace(' ', '_')}_Business_Intel.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"\n[+] Business Intelligence Saved: {filename}")

if __name__ == "__main__":
    scanner = BusinessIntelEngine()
    scanner.ignite_business_scan("Gary Grinberg", "Miami")
