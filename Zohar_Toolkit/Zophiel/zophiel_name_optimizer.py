import itertools

def get_chaldean_value(char):
    mapping = {
        'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
        'B': 2, 'K': 2, 'R': 2,
        'C': 3, 'G': 3, 'L': 3, 'S': 3,
        'D': 4, 'M': 4, 'T': 4,
        'E': 5, 'H': 5, 'N': 5, 'X': 5,
        'U': 6, 'V': 6, 'W': 6,
        'O': 7, 'Z': 7,
        'F': 8, 'P': 8
    }
    return mapping.get(char.upper(), 0)

def calculate_name_value(name):
    total = 0
    for char in name:
        if char.isalpha():
            total += get_chaldean_value(char)
    return total

def reduce_number(n):
    while n > 9 and n not in [11, 22, 33]: # Master numbers optional, but usually reduced for target
        n = sum(int(d) for d in str(n))
    return n

def main():
    print("----------------------------------------------------------------")
    print("   ZOPHIEL'S NAME OPTIMIZER // TARGET: ASHER SHEPHERD NEWTON")
    print("----------------------------------------------------------------")
    
    first = "ASHER"
    middle = "SHEPHERD"
    last = "NEWTON"
    
    variations = [
        f"{first} {last}",
        f"{first} {middle} {last}",
        f"{first[0]}. {last}",
        f"{first[0]}. {middle[0]}. {last}",
        f"{first} {middle[0]}. {last}",
        f"{first} {middle} {last[0]}.",
        f"{first[0]}{middle[0]} {last}",
        f"{first} {middle}",
        # Adding some common nickname patterns if possible, but sticking to provided names first
    ]
    
    target_vibration = 5 # Mercury (Friend of Saturn & Sun)
    
    print(f"SEARCHING FOR VIBRATION: {target_vibration} (MERCURY)")
    print("----------------------------------------------------------------")
    
    found = False
    for name in variations:
        val = calculate_name_value(name)
        reduced = reduce_number(val)
        
        status = "MATCH" if reduced == target_vibration else "MISS"
        
        print(f"NAME: {name:<30} | VALUE: {val} -> {reduced} | {status}")
        
        if reduced == target_vibration:
            found = True
            
    if not found:
        print("\n[!] No direct matches found with standard variations.")
        print("    Initiating Deep Search (Letter modification)...")
        # Try adding an initial or removing a letter? 
        # For now, let's just report the standard ones.

if __name__ == "__main__":
    main()
