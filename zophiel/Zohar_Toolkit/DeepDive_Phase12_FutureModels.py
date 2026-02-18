import re
import os
import sys

# Ensure we can import HiveMind
sys.path.append(os.path.join(os.path.dirname(__file__), "HiveMind"))
try:
    from HiveMind import HiveMind
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from HiveMind.HiveMind import HiveMind

class FutureModelHunter:
    def __init__(self):
        self.mind = HiveMind()
        self.js_dir = "loot/js_assets"
        self.keywords = [
            "gpt-6", "gpt6", "gpt-next", "gpt-7", 
            "arrakis", "gobi", "sahara", "orion", # Known rumors
            "prototype", "research-v2", "deep-research",
            "model-v-next", "future-model",
            "internal-preview", "canary-model"
        ]
        self.findings = {}

    def scan_files(self):
        if not os.path.exists(self.js_dir):
            print("[-] No JS loot found. Run Phase 11 first.")
            return

        print(f"[*] Scanning {len(os.listdir(self.js_dir))} files for Future Models: {self.keywords}")
        
        for filename in os.listdir(self.js_dir):
            if not filename.endswith(".js"): continue
            
            path = os.path.join(self.js_dir, filename)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            for kw in self.keywords:
                # Case insensitive search
                matches = re.finditer(f"({kw})", content, re.IGNORECASE)
                for m in matches:
                    # Get context (50 chars before/after)
                    start = max(0, m.start() - 50)
                    end = min(len(content), m.end() + 50)
                    context = content[start:end].replace("\n", " ")
                    
                    if kw not in self.findings:
                        self.findings[kw] = []
                    
                    # Dedup
                    if context not in self.findings[kw]:
                        self.findings[kw].append(context)
                        print(f"    [!!!] FOUND TRACE: '{kw}' in {filename}")
                        print(f"          Context: ...{context}...")

    def run(self):
        print("=== Zohar Phase 12: Future Model Hunter (GPT-6/Codenames) ===")
        self.scan_files()
        
        if self.findings:
            print("\n=== FINDINGS SUMMARY ===")
            for kw, contexts in self.findings.items():
                print(f"[*] {kw}: {len(contexts)} occurrences")
                
            # Update Brain?
            # For now just print, user wants to know "what is next"
            
if __name__ == "__main__":
    hunter = FutureModelHunter()
    hunter.run()
