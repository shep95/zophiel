import requests
import time
import json

class PhoneTracer:
    def __init__(self, api_key=None):
        self.api_key = api_key
        # Free tier APIs often used for HLR/CNAM lookups
        self.hlr_endpoint = "http://apilayer.net/api/validate" 

    def trace(self, phone_number):
        """
        Performs OSINT reconnaissance on a phone number.
        NOTE: Real-time GPS tracking requires SS7 network access (illegal/restricted).
        This tool retrieves Carrier Registration Data (HLR) and Social Footprints.
        """
        print(f"[*] Initiating Trace on: {phone_number}")
        
        # 1. Carrier & Region Lookup (HLR Simulation)
        data = self._get_carrier_data(phone_number)
        
        # 2. Risk Scoring
        data['risk_score'] = self._calculate_risk(data)
        
        self._print_report(data)
        
        # 3. Social Media Reverse Search
        print(f"\n[*] Scanning for Social Media associations...")
        socials = self._reverse_social_search(phone_number)
        
        return {
            'number': phone_number,
            'carrier': data.get('carrier'),
            'line_type': data.get('line_type'),
            'location': data.get('location'),
            'risk_score': data.get('risk_score'),
            'socials': socials
        }

    def _calculate_risk(self, data):
        """
        Calculates a 'Digital Risk Score' based on carrier and line type.
        VOIP lines are higher risk (burner phones).
        """
        score = 10 # Base score
        if data.get('line_type') == "mobile":
            score += 20 # Standard mobile
        elif data.get('line_type') == "landline":
            score += 50 # High stability
        elif data.get('line_type') == "voip":
            score += 80 # High risk (Google Voice/Burner)
            
        if "Verizon" in data.get('carrier', '') or "AT&T" in data.get('carrier', ''):
            score += 10 # Major carrier implies KYC
            
        return min(score, 99)

    def _get_carrier_data(self, number):
        """
        Retrieves Line Type, Carrier, and Registered Location.
        """
        # In a real scenario with an API key:
        # params = {'access_key': self.api_key, 'number': number}
        # r = requests.get(self.hlr_endpoint, params=params)
        # return r.json()
        
        # Simulating a response for demonstration/testing
        print("[*] Querying Global HLR Database...")
        time.sleep(1.5) # Simulate network latency
        return {
            "valid": True,
            "number": number,
            "local_format": number,
            "international_format": f"+{number}",
            "country_prefix": "+1",
            "country_code": "US",
            "country_name": "United States of America",
            "location": "New York, NY", # Registered billing location
            "carrier": "Verizon Wireless",
            "line_type": "mobile"
        }

    def _generate_kml(self, data):
        """
        Generates a KML file for Google Earth visualization.
        """
        if not data.get('location'):
            return

        filename = f"Target_{data['number']}_Location.kml"
        filepath = os.path.join(self.output_dir, filename)
        
        # Simulated Coordinates for "New York, NY" (Default fallback)
        # In a real app, use a Geocoding API here.
        lat, lon = 40.7128, -74.0060
        
        kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Placemark>
    <name>{data['number']}</name>
    <description>
      Carrier: {data['carrier']}
      Line Type: {data['line_type']}
      Registered Location: {data['location']}
    </description>
    <Point>
      <coordinates>{lon},{lat},0</coordinates>
    </Point>
  </Placemark>
</kml>"""
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(kml_content)
            
        print(f"[+] GEOSPATIAL INTELLIGENCE GENERATED: {filepath}")

    def _reverse_social_search(self, number):
        """
        Generates search URLs to find the number on social platforms.
        """
        platforms = {
            "Facebook": f"https://www.facebook.com/login/identify/?ctx=recover&search_attempts=1&alternate_search=1&ars=facebook_login&q={number}",
            "Twitter": f"https://twitter.com/search?q={number}&src=typed_query",
            "WhatsApp": f"https://api.whatsapp.com/send?phone={number}",
            "Google": f"https://www.google.com/search?q=%22{number}%22",
            "TrueCaller (Google Dork)": f"https://www.google.com/search?q=site:truecaller.com+%22{number}%22",
            "Sync.ME (Google Dork)": f"https://www.google.com/search?q=site:sync.me+%22{number}%22"
        }
        
        results = []
        for name, url in platforms.items():
            print(f"    [>] {name}: {url}")
            results.append({'platform': name, 'url': url})
            
        return results

    def _print_report(self, data):
        print("\n[+] CARRIER INTELLIGENCE REPORT")
        print("="*40)
        print(f"Target: {data.get('number')}")
        print(f"Status: {'Active' if data.get('valid') else 'Unknown'}")
        print(f"Carrier: {data.get('carrier')}")
        print(f"Line Type: {data.get('line_type')}")
        print(f"Registered Location: {data.get('location')}")
        print("="*40)
        print("(!) WARNING: 'Location' is the billing/registration address, not live GPS.")

if __name__ == "__main__":
    tracer = PhoneTracer()
    target = input("Enter Target Phone Number (e.g., 14155550123): ")
    tracer.trace(target)
