
def chaldean_numerology(name):
    chaldean_map = {
        'a': 1, 'i': 1, 'j': 1, 'q': 1, 'y': 1,
        'b': 2, 'k': 2, 'r': 2,
        'c': 3, 'g': 3, 'l': 3, 's': 3,
        'd': 4, 'm': 4, 't': 4,
        'e': 5, 'h': 5, 'n': 5, 'x': 5,
        'u': 6, 'v': 6, 'w': 6,
        'o': 7, 'z': 7,
        'f': 8, 'p': 8
    }
    
    total = 0
    breakdown = []
    
    clean_name = name.lower().strip()
    
    parts = clean_name.split()
    part_totals = []
    
    for part in parts:
        part_sum = 0
        part_chars = []
        for char in part:
            if char in chaldean_map:
                val = chaldean_map[char]
                part_sum += val
                part_chars.append(f"{char}({val})")
        
        part_totals.append(part_sum)
        total += part_sum
        breakdown.append(f"{part}: {'+'.join(part_chars)} = {part_sum}")

    return total, breakdown, part_totals

names_to_test = [
    "Asher Shepherd Newton",
    "Asher Newton",
    "Asher S. Newton",
    "A. S. Newton",
    "Asher S. Newton"
]

for n in names_to_test:
    t, b, pt = chaldean_numerology(n)
    print(f"Name: {n}")
    print(f"Breakdown: {b}")
    print(f"Total: {t} -> {sum(int(d) for d in str(t))}")
    print("-" * 20)
