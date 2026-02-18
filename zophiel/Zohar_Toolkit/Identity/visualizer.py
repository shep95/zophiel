
import os
import json

class NetworkGraphGenerator:
    def __init__(self, output_dir="Intelligence_Reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_graph(self, target_name, data):
        """
        Generates an interactive HTML network graph using Vis.js.
        """
        filename = f"{target_name.replace(' ', '_')}_NetworkMap.html"
        filepath = os.path.join(self.output_dir, filename)
        
        # Prepare Nodes and Edges
        nodes = []
        edges = []
        
        # 1. Central Target Node
        nodes.append({
            "id": 1, 
            "label": target_name.upper(), 
            "color": "#ff0000", 
            "shape": "box", 
            "font": {"color": "white", "size": 20}
        })
        
        node_id_counter = 2
        
        # 2. Selector Nodes (Usernames)
        for selector in data.get('selectors', [])[:5]: # Limit to top 5 to keep graph clean
            nodes.append({
                "id": node_id_counter,
                "label": selector,
                "color": "#00ff41",
                "shape": "ellipse"
            })
            edges.append({"from": 1, "to": node_id_counter, "label": "SELECTOR"})
            node_id_counter += 1
            
        # 3. Email Nodes
        for email in data.get('emails', [])[:3]:
            nodes.append({
                "id": node_id_counter,
                "label": email,
                "color": "#00ccff",
                "shape": "ellipse"
            })
            edges.append({"from": 1, "to": node_id_counter, "label": "EMAIL"})
            node_id_counter += 1
            
        # 4. Match Nodes (Confirmed Accounts)
        for match in data.get('matches', []):
            nodes.append({
                "id": node_id_counter,
                "label": match['platform'],
                "color": "#ffff00",
                "shape": "database"
            })
            edges.append({"from": 1, "to": node_id_counter, "label": "ACCOUNT"})
            
            # Link username to account if possible (simplified here)
            node_id_counter += 1

        # Serialize to JSON for JS injection
        nodes_json = json.dumps(nodes)
        edges_json = json.dumps(edges)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ZOHAR NETWORK MAP: {target_name.upper()}</title>
            <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
            <style type="text/css">
                body {{ background-color: #0a0a0a; color: #00ff41; margin: 0; }}
                #mynetwork {{ width: 100vw; height: 100vh; border: 1px solid #333; }}
                .overlay {{ position: absolute; top: 20px; left: 20px; background: rgba(0,0,0,0.8); padding: 15px; border: 1px solid #00ff41; pointer-events: none; }}
            </style>
        </head>
        <body>
            <div id="mynetwork"></div>
            <div class="overlay">
                <h2>TARGET LINK ANALYSIS</h2>
                <p>TARGET: {target_name.upper()}</p>
                <p>NODES: {len(nodes)}</p>
                <p>RELATIONSHIPS: {len(edges)}</p>
            </div>
            <script type="text/javascript">
                var nodes = new vis.DataSet({nodes_json});
                var edges = new vis.DataSet({edges_json});

                var container = document.getElementById('mynetwork');
                var data = {{ nodes: nodes, edges: edges }};
                var options = {{
                    nodes: {{
                        borderWidth: 2,
                        shadow: true
                    }},
                    edges: {{
                        width: 2,
                        shadow: true,
                        color: {{ color: '#333', highlight: '#00ff41' }}
                    }},
                    physics: {{
                        stabilization: false,
                        barnesHut: {{
                            gravitationalConstant: -8000,
                            springConstant: 0.04,
                            springLength: 95
                        }}
                    }}
                }};
                var network = new vis.Network(container, data, options);
            </script>
        </body>
        </html>
        """
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"\n[+] NETWORK GRAPH GENERATED: {filepath}")
        return filepath
