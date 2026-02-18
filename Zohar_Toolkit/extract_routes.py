import json
import re

FILE = r"c:\Users\kille\Documents\trae_projects\osint_links\Zohar_Toolkit\Intelligence_Database\OpenAI\Backend_Code\Frontend_JS_Bundles\manifest-91bbfafc.js"

def extract_routes():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract JSON object
        match = re.search(r"window\.__reactRouterManifest\s*=\s*(\{.*?\});", content)
        if match:
            json_str = match.group(1)
            # Basic cleanup if needed (though re.search should grab valid json if it's one block)
            # The file is minified, so the regex needs to be greedy enough but stop at the semicolon
            # Actually, regex for nested JSON is hard. Let's try to just find "path":"..." patterns.
            
            paths = re.findall(r'"path"\s*:\s*"([^"]+)"', content)
            ids = re.findall(r'"id"\s*:\s*"([^"]+)"', content)
            
            print(f"Found {len(paths)} paths.")
            
            print("\n=== ROUTE MAP ===")
            for p in sorted(set(paths)):
                print(f"- {p}")
                
            print("\n=== ID MAP (Hidden Routes?) ===")
            for i in sorted(set(ids)):
                if "debug" in i or "admin" in i or "test" in i or "internal" in i:
                    print(f"- {i}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_routes()
