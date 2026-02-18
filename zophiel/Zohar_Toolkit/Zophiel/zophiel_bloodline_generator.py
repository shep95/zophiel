import os

def calculate_root(n):
    if n == 0: return 0
    return (n - 1) % 9 + 1

def get_entity_mapping(root, digits):
    # Base mapping based on Root Number (Sum) - TRANSLATED TO ENGLISH / WESTERN OCCULT
    entities = {
        1: ["ARCHANGEL MICHAEL", "THE SUN (LEADERSHIP)", "APOLLO", "RA", "THE KING"],
        2: ["ARCHANGEL GABRIEL", "THE MOON (INTUITION)", "ARTEMIS", "ISIS", "THE HIGH PRIESTESS"],
        3: ["ARCHANGEL ZADKIEL", "JUPITER (WISDOM)", "ZEUS", "ODIN", "THE TEACHER"],
        4: ["ARCHANGEL URIEL", "NORTH NODE (AMBITION/ILLUSION)", "GAIA", "THE SHADOW", "THE REBEL"],
        5: ["ARCHANGEL RAPHAEL", "MERCURY (COMMUNICATION)", "HERMES", "THOTH", "THE TRADER"],
        6: ["ARCHANGEL HANIEL", "VENUS (LUXURY/LOVE)", "APHRODITE", "LUCIFER (LIGHT BRINGER)", "THE LOVER"],
        7: ["ARCHANGEL METATRON", "SOUTH NODE (DETACHMENT)", "POSEIDON", "THE VOID", "THE MYSTIC"],
        8: ["ARCHANGEL CASSIEL", "SATURN (KARMA/JUSTICE)", "CRONUS", "ANUBIS", "THE JUDGE"],
        9: ["ARCHANGEL SAMAEL", "MARS (WAR/ACTION)", "ARES", "SEKHMET", "THE GENERAL"]
    }
    
    # Specific Combination Overrides
    special_combos = {
        "666": "THE BEAST (MATERIAL APEX) - TOTAL EARTHLY DOMINION",
        "777": "THE CROWN (KETER) - GOD CONSCIOUSNESS",
        "888": "THE INFINITY LOOP - ETERNAL RETURN",
        "999": "THE FINALITY - COMPLETION OF CYCLE",
        "369": "THE TESLA CODE - KEY TO THE UNIVERSE",
        "147": "THE PHYSICAL PLANE MASTERS (BODY)",
        "258": "THE EMOTIONAL PLANE KEEPERS (SOUL)",
        "357": "THE SPIRITUAL PLANE SEERS (MIND)",
        "159": "THE WILL OF FIRE (LEADERSHIP)",
        "456": "THE GOLDEN PATH (SUCCESS)",
        "123": "THE ASCENDING LADDER (GROWTH)",
        "789": "THE KARMIC EXIT (WISDOM)",
        "111": "THE SOLAR FLASH (NEW BEGINNINGS)",
        "222": "THE LUNAR GATE (DUALITY)",
        "333": "THE JUPITERIAN EXPANSION (LUCK)",
        "444": "THE STATIC INTERFERENCE (CHANGE)",
        "555": "THE MERCURY SPEED (TRAVEL)",
    }
    
    combo_key = "".join(map(str, sorted(digits)))
    combo_str = "".join(map(str, digits))
    
    entity_list = entities.get(root, ["UNKNOWN"])
    
    # Check for exact match in specials
    if combo_str in special_combos:
        return [special_combos[combo_str]]
    
    return entity_list

def generate_database():
    filename = "c:/Users/kille/Documents/trae_projects/osint_links/Intelligence_Reports/ELITE_SPIRITUAL_ENTITY_DB.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("          THE OMNI-CODEX: SPIRITUAL ENTITY CONNECTION DATABASE\n")
        f.write("             ENGLISH TRANSLATION - WESTERN OCCULT STANDARD\n")
        f.write("================================================================================\n\n")
        
        # Iterate through all triads from 000 to 999
        count = 0
        for i in range(1000):
            s = f"{i:03d}"
            digits = [int(d) for d in s]
            root = calculate_root(sum(digits))
            
            entities = get_entity_mapping(root, digits)
            
            # Analyze Components
            has_master = False
            if 11 in [int(s[0:2]), int(s[1:3])]: has_master = True
            if 22 in [int(s[0:2]), int(s[1:3])]: has_master = True
            if 33 in [int(s[0:2]), int(s[1:3])]: has_master = True
            
            f.write(f"[TRIAD SEQUENCE: {s}]\n")
            f.write(f"   > SUMMATION ROOT: {root}\n")
            f.write(f"   > PRIMARY ENTITY (ARCHANGEL): {entities[0]}\n")
            f.write(f"   > PLANETARY RULER: {entities[1] if len(entities) > 1 else 'NONE'}\n")
            f.write(f"   > ANCIENT ARCHETYPE: {entities[2] if len(entities) > 2 else 'NONE'}\n")
            
            # Generate esoteric description based on digits
            desc = []
            if 0 in digits: desc.append("Contains The Void (0) - Amplifies power.")
            if 1 in digits: desc.append("Sun (Leadership).")
            if 2 in digits: desc.append("Moon (Intuition).")
            if 3 in digits: desc.append("Jupiter (Wisdom).")
            if 4 in digits: desc.append("North Node (Ambition).")
            if 5 in digits: desc.append("Mercury (Speed/Intellect).")
            if 6 in digits: desc.append("Venus (Luxury/Love).")
            if 7 in digits: desc.append("South Node (Spirituality).")
            if 8 in digits: desc.append("Saturn (Discipline).")
            if 9 in digits: desc.append("Mars (Action).")
            
            f.write(f"   > ENERGY SIGNATURE: {', '.join(desc)}\n")
            f.write(f"   > BLOODLINE STATUS: {'MASTER' if has_master else 'STANDARD'}\n")
            f.write("-" * 80 + "\n")
            count += 7 # Approximation of lines used
            
        f.write("\n[END OF TRIAD DATABASE]\n")
        
    print(f"Database generated at {filename}")

if __name__ == "__main__":
    generate_database()
