import os

ASSETS_DIR = r"Zohar_Toolkit/Intelligence_Database/OpenAI/Bug_Bounty/Leaked_Assets"

INTERESTING_FILES = {
    "1a7ebd5f-ihenykhpblfwilpu.js": ["/backend-api/f/conversation", "sentinel", "pricing_rollout_gate"],
    "d70d5a79-dclbvm9m6cqvo0bj.js": ["in_shared_projects_gate"],
    "4813494d-di0bpg5zidu9s57f.js": ["feature_gates", "gate_evaluation"],
    "0bb44966-nomjbrnmr4xambs9.js": ["use forget", "spacingAbove"], # The one user opened
}

def extract_context():
    print("Starting Context Extraction...\n")
    
    for filename, keywords in INTERESTING_FILES.items():
        filepath = os.path.join(ASSETS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename} (not found)")
            continue
            
        print(f"--- Analyzing {filename} ---")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for kw in keywords:
                start_idx = 0
                while True:
                    idx = content.find(kw, start_idx)
                    if idx == -1:
                        break
                    
                    # Extract context
                    context_start = max(0, idx - 100)
                    context_end = min(len(content), idx + len(kw) + 100)
                    snippet = content[context_start:context_end].replace('\n', ' ')
                    
                    print(f"\n[MATCH] '{kw}'")
                    print(f"Context: ...{snippet}...")
                    
                    start_idx = idx + 1
                    
        except Exception as e:
            print(f"Error reading {filename}: {e}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    extract_context()
