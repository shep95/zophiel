import json
import os

class Archon:
    """
    ARCHON: The Identity Mapper.
    Module for cross-referencing user identities across different ecosystem apps
    and reconstructing social graphs to identify High Value Targets (HVTs).
    """
    def __init__(self):
        self.known_matches = []
        self.social_graph = {}
        self.hvt_list = []

    def analyze_social_graph(self, follows_file):
        """
        Reconstructs the social graph from follows data to identify influencers.
        """
        print(f"\n[ARCHON] Reconstructing Social Graph from {follows_file}...")
        
        if not os.path.exists(follows_file):
            print(f"  [!] Follows file not found: {follows_file}")
            return {}

        with open(follows_file, 'r') as f:
            follows_data = json.load(f)

        # Build Graph
        # structure: { user_id: { 'followers': [], 'following': [] } }
        graph = {}
        
        for rel in follows_data:
            follower = rel.get('follower_id')
            following = rel.get('following_id')
            
            # Initialize nodes if they don't exist
            if follower not in graph: graph[follower] = {'followers': [], 'following': []}
            if following not in graph: graph[following] = {'followers': [], 'following': []}
            
            # Add edges
            if follower and following:
                graph[follower]['following'].append(following)
                graph[following]['followers'].append(follower)
        
        self.social_graph = graph
        print(f"  [+] Graph reconstructed: {len(graph)} nodes.")
        
        # Identify HVTs (High Value Targets) based on follower count
        sorted_users = sorted(graph.items(), key=lambda x: len(x[1]['followers']), reverse=True)
        
        print("  [+] Top Influencers (Potential Admins/Mods):")
        for user_id, data in sorted_users[:5]:
            count = len(data['followers'])
            print(f"    - {user_id}: {count} followers")
            self.hvt_list.append({'id': user_id, 'followers': count, 'role': 'influencer'})
            
        return graph

    def map_identities(self, bosley_users_file, follows_file, external_uuids):
        """
        Correlates a list of external UUIDs (e.g. from Avven) against Bosley data.
        """
        print(f"\n[ARCHON] Mapping identities across the ecosystem...")
        
        # 1. Analyze Social Graph first to populate HVT list
        self.analyze_social_graph(follows_file)
        
        matches = []
        
        # 2. Load Bosley User Database (if available) or use Graph Nodes
        bosley_users = []
        if os.path.exists(bosley_users_file):
            with open(bosley_users_file, 'r') as f:
                bosley_users = json.load(f)
            print(f"  [+] Loaded {len(bosley_users)} known Bosley entities from file.")
        else:
            # Fallback to graph nodes
            bosley_users = list(self.social_graph.keys())
            print(f"  [+] Using {len(bosley_users)} graph nodes as entity list.")

        # 3. Cross-Reference External UUIDs
        print(f"  [+] Cross-referencing {len(external_uuids)} external targets...")
        for target in external_uuids:
            # Check existence
            if target in bosley_users:
                print(f"    [MATCH] EXTERNAL TARGET {target} FOUND IN BOSLEY!")
                role = "user"
                # Check if HVT
                for hvt in self.hvt_list:
                    if hvt['id'] == target:
                        role = "HVT/Influencer"
                
                matches.append({
                    "uid": target,
                    "status": "CONFIRMED",
                    "role": role,
                    "platform_cross_ref": "Avven/Zorak -> Bosley"
                })
        
        self.known_matches = matches
        if not matches:
            print("  [-] No direct cross-app identity matches found.")
        
        return matches
