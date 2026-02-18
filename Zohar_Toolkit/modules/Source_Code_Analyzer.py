import os
import re
import sys
import json
import time

# Ensure Zohar_Toolkit root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Source_Code_Analyzer:
    """
    RAZIEL MODULE: SOURCE CODE ANALYZER
    Analyzes beautified JS files for hardcoded secrets, API endpoints, and feature flags.
    """
    
    def __init__(self, input_dir="Intelligence_Database/Notion/Source_Code"):
        self.input_dir = input_dir
        self.findings = {
            "secrets": [],
            "endpoints": [],
            "feature_flags": [],
            "internal_domains": []
        }
        
        # Regex Patterns
        self.patterns = {
            'api_route': r'["\'](/backend-api/[a-zA-Z0-9-_/]+|/public-api/[a-zA-Z0-9-_/]+|/v1/[a-zA-Z0-9-_/]+|/api/[a-zA-Z0-9-_/]+)["\']',
            'deep_research': r'["\'](/[a-zA-Z0-9-_/]*deep-research[a-zA-Z0-9-_/]*)["\']',
            'supabase_key': r'sb-[a-zA-Z0-9-]{20,}',
            'generic_key': r'(?i)(api_key|access_token|secret)["\']?\s*[:=]\s*["\']([a-zA-Z0-9-_]{20,})["\']',
            'feature_gate': r'["\']([a-zA-Z0-9-_]*gate[a-zA-Z0-9-_]*)["\']',
            'internal_domain': r'https?://[a-zA-Z0-9.-]*notion[a-zA-Z0-9.-]*\.(com|so|net|org)',
            'uuid': r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        }

    def log(self, message, level="INFO"):
        print(f"[{level}] {message}")

    def analyze_files(self):
        self.log(f"Scanning directory: {self.input_dir}", "ANALYZER")
        
        if not os.path.exists(self.input_dir):
            self.log("Directory not found!", "ERROR")
            return

        for filename in os.listdir(self.input_dir):
            if filename.endswith(".js"):
                filepath = os.path.join(self.input_dir, filename)
                self.log(f"Analyzing {filename}...", "SCAN")
                
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    # Scan for patterns
                    for name, pattern in self.patterns.items():
                        matches = re.findall(pattern, content)
                        if matches:
                            unique_matches = list(set(matches))
                            self.log(f"  [+] Found {len(unique_matches)} {name}(s)", "HIT")
                            
                            if name == 'generic_key' or name == 'supabase_key':
                                self.findings['secrets'].extend([{"file": filename, "match": m} for m in unique_matches])
                            elif name == 'api_route':
                                self.findings['endpoints'].extend([{"file": filename, "match": m} for m in unique_matches])
                            elif name == 'feature_gate':
                                self.findings['feature_flags'].extend([{"file": filename, "match": m} for m in unique_matches])
                            elif name == 'internal_domain':
                                self.findings['internal_domains'].extend([{"file": filename, "match": m} for m in unique_matches])
                                
                except Exception as e:
                    self.log(f"Error reading {filename}: {e}", "ERROR")

    def generate_report(self):
        report_path = os.path.join(self.input_dir, "Analysis_Report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.findings, f, indent=4)
        self.log(f"Report saved to {report_path}", "SUCCESS")
        
        # Print Summary
        print("\n=== ANALYSIS SUMMARY ===")
        print(f"Secrets Found: {len(self.findings['secrets'])}")
        print(f"Endpoints Found: {len(self.findings['endpoints'])}")
        print(f"Feature Flags Found: {len(self.findings['feature_flags'])}")
        print(f"Internal Domains: {len(self.findings['internal_domains'])}")

if __name__ == "__main__":
    analyzer = Source_Code_Analyzer()
    analyzer.analyze_files()
    analyzer.generate_report()
