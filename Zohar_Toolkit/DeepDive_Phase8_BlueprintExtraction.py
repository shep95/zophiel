import json
import re
import os

def extract_blueprints():
    print("=== EXTRACTING INTERNAL BLUEPRINTS & SCHEMAS ===")
    
    leaked_dir = "Intelligence_Database/OpenAI/Leaked_Assets"
    findings = []

    for filename in os.listdir(leaked_dir):
        if filename.endswith(".ipynb"):
            path = os.path.join(leaked_dir, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    
                # Scan cells
                for cell in content.get("cells", []):
                    source = "".join(cell.get("source", []))
                    
                    # 1. Look for System Prompts / Templates
                    if "<" in source and ">" in source and ("system" in source.lower() or "prompt" in source.lower()):
                         # Extract things that look like XML tags used in prompts
                        tags = re.findall(r"<([a-zA-Z0-9_]+)>", source)
                        if tags:
                            findings.append({
                                "file": filename,
                                "type": "Prompt Template",
                                "content": source[:500] + "...",
                                "tags": list(set(tags))
                            })

                    # 2. Look for JSON Schemas / API Definitions
                    if "class " in source and "Model" in source:
                        findings.append({
                            "file": filename,
                            "type": "Backend Schema (Class)",
                            "content": source[:500] + "..."
                        })
                    
                    if "def " in source and "tool" in source.lower():
                         findings.append({
                            "file": filename,
                            "type": "Internal Tool Definition",
                            "content": source[:500] + "..."
                        })

            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # Report
    with open("Intelligence_Database/OpenAI/Reports/INTERNAL_BLUEPRINTS.md", "w", encoding="utf-8") as f:
        f.write("# 🏗️ INTERNAL BLUEPRINTS (Extracted from Leaks)\n\n")
        for item in findings:
            f.write(f"## {item['type']} (Source: `{item['file']}`)\n")
            f.write(f"**Extracted Logic:**\n```python\n{item['content']}\n```\n")
            if "tags" in item:
                f.write(f"**Detected System Tags:** `{', '.join(item['tags'])}`\n")
            f.write("\n---\n")

    print(f"Extraction complete. Found {len(findings)} blueprint artifacts.")

if __name__ == "__main__":
    extract_blueprints()
