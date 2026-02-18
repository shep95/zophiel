from graph_db import GraphDB
from data_models import Finding, Relationship, CorrelationType, FindingType, AttackChain, AttackObjective, Difficulty, DetectionRisk
from itertools import combinations
import networkx as nx

class CorrelationEngine:
    def __init__(self, graph_db: GraphDB):
        self.graph_db = graph_db

    def correlate_findings(self):
        self.correlate_credential_reuse()

    def correlate_credential_reuse(self):
        # Get all findings that are API keys
        api_keys = self.graph_db.get_findings_by_type(FindingType.API_KEY)
        
        # Group API keys by value
        keys_by_value = {}
        for key_finding in api_keys:
            if key_finding['value'] not in keys_by_value:
                keys_by_value[key_finding['value']] = []
            keys_by_value[key_finding['value']].append(key_finding)
            
        # If a key is found in more than one place, it's reused
        for key_value, findings in keys_by_value.items():
            if len(findings) > 1:
                # Create relationships between all pairs of findings for the same key
                for f1_data, f2_data in combinations(findings, 2):
                    f1 = Finding(**f1_data)
                    f2 = Finding(**f2_data)
                    relationship = Relationship(
                        type=CorrelationType.CREDENTIAL_REUSE,
                        findings=[f1, f2],
                        description=f"API key {key_value} reused in {f1.source_module} and {f2.source_module}",
                        confidence=0.9,
                        impact="High"
                    )
                    self.graph_db.add_relationship(relationship)
                    print(f"Found credential reuse: {relationship.description}")

class AttackChainGenerator:
    def __init__(self, graph_db: GraphDB):
        self.graph_db = graph_db

    def generate_attack_chains(self, entry_point_type, target_type):
        attack_chains = []
        entry_points = self.graph_db.get_findings_by_type(entry_point_type)
        targets = self.graph_db.get_findings_by_type(target_type)

        for entry_point_data in entry_points:
            for target_data in targets:
                entry_point = Finding(**entry_point_data)
                target = Finding(**target_data)
                
                # Find all paths between the entry point and the target
                paths = nx.all_simple_paths(self.graph_db.graph, source=entry_point.id, target=target.id)

                for path_ids in paths:
                    path_findings = [Finding(**self.graph_db.graph.nodes[node_id]) for node_id in path_ids]
                    attack_chain = AttackChain(
                        steps=path_findings,
                        entry_point=entry_point,
                        objective=AttackObjective.DATA_ACCESS,  # This would be more dynamic
                        difficulty=Difficulty.MEDIUM, # This would be calculated based on the steps
                        detection_risk=DetectionRisk.MEDIUM # This would be calculated based on the steps
                    )
                    attack_chains.append(attack_chain)
                    print(f"Generated attack chain with {len(path_findings)} steps.")
        return attack_chains
