import requests
import json
import os
from dotenv import load_dotenv
from data_models import Finding, FindingType
from enum import Enum
import logging
from graph_db import GraphDB
from pipeline import Pipeline
from mutation import MutationEngine

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Finding):
            from dataclasses import asdict
            return asdict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("ANON_KEY")

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}

# Common table names in Supabase/Postgres apps
candidates = [
    "users", "profiles", "accounts", "public_users",
    "posts", "comments", "replies", "likes", "reactions",
    "follows", "followers", "relationships",
    "messages", "direct_messages", "chats", "chat_rooms", "conversations",
    "notifications", "activities", "events",
    "transactions", "orders", "payments", "wallets", "balances",
    "products", "items", "inventory",
    "settings", "config", "app_config",
    "audit_logs", "logs", "errors",
    "reports", "feedback", "support_tickets",
    "banned_users", "blocked_users",
    "roles", "permissions", "admin"
]

if __name__ == "__main__":
    # Initialize components
    graph_db = GraphDB()
    pipeline = Pipeline(graph_db)
    mutation_engine = MutationEngine(graph_db)

    # 1. Process existing findings to learn patterns
    logging.info("Learning from existing findings...")
    pipeline.process_findings()
    mutation_engine.learn_from_successful_findings()
    logging.info(f"Learned {len(mutation_engine.get_patterns())} patterns.")

    # 2. Get mutations
    mutated_candidates = mutation_engine.get_prioritized_mutations(count=50)
    logging.info(f"Generated {len(mutated_candidates)} mutations.")
    
    # Add mutations to the candidate list (basic extraction)
    # This part is conceptual and needs a robust implementation
    new_candidates = [m.split('/')[-1] for m in mutated_candidates if '/{resource}' not in m] 
    extended_candidates = list(set(candidates + new_candidates))

    logging.info(f"Probing {len(extended_candidates)} potential tables on {URL}...")

    all_findings = []

    for table in extended_candidates:
        url = f"{URL}/rest/v1/{table}?select=*&limit=1"
        try:
            resp = requests.get(url, headers=headers)
            
            if resp.status_code == 200:
                logging.info(f"FOUND: '{table}' (200 OK)")
                data = resp.json()
                metadata = {"table_name": table, "status": "open"}
                if data:
                    logging.info(f"    -> Contains data! Sample keys: {list(data[0].keys())}")
                    metadata["contains_data"] = True
                    metadata["sample_keys"] = list(data[0].keys())
                else:
                    logging.info(f"    -> Empty.")
                    metadata["contains_data"] = False
                
                finding = Finding(
                    value=f"Discovered table: {table}",
                    type=FindingType.ENDPOINT,
                    source_module="discover_tables",
                    target=url,
                    confidence=0.9,
                    metadata=metadata
                )
                all_findings.append(finding)

            elif resp.status_code == 401:
                logging.warning(f"LOCKED: '{table}' (401 Unauthorized - RLS likely)")
                finding = Finding(
                    value=f"Discovered (locked) table: {table}",
                    type=FindingType.ENDPOINT,
                    source_module="discover_tables",
                    target=url,
                    confidence=0.7,
                    metadata={"table_name": table, "status": "locked"}
                )
                all_findings.append(finding)
            
        except Exception as e:
            logging.error(f"Error probing {table}: {e}")

    logging.info("Discovery Complete.")
    if all_findings:
        findings_filename = os.path.join("output", "discover_tables", "discovered_tables_findings.json")
        os.makedirs(os.path.dirname(findings_filename), exist_ok=True)
        with open(findings_filename, "w", encoding='utf-8') as f:
            json.dump(all_findings, f, indent=2, cls=EnhancedJSONEncoder)
        logging.info(f"All {len(all_findings)} findings saved to {findings_filename}")
    else:
        logging.info("No findings were discovered.")
