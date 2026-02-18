import networkx as nx
from data_models import Finding, Relationship

class GraphDB:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_finding(self, finding: Finding):
        # Add the finding as a node
        self.graph.add_node(finding.id, **finding.__dict__)

    def add_relationship(self, relationship: Relationship):
        # Add an edge between the two findings
        if len(relationship.findings) == 2:
            finding1 = relationship.findings[0]
            finding2 = relationship.findings[1]
            self.graph.add_edge(finding1.id, finding2.id, **relationship.__dict__)

    def get_findings_by_type(self, finding_type):
        return [data for node, data in self.graph.nodes(data=True) if data.get('type') == finding_type]

    def export_to_neo4j_cypher(self, cypher_filename="import.cypher"):
        with open(cypher_filename, "w") as f:
            # Create nodes
            for node, data in self.graph.nodes(data=True):
                finding = Finding(**data)
                cypher = f'''MERGE (n:Finding {{id: \'{finding.id}'}}) SET n += {{value: \'{finding.value}', type: \'{finding.type.value}', source_module: \'{finding.source_module}', target: \'{finding.target}', confidence: {finding.confidence}, timestamp: \'{finding.timestamp}'}};\n'''
                f.write(cypher)

            # Create edges
            for u, v, data in self.graph.edges(data=True):
                relationship = Relationship(**data)
                cypher = f'''MATCH (a:Finding {{id: \'{u}'}}), (b:Finding {{id: \'{v}'}}) MERGE (a)-[r:{relationship.type.value} {{description: \'{relationship.description}', confidence: {relationship.confidence}, impact: \'{relationship.impact}'}}]->(b);\n'''
                f.write(cypher)

        print(f"Exported Cypher script to {cypher_filename}")
