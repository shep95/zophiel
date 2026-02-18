import json
import os
from data_models import Finding, FindingType
from graph_db import GraphDB
from enum import Enum

class EnhancedJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if 'id' in obj and 'type' in obj and 'value' in obj:
            # A bit of a hack, but should work for now
            try:
                obj['type'] = FindingType(obj['type'])
                return Finding(**obj)
            except (TypeError, ValueError):
                pass
        return obj

class Pipeline:
    def __init__(self, graph_db: GraphDB):
        self.graph_db = graph_db
        self.processed_finding_ids = set()

    def load_findings_from_file(self, filepath):
        with open(filepath, 'r') as f:
            try:
                findings = json.load(f, cls=EnhancedJSONDecoder)
                if isinstance(findings, list):
                    return findings
                return [findings]
            except json.JSONDecodeError:
                return []

    def process_findings(self, findings_dir="output"):
        for root, _, files in os.walk(findings_dir):
            for file in files:
                if file.endswith(".json"):
                    filepath = os.path.join(root, file)
                    findings = self.load_findings_from_file(filepath)
                    for finding in findings:
                        if finding.id not in self.processed_finding_ids:
                            self.graph_db.add_finding(finding)
                            self.processed_finding_ids.add(finding.id)
