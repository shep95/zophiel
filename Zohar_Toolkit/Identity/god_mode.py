import requests
import threading
import time
import random
import json
from datetime import datetime
from Identity.breach_check import BreachChecker
from Identity.entity_resolution import EntityResolver
from Zophiel.zophiel_core import ZophielEngine

class GodModeHunter:
    def __init__(self):
        self.breach_checker = BreachChecker()
        self.resolver = EntityResolver()
        self.zophiel = ZophielEngine()
        # High-Value Target Platforms for Enumeration (DISABLED PER USER REQUEST - FOCUSED ON HARD INTELLIGENCE)
        self.platforms = [
            # {"name": "GitHub", "url": "https://github.com/{}", "check": "status", "valid": 200},
            # {"name": "Instagram", "url": "https://www.instagram.com/{}/", "check": "content", "indicator": "\"og:type\" content=\"profile\""},
            # {"name": "Twitter/X", "url": "https://nitter.net/{}", "check": "status", "valid": 200}, 
            # {"name": "Twitch", "url": "https://m.twitch.tv/{}", "check": "content", "indicator": "twitch.tv"},
            # {"name": "Reddit", "url": "https://www.reddit.com/user/{}", "check": "content", "indicator": "profileId"},
            # {"name": "Spotify", "url": "https://open.spotify.com/user/{}", "check": "status", "valid": 200},
            # {"name": "Pinterest", "url": "https://www.pinterest.com/{}/", "check": "content", "indicator": "pinterest.com"},
            # {"name": "Steam", "url": "https://steamcommunity.com/id/{}", "check": "anti_content", "indicator": "The specified profile could not be found"},
            # {"name": "Telegram", "url": "https://t.me/{}", "check": "content", "indicator": "<div class=\"tgme_page_title\" dir=\"auto\">"},
            # {"name": "Pastebin", "url": "https://pastebin.com/u/{}", "check": "status", "valid": 200},
            # {"name": "Freelancer", "url": "https://www.freelancer.com/u/{}", "check": "status", "valid": 200},
            # {"name": "Roblox", "url": "https://www.roblox.com/user.aspx?username={}", "check": "status", "valid": 200},
            # {"name": "SoundCloud", "url": "https://soundcloud.com/{}", "check": "status", "valid": 200},
            # {"name": "Venmo", "url": "https://venmo.com/{}", "check": "status", "valid": 200},
            # {"name": "CashApp", "url": "https://cash.app/${}", "check": "status", "valid": 200},
            # {"name": "About.me", "url": "https://about.me/{}", "check": "status", "valid": 200},
            # {"name": "Medium", "url": "https://medium.com/@{}", "check": "status", "valid": 200},
            # {"name": "Wattpad", "url": "https://www.wattpad.com/user/{}", "check": "status", "valid": 200},
            # {"name": "Wikipedia", "url": "https://en.wikipedia.org/wiki/User:{}", "check": "status", "valid": 200},
            # {"name": "HackerNews", "url": "https://news.ycombinator.com/user?id={}", "check": "content", "indicator": "User:"},
            # {"name": "Academia.edu", "url": "https://independent.academia.edu/{}", "check": "status", "valid": 200},
            # {"name": "ResearchGate", "url": "https://www.researchgate.net/profile/{}", "check": "status", "valid": 200},
            # {"name": "SlideShare", "url": "https://www.slideshare.net/{}", "check": "status", "valid": 200},
            # {"name": "Flickr", "url": "https://www.flickr.com/people/{}", "check": "status", "valid": 200},
            # {"name": "Vimeo", "url": "https://vimeo.com/{}", "check": "status", "valid": 200},
            # {"name": "Patreon", "url": "https://www.patreon.com/{}", "check": "status", "valid": 200},
            # {"name": "Bandcamp", "url": "https://bandcamp.com/{}", "check": "status", "valid": 200},
            # {"name": "ProductHunt", "url": "https://www.producthunt.com/@{}", "check": "status", "valid": 200},
            # {"name": "Xbox Gamertag", "url": "https://xboxgamertag.com/search/{}", "check": "status", "valid": 200},
            # {"name": "PSNProfiles", "url": "https://psnprofiles.com/{}", "check": "status", "valid": 200},
            # {"name": "StackShare", "url": "https://stackshare.io/{}", "check": "status", "valid": 200},
            # {"name": "Gravatar", "url": "http://en.gravatar.com/{}", "check": "status", "valid": 200},
            # {"name": "Disqus", "url": "https://disqus.com/by/{}", "check": "status", "valid": 200},
            # {"name": "HubDocker", "url": "https://hub.docker.com/u/{}", "check": "status", "valid": 200}
        ]
        self.results = []
        self.lock = threading.Lock()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def execute_directive(self, name, dob=None, location=None, address=None):
        print(f"\n[*] ACTIVATING GOD-MODE SURVEILLANCE: {name.upper()}")
        print("="*60)
        
        # 1. Selector Generation
        print("[*] PHASE 1: GENERATING DIGITAL SELECTORS (Advanced Permutations)")
        selectors = self._generate_selectors(name, dob)
        emails = self._generate_emails(name, dob)
        print(f"    [+] Generated {len(selectors)} username probability vectors.")
        print(f"    [+] Generated {len(emails)} email probability vectors.")
        
        # 2. Active Interrogation (SKIPPED PER USER REQUEST)
        print(f"\n[*] PHASE 2: ACTIVE NETWORK INTERROGATION (SKIPPED - SOCIAL MEDIA DISABLED)")
        # print("    [>] Launching asynchronous probes against 12 high-traffic networks...")
        
        # Breach Check on Primary Email Guess
        if emails:
            print(f"\n[*] PHASE 2.5: CREDENTIAL COMPROMISE CHECK")
            primary_email = emails[0] # Most likely: first.last@gmail.com
            self.breach_checker.check_email(primary_email)
        
        threads = []
        # We limit to top 15 most likely selectors to cover middle name variations
        active_selectors = [] # selectors[:15] # DISABLED
        
        for username in active_selectors:
            t = threading.Thread(target=self._interrogate_network, args=(username, name, location))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        # 3. Zophiel Deep Web Scan (DuckDuckGo)
        print(f"\n[*] PHASE 3: DEEP WEB INTELLIGENCE (Zophiel Engine)")
        zophiel_report = self.zophiel.ignite(name, location)

        self._print_intelligence_report(name)
        
        public_records = self._generate_public_record_links(name, location)
        
        # Generate Report
        from Identity.html_reporter import IntelligenceReporter
        reporter = IntelligenceReporter()
        data = {
            'selectors': selectors,
            'emails': emails,
            'matches': self.results,
            'zophiel_intelligence': zophiel_report, # Added Zophiel Data
            'public_records': public_records,
            'address': address
        }
        reporter.generate_dossier(name, data, location=location)
        
        return data

    def _generate_public_record_links(self, name, location=None):
        """Generates massive list of passive search dorks for global intelligence."""
        links = []
        encoded_name = name.replace(" ", "+")
        
        # 1. CORE IDENTITY & PUBLIC RECORDS
        links.append({"source": "FamilySearch (Vital)", "url": f"https://www.familysearch.org/search/record/results?q.givenName={name.split()[0]}&q.surname={name.split()[-1]}"})
        links.append({"source": "OpenCorporates (Global Business)", "url": f"https://opencorporates.com/companies?q={encoded_name}"})
        links.append({"source": "Ancestry (Genealogy)", "url": f"https://www.ancestry.com/search/?name={name.split()[0]}_{name.split()[-1]}"})
        
        # 1b. CORPORATE & LLC HUNTING (LOGIC ADDED)
        links.append({"source": "Bizapedia (US Corporate)", "url": f"https://www.bizapedia.com/search.aspx?q={encoded_name}"})
        links.append({"source": "CorporationWiki", "url": f"https://www.corporationwiki.com/search/results?term={encoded_name}"})
        links.append({"source": "Google Dork (LLC Search)", "url": f"https://www.google.com/search?q=\"{name}\"+LLC+OR+Inc+OR+Owner"})
        links.append({"source": "OpenOwnership", "url": f"https://register.openownership.org/search?q={encoded_name}"})
        
        if location and ("florida" in location.lower() or "fl" in location.lower()):
            links.append({"source": "Florida Sunbiz (Official Corp Registry)", "url": f"https://search.sunbiz.org/Inquiry/CorporationSearch/ByName"})
            links.append({"source": "Florida DBPR (Licenses)", "url": f"https://www.myfloridalicense.com/wl11.asp?mode=0&SID="})
            links.append({"source": "Miami-Dade Property (If applicable)", "url": f"https://www.miamidade.gov/propertysearch/#/"})

        # 2. VEHICLE & TRANSPORT
        links.append({"source": "NHTSA VIN Decoder", "url": "https://vpic.nhtsa.dot.gov/decoder/"})
        links.append({"source": "FAA Registry (Aircraft)", "url": f"https://registry.faa.gov/aircraftinquiry/Search/NNumberInquiry"})
        links.append({"source": "FlightAware (Tracking)", "url": "https://flightaware.com/"})
        links.append({"source": "VesselFinder (Maritime)", "url": "https://www.vesselfinder.com/"})
        links.append({"source": "OpenRailwayMap", "url": "https://www.openrailwaymap.org/"})
        
        # 3. TELEPHONE & COMMUNICATIONS
        links.append({"source": "Truecaller", "url": "https://www.truecaller.com/"})
        links.append({"source": "NumLookup", "url": "https://www.numlookup.com/"})
        links.append({"source": "SpyDialer", "url": "https://spydialer.com/"})
        links.append({"source": "FCC License Search", "url": f"https://wireless2.fcc.gov/UlsApp/UlsSearch/results.jsp?qry={encoded_name}"})
        links.append({"source": "PhoneInfoga (Tool)", "url": "https://github.com/sundowndev/phoneinfoga"})
        links.append({"source": "CallerID Test (CNAM)", "url": "https://calleridtest.com/"})
        
        # 4. REAL ESTATE & ASSETS
        if location:
            links.append({"source": "Zillow (Location)", "url": f"https://www.zillow.com/homes/{location}_rb/"})
            links.append({"source": "Redfin", "url": f"https://www.redfin.com/city/{location}"})
            links.append({"source": "Trulia", "url": f"https://www.trulia.com/{location}"})
        else:
            links.append({"source": "Zillow (Global)", "url": "https://www.zillow.com/"})
        links.append({"source": "PropertyShark", "url": f"https://www.propertyshark.com/mason/search?q={encoded_name}"})
        links.append({"source": "Realtor.com", "url": f"https://www.realtor.com/realestateandhomes-search/{encoded_name}"})

        # 5. CRYPTO & FINANCIAL
        links.append({"source": "Blockchain.com Explorer", "url": "https://www.blockchain.com/explorer"})
        links.append({"source": "Etherscan (ETH)", "url": "https://etherscan.io/"})
        links.append({"source": "OXT.me (Bitcoin Graph)", "url": "https://oxt.me/"})
        links.append({"source": "Blockchair (Multi-Chain)", "url": "https://blockchair.com/search?q={encoded_name}"})
        links.append({"source": "BitRef", "url": "https://bitref.com/"})
        
        # 6. IMAGES & FACIAL RECOGNITION
        links.append({"source": "Yandex Images (Face)", "url": f"https://yandex.com/images/search?text={encoded_name}"})
        links.append({"source": "PimEyes (Facial Rec)", "url": "https://pimeyes.com/en"})
        links.append({"source": "TinEye (Reverse Image)", "url": "https://tineye.com/"})
        links.append({"source": "FaceCheck.id", "url": "https://facecheck.id/"})
        links.append({"source": "Google Lens", "url": "https://lens.google.com/"})
        
        # 7. PROFESSIONAL & NICHE
        links.append({"source": "LinkedIn", "url": f"https://www.linkedin.com/search/results/all/?keywords={encoded_name}"})
        links.append({"source": "Xing", "url": f"https://www.xing.com/search/members?keywords={encoded_name}"})
        links.append({"source": "ZoomInfo", "url": f"https://www.zoominfo.com/people/{name.replace(' ', '-')}"})
        links.append({"source": "Crunchbase", "url": f"https://www.crunchbase.com/text/search?q={encoded_name}"})
        links.append({"source": "RocketReach", "url": f"https://rocketreach.co/person?name={encoded_name}"})
        links.append({"source": "SignalHire", "url": "https://www.signalhire.com/"})
        
        # 8. GAMING & VIRTUAL WORLDS
        links.append({"source": "SteamID.uk", "url": "https://steamid.uk/"})
        links.append({"source": "Tracker.gg", "url": f"https://tracker.gg/search?q={encoded_name}"})
        links.append({"source": "Xbox Gamertag", "url": f"https://xboxgamertag.com/search/{encoded_name}"})
        links.append({"source": "Discord (Google Dork)", "url": f"https://www.google.com/search?q=site:discord.com+\"{name}\""})
        
        # 8b. DATING & SOCIAL
        links.append({"source": "Tinder (Dork)", "url": f"https://www.google.com/search?q=site:tinder.com+\"{name}\""})
        links.append({"source": "Bumble (Dork)", "url": f"https://www.google.com/search?q=site:bumble.com+\"{name}\""})
        links.append({"source": "Ashley Madison (Check)", "url": "https://ashleymadison.com/"})
        
        # 9. LEAKS & BREACHES
        links.append({"source": "HaveIBeenPwned", "url": "https://haveibeenpwned.com/"})
        links.append({"source": "Snusbase", "url": "https://snusbase.com/"})
        links.append({"source": "LeakCheck", "url": "https://leakcheck.io/"})
        links.append({"source": "DeHashed", "url": f"https://dehashed.com/search?query={encoded_name}"})
        links.append({"source": "Intelligence X", "url": f"https://intelx.io/?s={encoded_name}"})
        links.append({"source": "BreachDirectory", "url": "https://breachdirectory.org/"})
        
        # 10. ACADEMIC & SCIENTIFIC
        links.append({"source": "Google Scholar", "url": f"https://scholar.google.com/scholar?q={encoded_name}"})
        links.append({"source": "ORCID", "url": f"https://orcid.org/orcid-search/search?searchQuery={encoded_name}"})
        links.append({"source": "ResearchGate", "url": f"https://www.researchgate.net/search?q={encoded_name}"})
        
        # 10b. LICENSES & CERTIFICATIONS
        links.append({"source": "State Bar Association (Legal)", "url": f"https://www.google.com/search?q=site:barassociation.org+\"{name}\""})
        links.append({"source": "Medical Board (License)", "url": f"https://www.google.com/search?q=\"{name}\"+medical+license+lookup"})
        links.append({"source": "Contractor License", "url": f"https://www.google.com/search?q=\"{name}\"+contractor+license"})
        links.append({"source": "Amateur Radio (FCC)", "url": f"https://wireless2.fcc.gov/UlsApp/UlsSearch/searchLicense.jsp"})

        # 10c. DATA BROKERS (Opt-Out/Index)
        links.append({"source": "Spokeo", "url": f"https://www.spokeo.com/{name.replace(' ', '-')}"})
        links.append({"source": "BeenVerified", "url": f"https://www.beenverified.com/people/{name.replace(' ', '-')}"})
        links.append({"source": "Intelius", "url": f"https://www.intelius.com/people-search/{name.replace(' ', '-')}"})
        links.append({"source": "Acxiom", "url": "https://isapps.acxiom.com/optout/optout.aspx"})
        links.append({"source": "Radaris", "url": f"https://radaris.com/p/{name.split()[0]}/{name.split()[-1]}"})
        links.append({"source": "Whitepages", "url": f"https://www.whitepages.com/name/{name.replace(' ', '-')}"})
        
        # 11. INTERNATIONAL REGISTRIES
        links.append({"source": "OpenCorporates (Offshore)", "url": f"https://opencorporates.com/companies?q={encoded_name}"})
        links.append({"source": "Companies House (UK)", "url": f"https://find-and-update.company-information.service.gov.uk/search?q={encoded_name}"})
        links.append({"source": "Qichacha (China)", "url": "https://www.qichacha.com/"})
        links.append({"source": "Zefix (Switzerland)", "url": "https://www.zefix.ch/en/search/entity/list"})
        links.append({"source": "Handelsregister (Germany)", "url": "https://www.handelsregister.de/"})
        
        links.append({"source": "Wayback Machine", "url": f"https://web.archive.org/web/*/{encoded_name}"})
        return links

    def _generate_emails(self, name, dob=None):
        """
        Generates likely corporate and personal email formats.
        """
        parts = name.lower().split()
        if len(parts) < 2:
            return []
        
        first, last = parts[0], parts[-1]
        domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com"]
        
        email_formats = [
            f"{first}.{last}",
            f"{first}{last}",
            f"{first}_{last}",
            f"{last}.{first}",
            f"{first[0]}{last}"
        ]

        if dob:
            # Add year-based email formats
            try:
                # Handle YYYY-MM-DD format
                dt = datetime.strptime(dob, "%Y-%m-%d")
                yy = str(dt.year)[-2:]
                yyyy = str(dt.year)
                
                email_formats.append(f"{first}{last}{yy}")
                email_formats.append(f"{first}{last}{yyyy}")
                email_formats.append(f"{first}.{last}{yy}")
                email_formats.append(f"{first}_{last}{yy}")
            except:
                pass
        
        generated = []
        for fmt in email_formats:
            for domain in domains:
                generated.append(f"{fmt}@{domain}")
                
        return generated

    def _generate_selectors(self, name, dob=None):
        """
        Generates advanced username permutations based on common psychological patterns.
        """
        parts = name.lower().split()
        if len(parts) < 2:
            return [name.lower()]
        
        first, last = parts[0], parts[-1]
        middle = parts[1] if len(parts) > 2 else ""

        base_selectors = [
            f"{first}{last}",         # johnsmith
            f"{first}.{last}",        # john.smith
            f"{first}_{last}",        # john_smith
            f"{first}{last[0]}",      # johns
            f"iam{first}",            # iamjohn
            f"{last}.{first}",        # smith.john
        ]
        
        # Middle Name Permutations (High Value for "Shepherd")
        if middle:
            base_selectors.extend([
                f"{first}{middle}",          # ashershepherd
                f"{first}.{middle}",         # asher.shepherd
                f"{first}_{middle}",         # asher_shepherd
                f"{middle}{last}",           # shepherdnewton
                f"{middle}.{last}",          # shepherd.newton
                f"{first}{middle}{last}",    # ashershepherdnewton
                f"{first}.{middle}.{last}",  # asher.shepherd.newton
                f"{first[0]}{middle}{last}", # ashepherdnewton
                f"{first[0]}.{middle}.{last}" # a.shepherd.newton
            ])

        if dob:
            try:
                dt = datetime.strptime(dob, "%Y-%m-%d")
                yy = str(dt.year)[-2:]
                yyyy = str(dt.year)
                mm = f"{dt.month:02d}"
                dd = f"{dt.day:02d}"
                
                dob_selectors = [
                    f"{first}{last}{yy}",      # ashernewton05
                    f"{first}{last}{yyyy}",    # ashernewton2005
                    f"{first}.{last}{yy}",     # asher.newton05
                    f"{first}_{last}{yy}",     # asher_newton05
                    f"{first}{mm}{dd}",        # asher0926
                    f"{first}{last}{mm}{dd}",  # ashernewton0926
                    f"{last}{yy}",             # newton05
                    f"{first}{yyyy}",          # asher2005
                ]
                if middle:
                    dob_selectors.append(f"{first}{middle[0]}{last}{yy}") # asherSnewton05
                    dob_selectors.append(f"{first}{middle}{yy}")          # ashershepherd05
                    dob_selectors.append(f"{middle}{last}{yy}")           # shepherdnewton05
                
                return dob_selectors + base_selectors
            except:
                pass
        
        # Fallback to random years if no DOB logic applied
        years = [str(y) for y in range(1985, 2005)]
        selected_years = random.sample(years, 2)
        
        # Add year variations
        for b in base_selectors[:2]:
            for y in selected_years:
                base_selectors.append(f"{b}{y}")
                base_selectors.append(f"{b}{y[-2:]}") # last 2 digits
        
        # --- ELITE MODIFICATIONS (Leet Speak & Suffixes) ---
        leet_selectors = []
        suffixes = ["_official", "official", "_real", "real", "_private", "private", "1", "123", "01"]
        
        for sel in base_selectors:
            # Suffixes
            for suf in suffixes[:3]: # Limit to avoid explosion
                 leet_selectors.append(f"{sel}{suf}")
            
            # Simple Leet Speak (a->4, e->3, i->1, o->0)
            if 'a' in sel or 'e' in sel or 'i' in sel or 'o' in sel:
                leet = sel.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0')
                leet_selectors.append(leet)

        return base_selectors + leet_selectors

    def _interrogate_network(self, username, target_name=None, location=None):
        """
        Checks if the username exists on defined platforms and optionally verifies content.
        """
        for site in self.platforms:
            url = site["url"].format(username)
            try:
                r = requests.get(url, headers=self.headers, timeout=5)
                exists = False
                
                if site["check"] == "status":
                    if r.status_code == site["valid"]:
                        exists = True
                elif site["check"] == "content":
                    if site["indicator"] in r.text:
                        exists = True
                
                # ENTITY RESOLUTION ENGINE (The Brain)
                confidence = "POSSIBLE"
                metadata = {}
                if exists and target_name:
                    # Delegate to Entity Resolution Engine
                    score, confidence, metadata = self.resolver.calculate_confidence(target_name, r.text, location)

                if exists:
                    with self.lock:
                        self.results.append({
                            "platform": site["name"],
                            "username": username,
                            "url": url,
                            "status": "CONFIRMED",
                            "confidence": confidence,
                            "metadata": metadata
                        })
                        if confidence != "LOW (Name Not Found)":
                            print(f"    [!] MATCH FOUND: {site['name']} -> {username} [{confidence}]")
                        
            except:
                pass

    def _print_intelligence_report(self, name):
        print("\n" + "="*60)
        print(f"GOD-MODE INTELLIGENCE DOSSIER: {name.upper()}")
        print("="*60)
        
        if self.results:
            print(f"\n[+] CONFIRMED DIGITAL FOOTPRINT ({len(self.results)} Matches)")
            for res in self.results:
                print(f"    [{res['platform']}] {res['username']}")
                print(f"    └── URI: {res['url']}")
        else:
            print("\n[-] No direct public matches found on primary networks.")
            print("    Target may practice good OpSec or use aliases.")

        # Pattern of Life Analysis (Simulated based on findings)
        print(f"\n[+] PATTERN OF LIFE ANALYSIS (Predictive)")
        print("    -----------------------------------------")
        if any(r['platform'] == 'GitHub' for r in self.results):
            print("    > ROLE: Developer / Technical Entity")
            print("    > VECTORS: Check email in commit history (git log).")
        if any(r['platform'] in ['Instagram', 'Pinterest'] for r in self.results):
            print("    > EXIF RISK: High probability of geolocation data in images.")
        if any(r['platform'] == 'Twitter/X' for r in self.results):
            print("    > SENTIMENT: Available for NLP/Psychometric profiling.")
            
        print(f"\n[+] RECOMMENDED NEXT ACTIONS")
        print("    1. DEEP-DIVE: Clone GitHub repos for secret scanning.")
        print("    2. SOCMINT: Scrape Instagram followers for relationship graph.")
        print("    3. BREACH: Cross-reference '{name}' in DeHashed/IntelX.")
        print("="*60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Zohar God Mode Hunter")
    parser.add_argument("--target", required=True, help="Target Name")
    parser.add_argument("--dob", help="Date of Birth (YYYY-MM-DD)")
    parser.add_argument("--location", help="Target Location")
    args = parser.parse_args()
    
    gm = GodModeHunter()
    gm.execute_directive(args.target, args.dob, args.location)
