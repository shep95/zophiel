import re

FILE_PATH = r"c:\Users\kille\Documents\trae_projects\osint_links\Zohar_Toolkit\main_bundle.js"

# Focused keywords for deep analysis
KEYWORDS = ["client_feature_switch", "deep_research_in_context_upsell"]

def analyze_file():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            
        print(f"File size: {len(content)} bytes")
        
        for keyword in KEYWORDS:
            matches = [m.start() for m in re.finditer(re.escape(keyword), content)]
            if matches:
                print(f"\n[+] Found '{keyword}' at {len(matches)} locations:")
                for pos in matches[:5]: # Show first 5
                    # Expanded context to understand the parsing logic
                    start = max(0, pos - 500)
                    end = min(len(content), pos + 500)
                    snippet = content[start:end].replace("\n", " ")
                    print(f"    ...{snippet}...")
            else:
                print(f"[-] '{keyword}' not found.")
                
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    analyze_file()
