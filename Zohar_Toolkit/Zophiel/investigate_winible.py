from zophiel_core import ZophielEngine
import json
import os

def run():
    engine = ZophielEngine()
    
    print(">>> INITIATING WINIBLE PLATFORM DEEP DIVE <<<")
    
    # 1. Target: Noah Traisman (CEO)
    print("\n[*] Target 1: Noah Traisman (CEO)")
    report_ceo = engine.ignite(
        target_name="Noah Traisman", 
        location="Austin", # Or Miami, based on intel
        employer="Winible"
    )
    
    # 2. Target: Winible (The Platform itself)
    # We need to adapt the engine slightly or just use it with "Winible" as the name
    print("\n[*] Target 2: Winible.com (Platform Analysis)")
    # Using "Winible" as target name will trigger searches like "Winible" filetype:pdf, etc.
    report_platform = engine.ignite(
        target_name="Winible",
        location="United States",
        employer="SaaS"
    )

    print("\n[+] Investigation Complete. Data archived in Intelligence_Reports.")

if __name__ == "__main__":
    run()
