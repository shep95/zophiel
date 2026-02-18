import datetime

def get_reduced_sum(n):
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_personal_year(birth_day, birth_month, year):
    bd = get_reduced_sum(birth_day)
    bm = get_reduced_sum(birth_month)
    cy = get_reduced_sum(year)
    return get_reduced_sum(bd + bm + cy)

def get_tri_material_score(s_py, l_py, age):
    """
    Returns scores (0-100) for POWER, ASSETS, LIQUIDITY based on Solar/Lunar PY and Age.
    """
    power_score = 0
    asset_score = 0
    liquid_score = 0
    
    # ---------------------------------------------------------
    # 1. PLANETARY INFLUENCE (PY)
    # ---------------------------------------------------------
    
    # SOLAR PY (Weighted Higher for Power/Structure)
    if s_py == 8: power_score += 50; asset_score += 30; liquid_score += 10
    elif s_py == 1: power_score += 60; asset_score += 20; liquid_score += 10
    elif s_py == 9: power_score += 40; liquid_score += 20 # War energy
    elif s_py == 6: asset_score += 60; liquid_score += 30; power_score += 20
    elif s_py == 5: liquid_score += 60; asset_score += 20; power_score += 10
    elif s_py == 4: liquid_score += 70; power_score += 20 # Chaos Wealth
    elif s_py == 3: asset_score += 40; power_score += 30
    elif s_py == 2: liquid_score += 10; power_score -= 10 # Weak for Saturn
    
    # LUNAR PY (Weighted Higher for Liquidity/Speed)
    if l_py == 5: liquid_score += 40; asset_score += 10
    elif l_py == 6: asset_score += 40; liquid_score += 10
    elif l_py == 1: power_score += 30; liquid_score += 10
    elif l_py == 4: liquid_score += 50
    elif l_py == 3: asset_score += 20
    
    # ---------------------------------------------------------
    # 2. MATURATION BONUSES (PAKKA GHAR) - THE GUARANTEES
    # ---------------------------------------------------------
    if age == 24: liquid_score += 50 # Moon (Intuition -> Cash)
    if age == 25: asset_score += 100 # Venus (Luxury -> Assets) ** HUGE SPIKE **
    if age == 32: liquid_score += 100 # Mercury (Empire -> Cash Flow) ** HUGE SPIKE **
    if age == 36: power_score += 100 # Saturn (King -> Authority) ** HUGE SPIKE **
    if age == 42: liquid_score += 80; power_score += 50 # Rahu (Explosion)
    if age == 48: power_score -= 20; asset_score -= 20 # Ketu (Detachment)
    
    # Cap at 100 (visual clarity)
    power_score = min(power_score, 100)
    asset_score = min(asset_score, 100)
    liquid_score = min(liquid_score, 100)
    
    return power_score, asset_score, liquid_score

def get_wealth_activation_ages(root_number):
    """
    Returns the specific 'Pakka Ghar' (Maturation Ages) for a given Root Number.
    """
    activations = {
        1: [22, 24, 28, 35],       # SUN
        2: [24, 38, 47],           # MOON
        3: [16, 21, 32, 48],       # JUPITER
        4: [22, 36, 42],           # RAHU
        5: [25, 32, 50],           # MERCURY
        6: [24, 25, 33, 42],       # VENUS
        7: [21, 28, 35],           # KETU
        8: [36, 42, 44, 51],       # SATURN (Added 44)
        9: [28, 36, 45]            # MARS
    }
    return activations.get(root_number, [])


def analyze_grid_arrows(dob_digits):
    """
    Analyzes the 8 Arrows of Power in the Lo Shu Grid.
    """
    grid_counts = {i: dob_digits.count(i) for i in range(1, 10)}
    
    arrows = {
        "THE GOLDEN TRIO (4-5-6) [WEALTH]": [4, 5, 6],
        "THE SILVER TRIO (2-5-8) [PROPERTY]": [2, 5, 8],
        "THE MENTAL TRIO (4-9-2) [GENIUS]": [4, 9, 2],
        "THE EMOTIONAL TRIO (3-5-7) [INFLUENCE]": [3, 5, 7],
        "THE PRACTICAL TRIO (8-1-6) [BUSINESS]": [8, 1, 6],
        "THE VISION TRIO (4-3-8) [POLITICS]": [4, 3, 8],
        "THE WILL TRIO (9-5-1) [EXECUTION]": [9, 5, 1],
        "THE ACTION TRIO (2-7-6) [ENERGY]": [2, 7, 6]
    }
    
    print("\n[+] UNIVERSAL GRID ANALYSIS (THE 8 ELITE ARROWS):")
    
    detected_any = False
    for name, nums in arrows.items():
        if all(grid_counts[n] > 0 for n in nums):
            print(f"    -> [DETECTED] {name}")
            detected_any = True
            
    if not detected_any:
        print("    -> [NONE] No complete arrows detected.")
        
    return grid_counts

def analyze_poverty_traps(grid_counts, driver, conductor):
    """
    Analyzes negative patterns and 'Anti-Wealth' indicators.
    """
    print("\n[!] WEALTH OBSTACLE SCAN (POVERTY TRAPS):")
    traps_found = False

    # 1. MISSING KEY WEALTH NUMBERS
    if grid_counts.get(5, 0) == 0:
        print("    -> [WARNING] MISSING 5 (THE STABILIZER): Wealth instability. Money flows out fast.")
        traps_found = True
    
    if grid_counts.get(6, 0) == 0:
        print("    -> [WARNING] MISSING 6 (THE LUXURY): Hard work without easy rewards. Lack of support.")
        traps_found = True

    if grid_counts.get(4, 0) == 0:
        print("    -> [WARNING] MISSING 4 (THE DISCIPLINE): Lack of savings/assets. 'Easy come, easy go'.")
        traps_found = True

    # 2. NEGATIVE ARROWS (EMPTY LINES)
    # Frustration (Missing 4-5-6)
    if grid_counts.get(4, 0) == 0 and grid_counts.get(5, 0) == 0 and grid_counts.get(6, 0) == 0:
        print("    -> [CRITICAL] ARROW OF FRUSTRATION (MISSING 4-5-6): Broken ambition. Dreams without a bridge.")
        traps_found = True

    # Skepticism (Missing 3-5-7)
    if grid_counts.get(3, 0) == 0 and grid_counts.get(5, 0) == 0 and grid_counts.get(7, 0) == 0:
        print("    -> [CRITICAL] ARROW OF SKEPTICISM (MISSING 3-5-7): Missed opportunities due to doubt.")
        traps_found = True

    # Confusion (Missing 4-3-8)
    if grid_counts.get(4, 0) == 0 and grid_counts.get(3, 0) == 0 and grid_counts.get(8, 0) == 0:
        print("    -> [CRITICAL] ARROW OF CONFUSION (MISSING 4-3-8): Lack of planning. Drift.")
        traps_found = True

    # Indecision (Missing 9-5-1)
    if grid_counts.get(9, 0) == 0 and grid_counts.get(5, 0) == 0 and grid_counts.get(1, 0) == 0:
        print("    -> [CRITICAL] ARROW OF INDECISION (MISSING 9-5-1): Procrastination. Vision without will.")
        traps_found = True

    # 3. ANTI-WEALTH COMBINATIONS
    # 8 & 4 (Saturn + Rahu)
    if (driver == 8 and conductor == 4) or (driver == 4 and conductor == 8):
        print("    -> [DANGER] 8 & 4 COMBINATION (STRUGGLE): Legal issues/Sudden Reversals. Needs mastery.")
        traps_found = True

    # 2 & 8 (Moon + Saturn)
    if (driver == 2 and conductor == 8) or (driver == 8 and conductor == 2):
        print("    -> [DANGER] 2 & 8 COMBINATION (DEPRESSION): Fear of poverty blocks wealth. Emotional spending.")
        traps_found = True

    # 9 & 2 (Mars + Moon)
    if (driver == 9 and conductor == 2) or (driver == 2 and conductor == 9):
        print("    -> [DANGER] 9 & 2 COMBINATION (CONFLICT): Impulsive actions destroy wealth.")
        traps_found = True

    if not traps_found:
        print("    -> [CLEAN] No major poverty traps detected in the core grid.")

def analyze_spiritual_bloodlines(grid_counts, dob_day, lifepath_number, raw_lifepath_sum):
    """
    Analyzes the 3-digit Triads for Spiritual Bloodline classifications.
    Uses a WEIGHTED SCORING SYSTEM to determine the DOMINANT LINEAGE
    when multiple triads are detected.
    """
    print("\n[!] SPIRITUAL BLOODLINE SCAN (DNA OF THE SOUL):")
    
    # 1. DEFINE THE BLOODLINES
    bloodlines = {
        # DIVINE
        "THE ELOHIM (3-6-9)": {'nums': [3, 6, 9], 'type': 'DIVINE', 'desc': 'Creator/Architect Frequency'},
        "THE MALAKIM (1-4-7)": {'nums': [1, 4, 7], 'type': 'DIVINE', 'desc': 'Archangel/Warrior Bloodline'},
        "THE GRIGORI (2-5-8)": {'nums': [2, 5, 8], 'type': 'DIVINE', 'desc': 'Watcher/Healer Bloodline'},
        "THE OPHANIM (3-5-7)": {'nums': [3, 5, 7], 'type': 'DIVINE', 'desc': 'Prophet/Seer Bloodline'},
        "THE COMMANDER (1-5-9)": {'nums': [1, 5, 9], 'type': 'DIVINE', 'desc': 'King/General Bloodline'},
        
        # DARK/FALLEN
        "THE NEPHILIM (4-5-6)": {'nums': [4, 5, 6], 'type': 'DARK', 'desc': 'Titan/Fallen Bloodline'},
        "THE ABADDON (4-3-8)": {'nums': [4, 3, 8], 'type': 'DARK', 'desc': 'Chaos/Destroyer Bloodline'},
        "THE SORATH (6-6-6)": {'nums': [6], 'type': 'DARK', 'desc': 'The Beast Frequency', 'special': 'triple_6'},
        "THE SHADOW KEEPER (2-4-8)": {'nums': [2, 4, 8], 'type': 'DARK', 'desc': 'Prison Warden Bloodline'},
        "THE ILLUMINATI (1-6-8)": {'nums': [1, 6, 8], 'type': 'DARK', 'desc': 'Hidden Ruler Bloodline'},
        
        # OPERATIONAL/EXOTIC
        "THE ARCHITECT (1-2-3)": {'nums': [1, 2, 3], 'type': 'OPERATIONAL', 'desc': 'Strategist Bloodline'},
        "THE EXECUTIONER (7-8-9)": {'nums': [7, 8, 9], 'type': 'OPERATIONAL', 'desc': 'Reaper Bloodline'},
        "THE ALCHEMIST (1-5-7)": {'nums': [1, 5, 7], 'type': 'EXOTIC', 'desc': 'Transmuter Bloodline'},
        "THE SIREN (2-7-6)": {'nums': [2, 7, 6], 'type': 'EXOTIC', 'desc': 'Glamour Bloodline'},
        "THE BERSERKER (4-9-2)": {'nums': [4, 9, 2], 'type': 'EXOTIC', 'desc': 'Storm Bringer Bloodline'}
    }
    
    detected_bloodlines = []
    
    # Calculate Day Sum for Anchor Logic
    day_sum = sum(int(d) for d in str(dob_day))
    while day_sum > 9 and day_sum != 11 and day_sum != 22:
        day_sum = sum(int(d) for d in str(day_sum))

    # 2. SCAN AND SCORE
    for name, data in bloodlines.items():
        # Check for Triple 6 special case
        if data.get('special') == 'triple_6':
            if grid_counts.get(6, 0) >= 3:
                score = 100 # Immediate High Score
                detected_bloodlines.append({'name': name, 'score': score, 'data': data})
            continue

        # Standard Triad Check
        nums = data['nums']
        if all(grid_counts.get(n, 0) > 0 for n in nums):
            score = 10 # Base Score for Existence
            
            # A. INTENSITY BONUS (More numbers = Stronger signal)
            total_count = sum(grid_counts.get(n, 0) for n in nums)
            score += (total_count - 3) * 5 # +5 points for every extra digit beyond the base 3
            
            # B. ANCHOR BONUS (Does this bloodline contain your Soul/Day Number?)
            if day_sum in nums:
                score += 30 # HUGE Boost: This is WHO YOU ARE
                
            # C. DESTINY BONUS (Does this bloodline contain your Lifepath?)
            if lifepath_number in nums:
                score += 20 # Large Boost: This is your MISSION
            
            # D. TYPE BIAS (Divine gets slight nudge if day is odd, Dark if even? No, keep neutral)
            
            detected_bloodlines.append({'name': name, 'score': score, 'data': data})

    # 3. SORT AND DISPLAY
    if not detected_bloodlines:
        print("    -> [NULL] THE CLAY BORN: No activated bloodline vectors.")
        return

    # Sort by score descending
    detected_bloodlines.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"    [ANALYSIS COMPLETE] {len(detected_bloodlines)} POTENTIAL FREQUENCIES DETECTED.")
    print("    [CALCULATING DOMINANCE HIERARCHY...]")
    
    for i, item in enumerate(detected_bloodlines):
        rank = ""
        if i == 0: rank = "PRIMARY (DOMINANT)"
        elif i == 1: rank = "SECONDARY (SUPPORT)"
        else: rank = "MINOR (DORMANT)"
        
        print(f"    -> [{rank}] {item['name']} | SCORE: {item['score']}")
        print(f"       TYPE: {item['data']['type']} | ROLE: {item['data']['desc']}")
        
    # 4. ELITE TRINITY LOCK CHECK (Keep this logic as it's separate from standard scoring)
    # [ELITE CHECK] THE PURE SOURCE CHILD (THE TRINITY LOCK)
    is_pure_child = False
    
    # 1. DAY ANALYSIS
    day_sum_calc = sum(int(d) for d in str(dob_day))
    while day_sum_calc > 9 and day_sum_calc != 11 and day_sum_calc != 22:
        day_sum_calc = sum(int(d) for d in str(day_sum_calc))
        
    # 2. LIFEPATH ANALYSIS
    is_33_vibration = False
    if lifepath_number == 33: is_33_vibration = True
    if raw_lifepath_sum == 24 or raw_lifepath_sum == 42: is_33_vibration = True
    
    # 3. HIDDEN MASTER CODES
    is_hidden_master_day = False
    if dob_day == 20: is_hidden_master_day = True
    if dob_day == 24: is_hidden_master_day = True
    
    # Check if 3-6-9 was detected at all
    has_369 = any(b['name'] == "THE ELOHIM (3-6-9)" for b in detected_bloodlines)
    
    if has_369:
        if day_sum_calc == 9:
            print("       *** [ALERT] TRINITY LOCK ALPHA: Day 9 + 3-6-9. DIRECT FRACTURE DETECTED.")
        if is_33_vibration:
             print(f"       *** [ALERT] TRINITY LOCK BETA: Master Lifepath (Raw: {raw_lifepath_sum}) + 3-6-9. CHRIST CONSCIOUSNESS.")
        if is_hidden_master_day or dob_day == 11 or dob_day == 22 or day_sum_calc == 11 or day_sum_calc == 22:
             print(f"       *** [ALERT] TRINITY LOCK GAMMA: Master Day ({dob_day}) + 3-6-9. HIGH COMMAND.")
        if grid_counts.get(3, 0) >= 2 and grid_counts.get(6, 0) >= 2 and grid_counts.get(9, 0) >= 2:
             print("       *** [ALERT] TRINITY LOCK OMEGA: Double 3-6-9. PURE SOURCE CONSCIOUSNESS.")

def analyze_hidden_master_codes(dob_day, raw_lifepath_sum, lifepath_number):
    """
    Analyzes Hidden Master Numbers and High Position Intersections.
    """
    print("\n[!] MASTER CODE SCAN (HIDDEN & OVERT):")
    
    masters_found = []
    
    # 1. DAY POSITION (SOUL CODE)
    day_code = None
    day_type = "NORMAL"
    
    # Check 11s
    if dob_day == 11: day_code = 11; day_type = "OVERT"
    elif dob_day == 29: day_code = 11; day_type = "COMPOSITE (29)"
    elif dob_day == 20: day_code = 11; day_type = "HIDDEN (THE SLEEPING PROPHET)"
    
    # Check 22s
    elif dob_day == 22: day_code = 22; day_type = "OVERT"
    
    # Check 33s (Rare for Day, max is 31, but theoretically possible in other systems)
    # 24 and 42 cannot be Days (max 31). But 24 can be a Day.
    elif dob_day == 24: day_code = 33; day_type = "HIDDEN (THE ELDER BUILDER)"
    
    if day_code:
        print(f"    -> [SOUL POSITION] DAY {dob_day} DETECTED AS MASTER {day_code} ({day_type}).")
        masters_found.append({'pos': 'SOUL', 'val': day_code, 'type': day_type})
        
    # 2. LIFEPATH POSITION (DESTINY CODE)
    lp_code = None
    lp_type = "NORMAL"
    
    if lifepath_number == 11: 
        lp_code = 11; lp_type = "OVERT"
        if raw_lifepath_sum == 29: lp_type = "COMPOSITE (29)"
        if raw_lifepath_sum == 38: lp_type = "COMPOSITE (38)"
        if raw_lifepath_sum == 47: lp_type = "COMPOSITE (47)"
    elif lifepath_number == 22:
        lp_code = 22; lp_type = "OVERT"
    elif lifepath_number == 33:
        lp_code = 33; lp_type = "OVERT"
    
    # HIDDEN LIFEPATH CHECKS (Override Standard Reduction)
    if raw_lifepath_sum == 20: lp_code = 11; lp_type = "HIDDEN (THE SLEEPING PROPHET)"
    if raw_lifepath_sum == 24: lp_code = 33; lp_type = "HIDDEN (THE ELDER BUILDER)"
    if raw_lifepath_sum == 42: lp_code = 33; lp_type = "HIDDEN (THE MIRROR BUILDER)"
    
    if lp_code:
        print(f"    -> [DESTINY POSITION] LIFEPATH {raw_lifepath_sum} DETECTED AS MASTER {lp_code} ({lp_type}).")
        masters_found.append({'pos': 'DESTINY', 'val': lp_code, 'type': lp_type})
        
    # 3. INTERSECTION ANALYSIS (WHAT HAPPENS IF YOU HAVE MORE THAN ONE?)
    if len(masters_found) == 0:
        print("    -> [NONE] No Master Codes active in High Positions.")
    elif len(masters_found) == 1:
        print(f"    -> [SINGLE ACTIVATION] Initiate is anchored by the {masters_found[0]['val']} Frequency.")
    elif len(masters_found) >= 2:
        print("\n    *** [CRITICAL] MULTI-MASTER ACTIVATION DETECTED ***")
        val1 = masters_found[0]['val']
        val2 = masters_found[1]['val']
        
        if val1 == 11 and val2 == 11:
            print("    -> [THE DOUBLE PORTAL (11:11)] PURE VISIONARY.")
            print("       The 'Mirror' Effect. You are a walking stargate. Highly ungrounded but psychic.")
        elif (val1 == 11 and val2 == 22) or (val1 == 22 and val2 == 11):
            print("    -> [THE ARCHITECT-PROPHET (11-22)] MASTER OF DREAMS & REALITY.")
            print("       You have the Vision (11) and the Tools to Build it (22). Very powerful CEO energy.")
        elif (val1 == 11 and val2 == 33) or (val1 == 33 and val2 == 11):
            print("    -> [THE CHRIST-MIND (11-33)] HIGHEST SPIRITUAL POTENTIAL.")
            print("       Direct channel to Source (11) teaching Universal Love (33).")
        elif val1 == 33 and val2 == 33:
            print("    -> [THE AVATAR (33:33)] WORLD TEACHER STATUS.")
            print("       Double Master Teacher. You are here to shift the collective consciousness.")
        else:
            print(f"    -> [HYBRID MASTER ({val1}-{val2})] COMPLEX HIGH FREQUENCY.")
            print("       You operate on multiple dimensions simultaneously.")

def analyze_solar_lunar_eclipse(s_lifepath, l_lifepath):
    """
    Analyzes the Solar vs. Lunar Lifepath Dynamic (The Eclipse Protocol).
    """
    if not l_lifepath: return

    print("\n[!] SOLAR/LUNAR ECLIPSE PROTOCOL (HYBRID ANALYSIS):")
    print(f"    [INPUTS] SOLAR (OUTER): {s_lifepath} | LUNAR (INNER): {l_lifepath}")

    # Check for the specific 11/33 Hybrid
    s_is_33 = (s_lifepath == 33 or s_lifepath == 24 or s_lifepath == 42)
    l_is_11 = (l_lifepath == 11 or l_lifepath == 20 or l_lifepath == 38 or l_lifepath == 29)
    
    # Also check reverse (Solar 11 / Lunar 33)
    s_is_11 = (s_lifepath == 11 or s_lifepath == 20 or s_lifepath == 38 or s_lifepath == 29)
    l_is_33 = (l_lifepath == 33 or l_lifepath == 24 or l_lifepath == 42)

    if (s_is_33 and l_is_11) or (s_is_11 and l_is_33):
        print("    *** [CRITICAL] THE HIDDEN AVATAR DETECTED (TYPE: ECLIPSE WALKER) ***")
        print("    -> DYNAMIC: You hold the VISION (11) internally and the STRUCTURE (33) externally.")
        print("    -> MISSION: You are here to 'Ground the Lightning'. You must build systems for your visions.")
        print("    -> WARNING: High friction between the urge to escape (11) and the duty to serve (33).")
    else:
        print("    -> [STANDARD] No specific Eclipse Hybrid detected.")

def analyze_hidden_elite_patterns(dob_digits, driver, conductor):
    """
    Analyzes specific rare patterns for Elite/Secret Society markers.
    """
    print("\n[!] ELITE HIDDEN PATTERN SCAN (SECRET KNOWLEDGE):")
    found_any = False
    
    # 1. THE VOID WALKER (3+ Zeros)
    zero_count = dob_digits.count(0)
    if zero_count >= 3:
        print(f"    -> [DETECTED] THE VOID WALKER (0-0-0): {zero_count} Zeros found. 'System Breaker' / Infiltrator Frequency.")
        found_any = True
        
    # 2. THE MASTER BUILDER (22)
    if driver == 22 or conductor == 22 or 22 in dob_digits:
        print("    -> [DETECTED] THE MASTER BUILDER (22): Masonic Structure. Architect of Reality.")
        found_any = True

    # 3. THE ROYAL STAR (23/5)
    # Check if born on 23rd specifically (need raw DOB string, but we have digits. 
    # Logic: if driver is 5, check if digits contain 2 and 3 sequentially? Hard with just list.
    # Simplified check: Driver 5 and Conductor 23? Or Driver 5 from 23.
    # We passed 'driver' as int. Let's assume if driver == 5, we check if 2 and 3 are in the day part.
    # For now, just check if 23 appears in digits? No, 23 could be year 2023.
    # Let's rely on the user input day being 23.
    # We will just check for the 5 energy with 2 and 3 present.
    if driver == 5 and (2 in dob_digits and 3 in dob_digits):
        print("    -> [POTENTIAL] THE ROYAL STAR (23/5): 'Lion's Protection' detected. Leadership favor.")
        found_any = True

    # 4. THE TESLA CODE (3-6-9 DOMINANCE)
    threes = dob_digits.count(3)
    sixes = dob_digits.count(6)
    nines = dob_digits.count(9)
    if (threes + sixes + nines) >= 3:
        print("    -> [DETECTED] THE TESLA MATRIX (3-6-9): High concentration of Source Code. Genius/Alien Intellect.")
        found_any = True

    # 5. THE ROCKEFELLER (8-5-6)
    if 8 in dob_digits and 5 in dob_digits and 6 in dob_digits:
        print("    -> [DETECTED] THE ROCKEFELLER CODE (8-5-6): Financial Mastery. The 'Banking' Triad.")
        found_any = True

    # 6. THE BLACK SUN (4-8-13)
    if (driver == 4 or driver == 8) and (conductor == 4 or conductor == 8):
        print("    -> [DETECTED] THE BLACK SUN (4-8): Heavy Saturn/Rahu Karma. Occult Power & 'Hard Magic'.")
        found_any = True

    if not found_any:
        print("    -> [NONE] No specific Elite Secret Society markers found.")

def analyze_polarity_paradox(grid_counts):
    """
    Analyzes the 'Sentry vs. Void' Polarity.
    Checks for the coexistence of Extreme Light (1, 3, 9) and Extreme Dark (4, 8, 7) numbers.
    """
    print("\n[!] POLARITY PARADOX SCAN (SENTRY/VOID PROTOCOL):")
    
    # LIGHT SCORE (Creation/Order)
    light_score = grid_counts.get(1, 0) + grid_counts.get(3, 0) + grid_counts.get(9, 0)
    
    # DARK SCORE (Destruction/Chaos/Shadow)
    dark_score = grid_counts.get(4, 0) + grid_counts.get(8, 0) + grid_counts.get(7, 0)

    print(f"    [METRICS] LIGHT FORCE: {light_score} | SHADOW FORCE: {dark_score}")

    if light_score >= 2 and dark_score >= 2:
        print("    -> [CRITICAL] SENTRY CLASS ENTITY DETECTED.")
        print("       STATUS: HIGH VOLATILITY. You hold both the 'Golden Sun' and 'The Void'.")
        print("       RISK: Self-Sabotage. When you build (Sentry), you unconsciously destroy (Void).")
        print("       CURE: Shadow Integration. Do not deny your dark side; harness it for protection.")
    elif light_score >= 3 and dark_score == 0:
        print("    -> [WARNING] SOLAR OVERLOAD (PURE SENTRY).")
        print("       STATUS: Toxic Positivity / Burnout.")
        print("       RISK: You are blinding others. You lack 'Grounding' (Darkness). Reality check needed.")
    elif dark_score >= 3 and light_score == 0:
        print("    -> [WARNING] VOID CONSUMPTION (PURE SHADOW).")
        print("       STATUS: Depression / Nihilism.")
        print("       RISK: You are drowning in the abyss. You need 'Solar' activation (Routine, Ego, Action).")
    else:
        print("    -> [BALANCED] STANDARD POLARITY. No extreme splitting detected.")

def main():
    print("----------------------------------------------------------------")
    print("   ZOPHIEL'S UNIVERSAL WEALTH & MATURATION CALCULATOR")
    print("   ELITE PROTOCOL: ACTIVATED")
    print("----------------------------------------------------------------")
    
    try:
        print("--- TARGET ANALYSIS MODE ---")
        s_day = int(input("ENTER TARGET DAY (DD): "))
        s_month = int(input("ENTER TARGET MONTH (MM): "))
        s_year = int(input("ENTER TARGET YEAR (YYYY): "))
        
        # [ELITE] LUNAR INPUT (OPTIONAL)
        l_lifepath_input = input("ENTER LUNAR LIFEPATH SUM (Optional - Press Enter to Skip): ")
        l_lifepath = int(l_lifepath_input) if l_lifepath_input.strip() else None
        
        # Universal Mode: We just use Solar data for simplicity unless specified
        l_day, l_month = s_day, s_month
            
    except ValueError:
        print("Invalid input. Using default ASHER SHEPHERD NEWTON (09/26/2005)")
        s_day, s_month, s_year = 26, 9, 2005
        l_day, l_month = 23, 8
        l_lifepath = None

    s_root = get_reduced_sum(s_day)
    
    # CALCULATE DESTINY NUMBER (CONDUCTOR)
    total_sum = sum(int(d) for d in str(s_day) + str(s_month) + str(s_year))
    s_destiny = get_reduced_sum(total_sum)
    
    print(f"\n[+] TARGET ROOT (DRIVER):    {s_root}")
    print(f"[+] TARGET DESTINY (CONDUCTOR): {s_destiny}")
    
    # GRID ANALYSIS (Using Root & Destiny as Anchors if missing)
    dob_string = str(s_day) + str(s_month) + str(s_year)
    dob_digits = [int(d) for d in dob_string if d.isdigit()]
    
    # [ELITE UPGRADE]: We NOW include the Driver (Root) and Conductor (Destiny) 
    # in the grid. This represents your "Evolved Self," not just your raw factory settings.
    # If your Life Path is 6, you HAVE the 6, even if it's not in your DOB.
    dob_digits.append(s_root)
    dob_digits.append(s_destiny)
    
    print(f"[+] GRID DIGITS (RAW + DERIVED): {dob_digits}")
    
    grid_counts = analyze_grid_arrows(dob_digits)
    analyze_spiritual_bloodlines(grid_counts, s_day, s_destiny, total_sum)
    analyze_hidden_master_codes(s_day, total_sum, s_destiny)
    
    # [ELITE] Solar/Lunar Check
    if l_lifepath:
        analyze_solar_lunar_eclipse(total_sum, l_lifepath) # Using raw total_sum for Solar
    
    analyze_hidden_elite_patterns(dob_digits, s_root, s_destiny)
    analyze_poverty_traps(grid_counts, s_root, s_destiny)
    
    # Get Maturation Ages
    s_activations = get_wealth_activation_ages(s_root)
    print(f"\n[+] WEALTH ACTIVATION AGES: {s_activations}")
    
    print("----------------------------------------------------------------")
    print(f"{'YEAR':<6} | {'AGE':<3} | {'POWER':<5} | {'ASSET':<5} | {'LIQUID':<6} | {'VERDICT'}")
    print("-" * 80)
    
    current_year = datetime.datetime.now().year
    
    for year in range(current_year, current_year + 50):
        age = year - s_year
        
        s_py = calculate_personal_year(s_day, s_month, year)
        l_py = s_py # Simplified for Universal Mode
        
        p_score, a_score, l_score = get_tri_material_score(s_py, l_py, age)
        
        # BOOST SCORE IF AGE IS A MATURATION AGE
        verdict = ""
        if age in s_activations:
            p_score = 100
            a_score = 100
            verdict = f"!! [ROOT {s_root} MATURES]"
        
        # Visual Bars
        def get_bar(score):
            if score >= 80: return "|||||"
            elif score >= 60: return "|||| "
            elif score >= 40: return "|||  "
            elif score >= 20: return "||   "
            else: return "|    "
            
        p_bar = get_bar(p_score)
        a_bar = get_bar(a_score)
        l_bar = get_bar(l_score)
        
        print(f"{year:<6} | {age:<3} | {p_bar:<5} | {a_bar:<5} | {l_bar:<6} | {verdict}")

if __name__ == "__main__":
    main()
