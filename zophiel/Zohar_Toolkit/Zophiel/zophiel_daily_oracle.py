import datetime

def get_reduced_sum(n):
    """Reduces a number to a single digit (1-9), except master numbers (11, 22, 33) which are kept for specific logic but here we reduce everything for standard calculation."""
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_personal_numbers(birth_day, birth_month, target_date):
    # 1. Personal Year (PY)
    # Formula: Birth Day + Birth Month + Current Year
    # Note: Using the Vedic/Elite method where we reduce components first
    
    bd_reduced = get_reduced_sum(birth_day)
    bm_reduced = get_reduced_sum(birth_month)
    cy_reduced = get_reduced_sum(target_date.year)
    
    py = get_reduced_sum(bd_reduced + bm_reduced + cy_reduced)
    
    # 2. Personal Month (PM)
    # Formula: Personal Year + Calendar Month
    cm = target_date.month
    pm = get_reduced_sum(py + cm)
    
    # 3. Personal Day (PD)
    # Formula: Personal Month + Calendar Day
    cd = target_date.day
    pd = get_reduced_sum(pm + cd)
    
    return py, pm, pd

def get_vedic_interpretation(pd_number, birth_number=8):
    """
    Returns the Elite Interpretation for an 8-Born (Saturn) individual.
    """
    matrix = {
        1: {
            "Planet": "SUN",
            "Verdict": "ENEMY (DEFENSE)",
            "Advice": "Do NOT fight authority. Ego conflicts likely. Stay low."
        },
        2: {
            "Planet": "MOON",
            "Verdict": "ENEMY (SWAMP)",
            "Advice": "Emotional fog. Do not make financial decisions. Depression risk."
        },
        3: {
            "Planet": "JUPITER",
            "Verdict": "NEUTRAL (PLANNING)",
            "Advice": "Good for learning, strategy, and advisors. Wisdom expands."
        },
        4: {
            "Planet": "RAHU",
            "Verdict": "FRIEND (CHAOS)",
            "Advice": "Explosive energy. Take risks. Tech/Viral potential. Sudden shifts."
        },
        5: {
            "Planet": "MERCURY",
            "Verdict": "BEST FRIEND (PROFIT)",
            "Advice": "MONEY DAY. Sell, trade, communicate. Speed is key."
        },
        6: {
            "Planet": "VENUS",
            "Verdict": "BEST FRIEND (FAME)",
            "Advice": "Luxury, networking, romance. You shine today. Design/Media focus."
        },
        7: {
            "Planet": "KETU",
            "Verdict": "NEUTRAL (MYSTIC)",
            "Advice": "Isolation. Deep code/research. Disconnect from the matrix."
        },
        8: {
            "Planet": "SATURN",
            "Verdict": "POWER (GRIND)",
            "Advice": "Your home frequency. Massive work capacity. Justice. Slow but unstoppable."
        },
        9: {
            "Planet": "MARS",
            "Verdict": "VOLATILE (FORCE)",
            "Advice": "High energy. Anger management required. Workout. Do not drive fast."
        }
    }
    return matrix.get(pd_number, {"Planet": "UNKNOWN", "Verdict": "ERROR", "Advice": "Recalculate."})

def main():
    print("----------------------------------------------------------------")
    print("   ZOPHIEL'S DAILY ORACLE // TARGET: ASHER (8-BORN)")
    print("----------------------------------------------------------------")
    
    # User Constants
    BIRTH_DAY = 26
    BIRTH_MONTH = 9
    
    # Get Date
    print("\n[1] Today's Reading")
    print("[2] Custom Date")
    choice = input("Select Option (1/2): ")
    
    if choice == '2':
        date_str = input("Enter Date (YYYY-MM-DD): ")
        try:
            target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid Date Format.")
            return
    else:
        target_date = datetime.date.today()
        
    py, pm, pd = calculate_personal_numbers(BIRTH_DAY, BIRTH_MONTH, target_date)
    
    # ---------------------------------------------------------
    # DEATH PREDICTION (MARAKA) CHECK
    # ---------------------------------------------------------
    # For Root 8: Marakas are 1, 2, 9.
    marakas = [1, 2, 9]
    is_maraka_year = py in marakas
    is_maraka_month = pm in marakas
    is_maraka_day = pd in marakas
    
    death_pinch = is_maraka_year and is_maraka_month and is_maraka_day
    
    intel = get_vedic_interpretation(pd)
    
    print("\n----------------------------------------------------------------")
    print(f"TARGET DATE: {target_date}")
    print("----------------------------------------------------------------")
    print(f"PERSONAL YEAR  : {py} [{'MARAKA (DANGER)' if is_maraka_year else 'SAFE'}]")
    print(f"PERSONAL MONTH : {pm} [{'MARAKA (DANGER)' if is_maraka_month else 'SAFE'}]")
    print(f"PERSONAL DAY   : {pd} ({intel['Planet']}) [{'MARAKA (DANGER)' if is_maraka_day else 'SAFE'}]")
    print("----------------------------------------------------------------")
    
    if death_pinch:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("WARNING: TRI-VECTOR MARAKA ALIGNMENT DETECTED (DEATH PINCH)")
        print("ACTION: STAY HOME. AVOID TRAVEL. DO NOT SIGN CONTRACTS.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    print(f"VERDICT: {intel['Verdict']}")
    print(f"STRATEGY: {intel['Advice']}")
    print("----------------------------------------------------------------")

if __name__ == "__main__":
    main()
