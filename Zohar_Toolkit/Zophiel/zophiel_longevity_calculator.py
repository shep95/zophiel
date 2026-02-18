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

def get_age(birth_year, target_year):
    return target_year - birth_year

def main():
    print("----------------------------------------------------------------")
    print("   ZOPHIEL'S LONGEVITY (AYURDAYA) CALCULATOR")
    print("   TARGET: ASHER SHEPHERD NEWTON (ROOT 8)")
    print("----------------------------------------------------------------")
    
    # Constants for Root 8
    BIRTH_DAY = 26
    BIRTH_MONTH = 9
    BIRTH_YEAR = 2005
    
    MARAKAS = [1, 2, 9] # Sun, Moon, Mars
    
    print(f"BIRTH: {BIRTH_YEAR}-09-26")
    print(f"MARAKA NUMBERS: {MARAKAS} (Danger)")
    print("----------------------------------------------------------------")
    print("SCANNING TIMELINE (2025 - 2105)...")
    print("----------------------------------------------------------------")
    
    print(f"{'YEAR':<6} | {'AGE':<4} | {'PY':<3} | {'ZONE':<10} | {'VERDICT'}")
    print("-" * 65)
    
    for year in range(2025, 2105):
        age = get_age(BIRTH_YEAR, year)
        py = calculate_personal_year(BIRTH_DAY, BIRTH_MONTH, year)
        
        # Zone Logic
        if age <= 33:
            zone = "ALPAYU"
            zone_desc = "Youth"
        elif age <= 66:
            zone = "MADHYAYU"
            zone_desc = "Mid-Life"
        else:
            zone = "PURNAYU"
            zone_desc = "End-Game"
            
        if py in MARAKAS:
            is_danger = True
            
            # Severity Logic
            if zone == "PURNAYU":
                severity = "**EXIT POINT PROBABILITY**"
            elif zone == "MADHYAYU":
                severity = "CRISIS / HEALTH SCARE"
            else:
                severity = "TRANSFORMATION / EGO DEATH"
                
            # Specific Planet
            planet_map = {1: "SUN", 2: "MOON", 9: "MARS"}
            planet = planet_map.get(py, "UNKNOWN")
            
            print(f"{year:<6} | {age:<4} | {py:<3} | {zone:<10} | {planet}: {severity}")
            
    print("-" * 65)
    print("NOTE: Root 8 (Saturn) usually survives until 'PURNAYU' Zone (Age 67+).")
    print("      Early Maraka years are spiritual/financial resets, not death.")
    print("----------------------------------------------------------------")
    
    # ---------------------------------------------------------
    # DRILL DOWN: MONTH & DAY ANALYSIS
    # ---------------------------------------------------------
    print("\n[!] DRILL DOWN: IDENTIFYING SPECIFIC 'EXIT DATES' FOR A MARAKA YEAR")
    target_year = int(input("ENTER A MARAKA YEAR TO SCAN (e.g. 2027 or 2081): "))
    
    analyze_micro_timing(BIRTH_DAY, BIRTH_MONTH, target_year, MARAKAS)

def analyze_micro_timing(bd, bm, year, marakas):
    print(f"\nScanning {year} for TRI-VECTOR CONVERGENCE (Year + Month + Day)...")
    print("----------------------------------------------------------------")
    
    py = calculate_personal_year(bd, bm, year)
    if py not in marakas:
        print(f"WARNING: {year} (PY {py}) is NOT a Maraka Year. Risk is low.")
    
    # Check Months
    print(f"{'DATE':<12} | {'PM':<3} | {'PD':<3} | {'VERDICT'}")
    print("-" * 50)
    
    count = 0
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = datetime.timedelta(days=1)
    
    current_date = start_date
    while current_date <= end_date:
        # Personal Month
        pm = get_reduced_sum(py + current_date.month)
        
        # Personal Day
        pd = get_reduced_sum(pm + current_date.day)
        
        # TRI-VECTOR CHECK: PY is Maraka (assumed) + PM is Maraka + PD is Maraka
        if (pm in marakas) and (pd in marakas):
            planet_map = {1: "SUN", 2: "MOON", 9: "MARS"}
            trigger = planet_map.get(pd, "Unknown")
            print(f"{current_date} | {pm:<3} | {pd:<3} | ** DEATH PINCH ** ({trigger})")
            count += 1
            
        current_date += delta
        
    print("-" * 50)
    print(f"TOTAL HIGH-RISK DATES FOUND IN {year}: {count}")
    print("----------------------------------------------------------------")

if __name__ == "__main__":
    main()
