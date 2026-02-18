import re
from graph_db import GraphDB
from data_models import Finding, FindingType

class MutationEngine:
    def __init__(self, graph_db: GraphDB):
        self.graph_db = graph_db
        self.patterns = {}

    def learn_from_successful_findings(self, confidence_threshold=0.7):
        """Learns patterns from high-confidence findings in the graph."""
        for node, data in self.graph_db.graph.nodes(data=True):
            finding = Finding(**data)
            if finding.confidence >= confidence_threshold:
                if finding.type == FindingType.ENDPOINT:
                    pattern = self._extract_endpoint_pattern(finding.value)
                    if pattern not in self.patterns:
                        self.patterns[pattern] = {"success_count": 0, "total_attempts": 0}
                    self.patterns[pattern]["success_count"] += 1

    def record_mutation_attempt(self, pattern: str, mutation: str):
        """Records that a mutation has been attempted."""
        if pattern in self.patterns:
            self.patterns[pattern]["total_attempts"] += 1

    def record_mutation_success(self, pattern: str, mutation: str):
        """Records that a mutation was successful."""
        if pattern in self.patterns:
            self.patterns[pattern]["success_count"] += 1

    def _extract_endpoint_pattern(self, endpoint: str) -> str:
        """Extracts a generic pattern from a specific endpoint URL path."""
        # Replace numbers with a placeholder
        pattern = re.sub(r'\d+', '{id}', endpoint)
        # Add more pattern extraction rules here in the future
        # For example, replacing UUIDs, specific resource names, etc.
        # A more generic pattern could be to split by '/' and identify parts
        parts = [p for p in endpoint.split('/') if p]
        if len(parts) > 2 and parts[0] == 'api': # e.g. /api/v1/users
            pattern = f"/{parts[0]}/{{version}}/{{resource}}"

        return pattern

    def get_prioritized_mutations(self, count=100) -> list[str]:
        """Gets a list of mutations to try, prioritized by success rate."""
        # Sort patterns by success rate (success_count / total_attempts)
        sorted_patterns = sorted(
            self.patterns.items(), 
            key=lambda item: (item[1]["success_count"] / item[1]["total_attempts"]) if item[1]["total_attempts"] > 0 else 0,
            reverse=True
        )

        all_mutations = []
        for pattern, _ in sorted_patterns:
            all_mutations.extend(self.generate_mutations(pattern, count=20)) # Generate a few for each pattern

        return list(set(all_mutations))[:count]

    def generate_mutations(self, pattern: str, count=50) -> list[str]:
        """Generates mutations based on a learned pattern."""
        mutations = []
        common_ids = ["1", "0", "-1", "100", "admin", "test"]
        common_versions = ["v1", "v2", "v3", "v4"]
        common_resources = [
            "users", "profiles", "accounts", "customers", "members",
            "posts", "comments", "messages", "notifications",
            "orders", "products", "inventory", "payments", "transactions",
            "settings", "config", "roles", "permissions", "logs"
        ]

        # ID replacement
        if "{id}" in pattern:
            for i in range(count):
                new_id = common_ids[i % len(common_ids)]
                mutations.append(pattern.replace("{id}", new_id))

        # Version and resource replacement
        if "{version}" in pattern and "{resource}" in pattern:
            for i in range(count):
                version = common_versions[i % len(common_versions)]
                resource = common_resources[i % len(common_resources)]
                mutation = pattern.replace("{version}", version).replace("{resource}", resource)
                mutations.append(mutation)
                # Try different methods (conceptual)
                # In a real scenario, you'd return the method along with the URL
                mutations.append(f"POST:{mutation}")
                mutations.append(f"PUT:{mutation}")
                mutations.append(f"DELETE:{mutation}")

        return list(set(mutations)) # Deduplicate

    def get_patterns(self):
        return self.patterns
