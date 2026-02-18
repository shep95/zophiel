import json
import os
import time
from datetime import datetime

class TheOracle:
    """
    THE ORACLE: The Shared Mind.
    Central knowledge repository for all agents (Hermes, Hades, Oculus, Anubis) to share intelligence.
    
    "The Agents must work together, not separately."
    """
    def __init__(self, db_path):
        self.db_path = db_path
        # Schema for the Knowledge Base
        self.knowledge = {
            "meta": {
                "created_at": str(datetime.now()),
                "last_updated": str(datetime.now())
            },
            "domains": {
                # "openai.com": {"subdomains": [...], "technologies": [...]}
            },
            "intelligence": {
                "waf_bypass_rules": [], # ["unified-X pattern bypasses Cloudflare"]
                "alive_endpoints": [],  # ["https://api.unified-6..."]
                "secrets_found": [],    # [{"type": "jwt", "value": "...", "source": "..."}]
                "interesting_files": [] # ["https://.../main.js"]
            },
            "history": [] # Audit log of agent actions
        }
        self.load()

    def load(self):
        """Load knowledge from disk"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    # Merge or update
                    self.knowledge.update(data)
                print(f"[ORACLE] Knowledge Base loaded from {self.db_path}")
            except Exception as e:
                print(f"[ORACLE] Failed to load Knowledge Base: {e}")
        else:
            print(f"[ORACLE] No existing memory found. Creating new Knowledge Base.")
            self.save()

    def save(self):
        """Persist knowledge to disk"""
        self.knowledge["meta"]["last_updated"] = str(datetime.now())
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.knowledge, f, indent=4)
        except Exception as e:
            print(f"[ORACLE] CRITICAL: Failed to save memory: {e}")

    def add_subdomains(self, main_domain, subdomains):
        """Hermes feeds discovered subdomains here"""
        if main_domain not in self.knowledge["domains"]:
            self.knowledge["domains"][main_domain] = {"subdomains": []}
        
        # Unique merge
        current = set(self.knowledge["domains"][main_domain].get("subdomains", []))
        new_subs = set(subdomains)
        updated = list(current.union(new_subs))
        
        self.knowledge["domains"][main_domain]["subdomains"] = updated
        self.log("Hermes", f"Added {len(new_subs)} subdomains for {main_domain}")
        self.save()

    def add_alive_host(self, url, status_code, server_header=None):
        """Hades feeds reachable hosts here"""
        entry = {
            "url": url,
            "status": status_code,
            "server": server_header,
            "timestamp": str(datetime.now())
        }
        # Check if already exists to avoid duplicates (naive check)
        exists = any(x['url'] == url for x in self.knowledge["intelligence"]["alive_endpoints"])
        if not exists:
            self.knowledge["intelligence"]["alive_endpoints"].append(entry)
            
            # Learning Logic: WAF Analysis
            if status_code in [404, 401, 200] and "unified" in url:
                self.learn_waf_rule(f"Shard '{url}' is reachable (Status: {status_code}). WAF likely bypassed.")
                
            self.save()

    def learn_waf_rule(self, rule):
        """Record a WAF behavior or bypass technique"""
        if rule not in self.knowledge["intelligence"]["waf_bypass_rules"]:
            self.knowledge["intelligence"]["waf_bypass_rules"].append(rule)
            self.log("Hades", f"Learned WAF Rule: {rule}")
            self.save()

    def add_secret(self, secret_type, value, source):
        """Oculus feeds findings here"""
        entry = {
            "type": secret_type,
            "value": value,
            "source": source,
            "timestamp": str(datetime.now())
        }
        self.knowledge["intelligence"]["secrets_found"].append(entry)
        self.log("Oculus", f"FOUND SECRET: {secret_type} in {source}")
        self.save()

    def get_subdomains(self, main_domain):
        """Retrieve subdomains for a target"""
        return self.knowledge["domains"].get(main_domain, {}).get("subdomains", [])

    def get_alive_hosts(self):
        """Retrieve reachable hosts for scanning"""
        return [x['url'] for x in self.knowledge["intelligence"]["alive_endpoints"]]

    def log(self, agent, message):
        """Audit trail"""
        print(f"[{agent.upper()}] {message}")
        self.knowledge["history"].append(f"[{datetime.now()}] [{agent}] {message}")
