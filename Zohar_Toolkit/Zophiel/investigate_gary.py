from zophiel_core import ZophielEngine

def run():
    engine = ZophielEngine()
    # User Request:
    # Target: Gary Gringberg (Correcting to Gary Grinberg for better results, will try to include alias if possible or just rely on broad search)
    # Location: Miami
    # Context: GG33
    
    # Note: I am using "Gary Grinberg" as the primary target name as it's the correct spelling for the GG33 founder.
    # The search queries in zophiel_core are now generalized to look for biography, business, etc.
    
    report = engine.ignite(
        target_name="Gary Grinberg", 
        location="Miami", 
        employer="GG33"
    )
    
    print("\n[+] Investigation Complete. Check the 'Intelligence_Reports' directory.")

if __name__ == "__main__":
    run()
