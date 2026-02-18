import re

file_path = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\Legacy_Targets\Toolkit_Archives\aureon_investig\index-DNF4kIq3.js"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'key:"(eyJ[^"]+)"', content)
        if match:
            print(f"FOUND_KEY: {match.group(1)}")
        else:
            # Try alternative patterns if the first one fails
            # Sometimes it's anonKey: "..." or supabaseKey: "..."
            match2 = re.search(r'anonKey:"(eyJ[^"]+)"', content)
            if match2:
                 print(f"FOUND_KEY: {match2.group(1)}")
            else:
                 print("KEY_NOT_FOUND")
except Exception as e:
    print(f"Error: {e}")
