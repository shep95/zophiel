import os
import re
import json
import sys

# Ensure Zohar_Toolkit is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HiveMind.HiveMind import HiveMind

class CommsHunter:
    def __init__(self):
        self.js_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Intelligence_Database", "OpenAI", "Backend_Code", "Frontend_JS_Bundles")
        self.brain = HiveMind()
        self.findings = {
            "slack_channels": set(),
            "internal_domains": set(),
            "sso_endpoints": set(),
            "email_addresses": set()
        }

    def hunt(self):
        print(f"[*] Starting Comms Hunt in {self.js_dir}...")
        
        if not os.path.exists(self.js_dir):
            print(f"[!] Error: Directory {self.js_dir} not found. Run Phase 11 first.")
            return

        # Regex Patterns
        patterns = {
            "slack": r'(?i)slack\.com\/archives\/[A-Z0-9]+',
            "internal_domain": r'(?i)([a-z0-9-]+\.openai\.com|[a-z0-9-]+\.internal)',
            "sso": r'(?i)(sso|auth0|okta)',
            "email": r'[a-zA-Z0-9._%+-]+@openai\.com'
        }

        files = [f for f in os.listdir(self.js_dir) if f.endswith('.js')]
        
        for file in files:
            path = os.path.join(self.js_dir, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Scan for Slack
                    slacks = re.findall(patterns["slack"], content)
                    self.findings["slack_channels"].update(slacks)
                    
                    # Scan for Internal Domains
                    domains = re.findall(patterns["internal_domain"], content)
                    # Filter out common public ones
                    public_domains = {'api.openai.com', 'platform.openai.com', 'help.openai.com', 'chat.openai.com', 'cdn.openai.com'}
                    for d in domains:
                        if d not in public_domains:
                            self.findings["internal_domains"].add(d)
                            
                    # Scan for SSO
                    if re.search(patterns["sso"], content):
                        # Extract context if possible, for now just marking file
                        self.findings["sso_endpoints"].add(f"Ref in {file}")

                    # Scan for Emails
                    emails = re.findall(patterns["email"], content)
                    self.findings["email_addresses"].update(emails)

            except Exception as e:
                print(f"[!] Error reading {file}: {e}")

        self.report_and_save()

    def report_and_save(self):
        print("\n[+] --- Comms Hunt Results ---")
        
        print(f"\n[+] Internal Domains Found: {len(self.findings['internal_domains'])}")
        for d in list(self.findings['internal_domains'])[:10]: # Show top 10
            print(f"  - {d}")
            
        print(f"\n[+] Emails Found: {len(self.findings['email_addresses'])}")
        for e in list(self.findings['email_addresses'])[:5]:
            print(f"  - {e}")

        # Save to Brain
        print("\n[*] Uploading intelligence to HiveMind Brain...")
        
        # Add Domains to Arsenal (as potential targets)
        for domain in self.findings["internal_domains"]:
            self.brain.add_target(f"https://{domain}", "Internal Domain Discovery")
            
        # Add Emails as "Users" (conceptually) or just notes
        # For now, we'll store them in a new "Comms" section of the brain manually
        # Or just use the brain's "knowledge" if we had that.
        # Let's add them as 'intel' notes in the brain.
        
        intel_data = {
            "internal_domains": list(self.findings["internal_domains"]),
            "emails": list(self.findings["email_addresses"]),
            "slack_refs": list(self.findings["slack_channels"])
        }
        
        # We need to expose a way to save generic intel to the brain.
        # I'll update the brain file directly for now or extend the class later.
        # For this step, I will just dump a JSON report for the user to see.
        
        with open("Comms_Intel.json", "w") as f:
            json.dump(intel_data, f, indent=2)
            print("[*] Saved full intel to Comms_Intel.json")

if __name__ == "__main__":
    hunter = CommsHunter()
    hunter.hunt()
