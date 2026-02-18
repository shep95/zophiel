import sys
import os
import json

# Ensure parent directories are in path to import Zophiel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Zohar_Toolkit.Zophiel.zophiel_core import ZophielEngine

def run_vedic_research():
    print("==================================================")
    print("   ZOPHIEL: VEDIC KNOWLEDGE ACQUISITION PROTOCOL")
    print("==================================================")
    
    engine = ZophielEngine()
    
    # Advanced/Elite topics to research
    topics = [
        "Vedic Astrology", # Simple test
        "Shashtyamsha D60 chart analysis techniques advanced",
        "Bhrigu Nandi Nadi secret prediction rules",
        "Gandanta points psychological effects vedic astrology",
        "Sarvatobhadra Chakra vedh techniques",
        "Panchanguli Sadhana for astrologers",
        "Rahu Ketu karmic axis secret meanings",
        "Nakshatra Padas advanced interpretation",
        "Atmakaraka in Navamsa chart secrets"
    ]
    
    knowledge_base = []
    
    for topic in topics:
        print(f"\n[+] Initiating deep search for: {topic}")
        try:
            results = engine.search(topic, max_results=3)
            print(f"    -> Found {len(results)} search results.")
        except Exception as e:
            print(f"    [!] Search failed: {e}")
            results = []
        
        for res in results:
            url = res.get('url')
            title = res.get('title')
            print(f"    -> Processing: {title} ({url})")
            
            # Deep Scrape
            content = engine._scrape_url(url)
            
            if content:
                # Basic cleaning to reduce noise
                # Limit content length to avoid massive dumps of irrelevant footer text
                content_snippet = content[:5000] 
                
                entry = {
                    "topic": topic,
                    "title": title,
                    "url": url,
                    "content": content_snippet
                }
                knowledge_base.append(entry)
                print(f"    -> Acquired {len(content_snippet)} chars of gnosis.")
            
    # Generate Report
    report_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'VEDIC_ASTROLOGY_ELITE_KNOWLEDGE.txt')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("ZOPHIEL INTELLIGENCE REPORT: ELITE VEDIC KNOWLEDGE\n")
        f.write("==================================================\n\n")
        
        for item in knowledge_base:
            f.write(f"TOPIC: {item['topic']}\n")
            f.write(f"SOURCE: {item['title']} ({item['url']})\n")
            f.write("-" * 50 + "\n")
            f.write(item['content'])
            f.write("\n\n" + "=" * 50 + "\n\n")
            
    print(f"\n[+] Knowledge acquisition complete. Grimoire saved to: {report_path}")

if __name__ == "__main__":
    run_vedic_research()
