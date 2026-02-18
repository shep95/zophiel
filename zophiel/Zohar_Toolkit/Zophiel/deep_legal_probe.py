from zophiel_core import ZophielEngine
import re

def deep_legal_probe():
    engine = ZophielEngine()
    print("\n>>> DEEP LEGAL PROBE: NATIONWIDE v. GRINBERG (2003 RICO)")
    
    # 1. Find Case Number and Co-Conspirators
    queries = [
        '"Nationwide Mutual Insurance" v "Gary Grinberg" lawsuit text',
        '"Alex Buziashvili" "Gary Grinberg" RICO indictment',
        '"Gary Grinberg" New York insurance fraud 2003 "no-fault"',
        '"Gary Grinberg" arrest record Staten Island'
    ]
    
    for q in queries:
        print(f"\n[*] Probing: {q}")
        results = engine.search(q, max_results=3)
        for r in results:
            print(f"   -> Found: {r['title']}")
            print(f"      URL: {r['url']}")
            
            # Deep Scrape for Case ID
            content = engine._scrape_url(r['url'])
            if content:
                # Look for patterns like "Case No. 03-CV..." or "Index No."
                case_patterns = re.findall(r'(Case\s+No\.?|Index\s+No\.?)\s*[:#]?\s*(\w+[-\d]+)', content, re.IGNORECASE)
                if case_patterns:
                    print(f"      [!] POTENTIAL CASE ID: {case_patterns}")
                
                # Look for specific allegations
                if "racketeering" in content.lower() or "fraud" in content.lower():
                    print(f"      [!] CONFIRMED FRAUD CONTEXT in {r['url']}")

if __name__ == "__main__":
    deep_legal_probe()
