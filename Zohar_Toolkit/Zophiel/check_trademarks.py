from zophiel_core import ZophielEngine

def check_trademarks():
    engine = ZophielEngine()
    print("\n>>> TRADEMARK INTELLIGENCE SCAN: GG33")
    
    # Trademark specific queries
    queries = [
        'site:uspto.report "GG33" owner',
        'site:trademarkia.com "GG33" Gary Grinberg',
        'site:justia.com trademark "GG33"',
        '"Gary Grinberg" fraud lawsuit 2003 NY details' # Digging deeper into the fraud case
    ]
    
    for q in queries:
        results = engine.search(q, max_results=3)
        for r in results:
            print(f"FOUND: {r['title']} -> {r['url']}")
            print(f"SNIPPET: {r['snippet']}\n")

if __name__ == "__main__":
    check_trademarks()
