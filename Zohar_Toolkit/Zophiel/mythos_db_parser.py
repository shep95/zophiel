import json
import os
import re

INPUT_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'MYTHOS_DB', 'FULL_MYTHOS_DB.txt')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'Intelligence_Reports', 'MYTHOS_DB', 'MYTHOS_RECONSTRUCTED_DB.json')

def parse_db():
    print("[*] Parsing extracted text data into structured JSON...")
    
    if not os.path.exists(INPUT_FILE):
        print("[-] Input file not found!")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    db = {
        "metadata": {
            "source": "mythoshub.com",
            "extraction_date": "2026-02-10",
            "status": "PARTIAL_RECONSTRUCTION"
        },
        "numerology": {},
        "mbti": {},
        "blood_type": {}
    }

    # --- Parse Numerology ---
    # Look for "1\nThe Leader\nLeadership..." pattern
    # This is tricky with regex, we'll try a block approach
    
    num_section = re.search(r'NUMEROLOGY.*?Grid(.*?)Select a number', content, re.DOTALL)
    if num_section:
        raw_text = num_section.group(1)
        # Regex to find Number, Title, Keywords
    # Use lookahead (?=) to ensure we don't consume the start of the next block
    matches = re.findall(r'\n(\d+)\s*\n(.*?)\n(.*?)(?=\n\d+|\nSelect)', raw_text, re.DOTALL)
    for num, title, keywords in matches:
        db['numerology'][num] = {
            "archetype": title.strip(),
            "keywords": keywords.strip()
        }
            
    # --- Parse Blood Type ---
    # Pattern: Type\n(.*?)\n(.*?)\n(.*?)\n% Global
    bt_matches = re.findall(r'Type\n(.*?)\n(.*?)\n(.*?)\n% Global', content)
    for b_type, title, percent in bt_matches:
        db['blood_type'][b_type.strip()] = {
            "archetype": title.strip(),
            "rarity": f"{percent.strip()}%"
        }

    # --- Parse MBTI ---
    # The text didn't contain the definitions, just the "Assessment" page text.
    # So we leave MBTI empty or just note it exists.
    db['mbti']['note'] = "Definitions not found in public scrape. System uses Cognitive Functions (Jungian)."

    # Save
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2)
        
    print(f"[+] Reconstructed Database saved to {OUTPUT_FILE}")
    print(json.dumps(db, indent=2))

if __name__ == "__main__":
    parse_db()
