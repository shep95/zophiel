import difflib
import datetime

class EntityResolver:
    """
    THE BRAIN: Entity Resolution Engine
    Connects aliases to real identities using fuzzy matching, temporal analysis, and behavioral signatures.
    """
    
    def __init__(self):
        self.identity_graph = {
            "immutable": [],    # Email hashes, phone numbers
            "semi_mutable": [], # Username patterns, writing stylometry
            "mutable": []       # Names, addresses, employment
        }

    def detect_corporate_footprint(self, content):
        """Scans content for business entity markers (LLC, Inc, CEO, etc)."""
        content = content.lower()
        markers = ["llc", "inc.", "incorporated", "limited liability company", "corp.", "corporation", 
                   "founder", "co-founder", "ceo", "chief executive officer", "director", "board member", 
                   "owner", "partner", "president", "registered agent", "managing member"]
        found = list(set([m for m in markers if m in content])) # Unique matches
        return bool(found), found

    def calculate_confidence(self, target_name, profile_content, location=None):
        """
        Calculates a confidence score (0-100) that a profile belongs to the target.
        Returns: score (int), confidence (str), metadata (dict)
        """
        if not target_name or not profile_content:
            return 0, "LOW", {}

        target_name = target_name.lower()
        profile_content = profile_content.lower()
        location_score = 0
        location_match = False
        metadata = {"corporate": [], "location_matched": False}
        
        # 0. Corporate Footprint Detection
        is_corporate, corp_markers = self.detect_corporate_footprint(profile_content)
        corp_boost = 0
        if is_corporate:
            corp_boost = 20
            metadata["corporate"] = corp_markers
        
        # 0. Location Verification (If provided)
        if location:
            location = location.lower()
            
            # Location Aliases (Normalize)
            loc_aliases = [location]
            
            # US Context Detection
            us_indicators = ["america", "usa", "us", "united states", "florida", "california", "texas", "new york", "ohio", "michigan"]
            is_us_context = any(ind in location for ind in us_indicators)
            
            if is_us_context:
                loc_aliases.extend(["united states", "usa", "america", "north america", "fl", "fla", "florida"])
            
            # Negative Indicators (Anti-Match)
            negative_indicators = []
            if is_us_context:
                negative_indicators = ["united kingdom", "london", "uk", "germany", "france", "australia", "canada", "europe"]
            
            # Check Negative
            for neg in negative_indicators:
                if neg in profile_content:
                    return 0, "LOW (Location Mismatch)", metadata

            # Check Positive
            for alias in loc_aliases:
                if alias in profile_content:
                    location_score = 30
                    location_match = True
                    metadata["location_matched"] = True
                    break
            
            if not location_match:
                 # Split location into parts
                 loc_parts = [p.strip() for p in location.replace(',', ' ').split() if len(p) > 2]
                 for part in loc_parts:
                     if part in profile_content:
                         location_score += 15
                         location_match = True
                         metadata["location_matched"] = True
                         break
        
        # 1. Exact Name Match (Highest Confidence)
        if target_name in profile_content:
            final_score = 95
            if location and location_match:
                return 99, "HIGH (Verified + Location Match)", metadata
            elif location and not location_match:
                return 90, "HIGH (Verified Name)", metadata
            return 95, "HIGH (Verified)", metadata

        # 2. Fuzzy Matching
        name_parts = target_name.split()
        matches_found = 0
        
        for part in name_parts:
            if part in profile_content:
                matches_found += 1
        
        # Calculate Ratio
        ratio = matches_found / len(name_parts)
        
        # Base Score from Name Match
        base_score = 0
        status = "LOW"
        
        if ratio >= 1.0:
            base_score = 95
            status = "HIGH (Verified)"
        elif ratio >= 0.5: 
            if len(name_parts) > 1 and matches_found == 1:
                 base_score = 40
                 status = "LOW (Partial Match)"
            else:
                base_score = 75
                status = "MEDIUM (Probable)"
        else:
            base_score = 10
            status = "LOW (Name Not Found)"

        # Apply Location Boost and Corporate Boost
        final_score = base_score + location_score + corp_boost
        
        # Cap at 100
        if final_score > 100: final_score = 100
        
        # Refine Status based on new Final Score
        if final_score >= 90:
            status = f"HIGH (Verified)"
            if location_match: status += " + LOC"
        elif final_score >= 70:
            status = f"MEDIUM (Probable)"
            if location_match: status += " + LOC"
        elif final_score >= 50:
            status = f"MEDIUM (Possible)"
            
        if is_corporate:
            status += f" [CORP: {', '.join(corp_markers[:2])}]"
        
        return final_score, status, metadata

    def build_identity_graph(self, data):
        """
        Constructs a probabilistic graph linking collected data points.
        Returns a structured dictionary representing the graph.
        """
        graph = {
            "nodes": [],
            "edges": []
        }
        
        # Add Target Node
        target_node_id = "TARGET_001"
        graph["nodes"].append({"id": target_node_id, "label": "TARGET", "type": "person"})
        
        # Process Matches
        for match in data.get('matches', []):
            node_id = f"{match['platform']}_{match['username']}"
            graph["nodes"].append({"id": node_id, "label": match['username'], "type": "account"})
            
            # Edge Weight based on Confidence
            weight = 0.5
            if "HIGH" in match.get('confidence', ''):
                weight = 0.9
            elif "MEDIUM" in match.get('confidence', ''):
                weight = 0.6
                
            graph["edges"].append({
                "from": target_node_id, 
                "to": node_id, 
                "label": "owns", 
                "weight": weight
            })
            
        return graph
