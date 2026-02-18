import json
import os

def analyze():
    path = r"c:\Users\kille\Documents\trae_projects\osint_links\Intelligence_Database\X_Corp\Reports\DEEP_SCAN_FINDINGS.json"
    
    if not os.path.exists(path):
        print("Findings file not found.")
        return

    with open(path, "r") as f:
        data = json.load(f)

    print(f"Loaded findings for {len(data)} urls.")
    
    high_value_keys = [
        "twitter_bearer", "twitter_csrf", "slack_webhook", "discord_webhook", 
        "private_key", "aws_key", "google_api", "openai_sk", "supabase_key", 
        "algolia_key", "generic_secret"
    ]
    
    found_high_value = False
    
    for url, findings in data.items():
        for key_type, values in findings.items():
            if key_type in high_value_keys:
                print(f"\n[CRITICAL] {key_type} found in {url}")
                for v in set(values):
                    print(f"  - {v[:100]}...") # Truncate long keys for safety/display
                found_high_value = True
            
            # Filter developer comments for interesting stuff
            if key_type == "developer_comment":
                for comment_tuple in values:
                    # comment_tuple is likely a list [match, context] or just string
                    # The regex returns tuples if groups are used.
                    # My regex was: r"(TODO|FIXME|HACK|Author|Created by|Dev|Maintainer)[:\s]+(.*?)(?=\n|$)"
                    # This returns a tuple (Keyword, Content)
                    
                    if isinstance(comment_tuple, list) or isinstance(comment_tuple, tuple):
                        content = comment_tuple[1] if len(comment_tuple) > 1 else comment_tuple[0]
                    else:
                        content = comment_tuple
                        
                    content = str(content).lower()
                    if any(x in content for x in ["secret", "password", "credential", "key ", "token", "internal"]):
                        print(f"\n[INTERESTING COMMENT] {url}")
                        print(f"  - {comment_tuple}")

    if not found_high_value:
        print("\n[-] No CRITICAL keys found (AWS, Slack, Twitter Bearer, etc).")

if __name__ == "__main__":
    analyze()
