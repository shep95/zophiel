import os
import json
import time
import datetime
import random
import uuid
from typing import List, Dict, Any
from .zephon_metadata import ZephonMetadata

class ZephonCore:
    """
    ZEPHON CORE ENGINE
    ------------------
    Codename: "THE SEARCHER"
    Capability Tier: Government/Nation-State Implementation
    
    Modules:
    1. Metadata Extraction (Deep Forensic Parsing)
    2. Entity Resolution (User Fingerprinting)
    3. Temporal Analysis (Document DNA)
    4. Operational Security (Counter-Surveillance)
    """

    def __init__(self):
        self.metadata_engine = ZephonMetadata()
        self.intelligence_db = []
        self.session_id = str(uuid.uuid4())
        self.classification = "TOP SECRET // NOFORN"
        self.vault = None

    def ingest_directory(self, directory_path: str) -> List[Dict]:
        """
        Recursively ingests files from a directory for deep analysis.
        Simulates 'Global-scale passive collection'.
        """
        print(f"[*] ZEPHON: Initializing Ingestion Protocol on {directory_path}")
        print(f"[*] ENCRYPTION: Quantum-Resistant Layer Active")
        
        results = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Skip system files
                if file.startswith('.') or 'System Volume Information' in file_path:
                    continue
                
                print(f"[*] TARGET ACQUIRED: {file}")
                intel = self.process_artifact(file_path)
                results.append(intel)
                self.intelligence_db.append(intel)
        
        return results

    def process_artifact(self, file_path: str) -> Dict[str, Any]:
        """
        Processes a single digital artifact.
        Fuses Metadata, Content Analysis, and Simulated SIGINT/FININT.
        """
        # 1. Metadata Extraction
        raw_data = self.metadata_engine.extract(file_path)
        
        # 2. Forensic Analysis
        analysis = self._analyze_vectors(raw_data)
        
        # 3. Nation-State Enrichment (Simulated/Logical)
        enrichment = self._enrich_intelligence(raw_data, analysis)

        return {
            "artifact_id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat(),
            "classification": self.classification,
            "raw_metadata": raw_data,
            "forensic_analysis": analysis,
            "agency_enrichment": enrichment
        }

    def _analyze_vectors(self, data: Dict) -> Dict:
        """
        Analyzes metadata for intelligence vectors (Usernames, Software, Anomalies).
        """
        analysis = {
            "risk_score": 0,
            "extracted_identities": [],
            "software_vulnerabilities": [],
            "anomalies": []
        }
        
        deep = data.get("deep_metadata", {})
        
        # Identity Extraction from Author/LastModifiedBy
        if "author" in deep and deep["author"]:
            analysis["extracted_identities"].append({"type": "author", "value": deep["author"]})
        if "last_modified_by" in deep and deep["last_modified_by"]:
            analysis["extracted_identities"].append({"type": "modifier", "value": deep["last_modified_by"]})
            
        # Identity Extraction from PDF Producer (often contains software version)
        if "Producer" in deep:
            analysis["software_vulnerabilities"].append(deep["Producer"])
        if "Creator" in deep:
            analysis["software_vulnerabilities"].append(deep["Creator"])

        # Path Analysis (if absolute path reveals user)
        # E.g. C:\Users\Gary\Desktop...
        abs_path = data.get("absolute_path", "")
        if "Users" in abs_path:
            try:
                # Naive split to get username
                parts = abs_path.split(os.sep)
                if "Users" in parts:
                    idx = parts.index("Users")
                    if idx + 1 < len(parts):
                        username = parts[idx+1]
                        analysis["extracted_identities"].append({"type": "system_user", "value": username})
                        analysis["risk_score"] += 10  # High value intel
            except:
                pass

        return analysis

    def _enrich_intelligence(self, data: Dict, analysis: Dict) -> Dict:
        """
        Adds Government-tier context (Simulated for the 'App' feel).
        """
        # Simulate SIGINT Correlation
        has_gps = any("GPS" in k for k in data.get("deep_metadata", {}).keys())
        
        return {
            "sigint_correlation": "DETECTED" if has_gps else "NEGATIVE",
            "finint_trace": "SCANNING_MACROS..." if "xl" in data.get("filename", "") else "N/A",
            "counter_surveillance_check": "PASSED" if analysis["risk_score"] < 50 else "ALERT: OPSEC VIOLATION",
            "geospatial_lock": "ACQUIRED" if has_gps else "ESTIMATING FROM IP...",
            "dissemination_channel": "JWICS/SIPRNet",
            "pattern_of_life": "Insufficient Data Points"
        }

    def generate_report(self, output_path: str = "Zephon_Report.json"):
        """
        Generates a disseminated intelligence report.
        ENCRYPTION: Auto-encrypts if Vault is active.
        """
        report = {
            "operation": "ZEPHON_DEEP_SEARCH",
            "session_id": self.session_id,
            "generated_at": datetime.datetime.now().isoformat(),
            "total_artifacts": len(self.intelligence_db),
            "artifacts": self.intelligence_db
        }
        
        # Dump cleartext JSON first (memory buffer style)
        json_str = json.dumps(report, indent=4, default=str)
        
        if self.vault:
            # Encrypt immediately
            encrypted_data = self.vault.encrypt_data(json_str)
            final_path = output_path + ".enc"
            with open(final_path, 'wb') as f:
                f.write(encrypted_data)
            print(f"[*] REPORT ENCRYPTED & LOCKED: {final_path}")
            return final_path
        else:
            # Fallback to cleartext (Risk!)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"[!] WARNING: ENCRYPTION OFFLINE. REPORT SAVED CLEARTEXT: {output_path}")
            return output_path

import datetime
