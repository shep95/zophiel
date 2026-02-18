import os
import json
from datetime import datetime

class IntelligenceReporter:
    def __init__(self, output_dir="Intelligence_Reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_dossier(self, target_name, data, mode="person", location=None):
        filename = f"{target_name.replace(' ', '_')}_Dossier.html"
        filepath = os.path.join(self.output_dir, filename)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        loc_str = f"LOCATION: {location.upper()}<br>" if location else ""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ZOHAR INTELLIGENCE DOSSIER: {target_name.upper()}</title>
            <style>
                body {{ background-color: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }}
                h1 {{ border-bottom: 2px solid #00ff41; padding-bottom: 10px; }}
                h2 {{ color: #fff; margin-top: 30px; border-left: 4px solid #00ff41; padding-left: 10px; }}
                .box {{ border: 1px solid #333; background: #111; padding: 15px; margin-bottom: 20px; }}
                .alert {{ color: #ff3333; font-weight: bold; }}
                .metadata {{ color: #888; font-size: 0.8em; margin-bottom: 30px; }}
                a {{ color: #00ccff; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
                th {{ background-color: #222; color: #fff; }}
            </style>
        </head>
        <body>
            <h1>CLASSIFIED INTELLIGENCE DOSSIER</h1>
            <div class="metadata">
                TARGET: {target_name.upper()}<br>
                {loc_str}
                GENERATED: {timestamp}<br>
                CLEARANCE: LEVEL 5 (GOD MODE)
            </div>

            <div class="box">
                <h2>EXECUTIVE SUMMARY</h2>
                <p>Automated surveillance conducted by ZOHAR toolkit. Target analyzed for digital footprint, social graph anomalies, and potential compromise vectors.</p>
            </div>
        """

        if mode == "person":
            html_content += self._render_person_section(data)
        elif mode == "phone":
            html_content += self._render_phone_section(data)

        # Address Section (If Available)
        if data.get('address'):
            html_content += self._render_address_section(data.get('address'))

        html_content += """
            <div class="box">
                <h2>INTELLIGENCE FRAMEWORK & METHODOLOGY</h2>
                
                <!-- 1. Data Acquisition Layer -->
                <h3>1. Data Acquisition Layer (Public Sources Only)</h3>
                <p>Modular acquisition from legally accessible datasets (The Canon of 2,249 Laws):</p>
                <table>
                    <tr><th>Category</th><th>Sources</th></tr>
                    <tr><td><strong>Public Records (US)</strong></td><td>Vital Records (FamilySearch, Obituaries), Property (Zillow, County Assessor), Court (PACER, CourtListener), Voter Rolls, Professional Licenses (State Bar/Medical Boards).</td></tr>
                    <tr><td><strong>People Search Aggregators</strong></td><td>Pipl (Email/Phone correlation), Spokeo/Whitepages (Consumer-grade), TLOxp/IRBsearch (Professional/Licensed PI tools).</td></tr>
                    <tr><td><strong>International</strong></td><td>UK (Companies House, 192.com), EU (Business Registers, OpenSanctions), Global (OpenCorporates - 120+ jurisdictions, Offshore Leaks).</td></tr>
                    <tr><td><strong>Digital Footprint</strong></td><td>WHOIS/DNS (SecurityTrails, ViewDNS), Certificates (crt.sh, Shodan), Web History (Wayback Machine, URLScan.io).</td></tr>
                    <tr><td><strong>Email/Username OSINT</strong></td><td>Have I Been Pwned (Breach), Sherlock (Username enumeration), Holehe (Email-to-service), MOSINT.</td></tr>
                    <tr><td><strong>Telephone & Comms</strong></td><td>Truecaller, NumLookup, SpyDialer, FCC License Search, PhoneInfoga, CNAM Lookup.</td></tr>
                    <tr><td><strong>Crypto & Blockchain</strong></td><td>Blockchain.com Explorer, Etherscan (ETH/ENS), OXT.me (Bitcoin Graph), Chainalysis Reactor, Blockchair.</td></tr>
                    <tr><td><strong>Vehicle & Transport</strong></td><td>VINCheck (NHTSA), FAA Registry (Aircraft), FlightAware (ADS-B), VesselFinder (Maritime), OpenRailwayMap.</td></tr>
                    <tr><td><strong>Geolocation</strong></td><td>OpenStreetMap (Nominatim), Sentinel Hub (Satellite), ShadowMap (SunCalc), ADS-B Exchange (Transport), Strava Heatmap.</td></tr>
                    <tr><td><strong>SOCMINT</strong></td><td>Twitter/X (Nitter, TweetDeck), LinkedIn (Sales Navigator), Facebook (Graph), Instagram/TikTok (Picuki), Reddit (Pushshift), Forums (BoardReader).</td></tr>
                    <tr><td><strong>Gaming & Virtual Worlds</strong></td><td>SteamID.uk, Tracker.gg (Fortnite/Valorant), Xbox Gamertag, PSNProfiles, Discord (Disboard), VRChat.</td></tr>
                    <tr><td><strong>Corporate & Financial</strong></td><td>OpenCorporates, SEC EDGAR, Orbis (Moody's), OpenOwnership, Sanctions (OFAC, OpenSanctions, World-Check), GDELT (Adverse Media).</td></tr>
                    <tr><td><strong>Dark Web (Legal)</strong></td><td>RansomWatch (Leak sites), Have I Been Pwned, DeHashed, DarkSearch.io (Tor indexing).</td></tr>
                    <tr><td><strong>Academic & Deep Web</strong></td><td>Google Scholar, Archive.org, Academia.edu, ResearchGate, Scribd/DocPlayer (Uploaded docs).</td></tr>
                </table>

                <br>

                <!-- 2. Identity Resolution Engine -->
                <h3>2. Identity Resolution Engine (The "Brain")</h3>
                <p><strong>Entity Resolution Stack:</strong></p>
                <ul>
                    <li><strong>Probabilistic Record Linking:</strong> Bayesian matching on name variants, DOB, address history.</li>
                    <li><strong>Graph Database:</strong> Neo4j linking emails → domains → phone numbers → associates.</li>
                    <li><strong>Username Correlation:</strong> Sherlock-style enumeration across 400+ platforms.</li>
                    <li><strong>Image Forensics:</strong> ExifTool metadata, reverse image search (Google, TinEye).</li>
                    <li><strong>Geolocation Verification:</strong> Cross-referencing claimed location with digital footprint (Timezone, Language, IP).</li>
                </ul>

                <br>

                <!-- 3. Operational Security -->
                <h3>3. Operational Security (Analyst Protection)</h3>
                <ul>
                    <li><strong>Sock Puppet Management:</strong> Browser isolation, consistent persona backstopping.</li>
                    <li><strong>Infrastructure:</strong> Residential proxy rotation to avoid IP flagging.</li>
                    <li><strong>Virtual Machines:</strong> Whonix/Tails (Disposable VMs for malicious sites).</li>
                    <li><strong>Attribution Control:</strong> Dedicated hardware or cloud sandboxed browsers.</li>
                </ul>

                <br>

                <!-- 4. Recommended Stack -->
                <h3>4. Recommended Operational Stack</h3>
                <p>The ZOHAR Toolkit integrates the following high-value, stable APIs:</p>
                <ul>
                    <li><strong>Core Data:</strong> OpenCorporates (Business graph), SecurityTrails (Infrastructure), Have I Been Pwned (Breach).</li>
                    <li><strong>Discovery:</strong> Shodan (Device exposure), GDELT (News sentiment), OpenSanctions (Compliance).</li>
                    <li><strong>History:</strong> Wayback Machine (Historical web).</li>
                    <li><strong>Commercial Feeds (Optional):</strong> Pipl API, Flashpoint, LexisNexis.</li>
                </ul>

                <br>

                <!-- 5. Ethical & Legal Safeguards -->
                <h3>5. Ethical & Legal Safeguards (Non-Negotiable)</h3>
                <p><strong>Data Classification:</strong></p>
                <ul>
                    <li><strong>Public:</strong> Blog posts, press releases.</li>
                    <li><strong>Semi-Public:</strong> LinkedIn connections, Twitter followers.</li>
                    <li><strong>Private/Red Line:</strong> Financial records behind auth, private messages.</li>
                </ul>
                <p><strong>Compliance Automation:</strong> GDPR/CCPA Right to Erasure workflows, Data Retention Limits (Auto-purge after 30-90 days), Immutable Audit Logging.</p>
                <p><strong>Bias Mitigation:</strong> Source weighting (downranking unverified claims), Context preservation.</p>

                <br>
                
                <!-- 6. Operational Technology Stack -->
                <h3>6. Operational Technology Stack</h3>
                <p>Infrastructure powering the ZOHAR Intelligence Platform:</p>
                <table>
                    <tr><th>Function</th><th>Tool</th></tr>
                    <tr><td><strong>Data Collection</strong></td><td>Scrapy (Python), n8n (workflow automation), Huginn (self-hosted IFTTT)</td></tr>
                    <tr><td><strong>Storage</strong></td><td>Elasticsearch (full-text search), PostgreSQL (structured data), Neo4j (relationships)</td></tr>
                    <tr><td><strong>Processing</strong></td><td>Apache Kafka (streaming), spaCy (NLP entity extraction), Tika (document parsing)</td></tr>
                    <tr><td><strong>Visualization</strong></td><td>Kibana (dashboards), Maltego (link analysis), Leaflet (maps)</td></tr>
                    <tr><td><strong>OPSEC</strong></td><td>Whonix/Tails (OS), SpiderFoot HX (cloud OSINT automation)</td></tr>
                </table>
            </div>

            <div class="box">
                <h2>LEGAL DISCLAIMER</h2>
                <p class="metadata">This report is for authorized intelligence use only. The information contained herein was gathered from Open Source Intelligence (OSINT) vectors.</p>
            </div>
        </body>
        </html>
        """

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"\n[+] INTELLIGENCE DOSSIER GENERATED: {filepath}")
        return filepath

    def _render_person_section(self, data):
        # data expected: {'selectors': [], 'matches': [], 'emails': [], 'dorks': []}
        
        # 1. Synthesize Profile (AI Analyst)
        html = self._render_profile_synthesis(data)
        
        html += "<h2>DIGITAL IDENTITY SELECTORS</h2><div class='box'><ul>"
        for sel in data.get('selectors', [])[:10]:
            html += f"<li>{sel}</li>"
        html += "</ul></div>"

        html += "<h2>CONFIRMED DIGITAL FOOTPRINT</h2><div class='box'><table>"
        html += "<tr><th>PLATFORM</th><th>USERNAME</th><th>LINK</th></tr>"
        for match in data.get('matches', []):
            html += f"<tr><td>{match['platform']}</td><td>{match['username']}</td><td><a href='{match['url']}' target='_blank'>OPEN TARGET</a></td></tr>"
        html += "</table></div>"

        # Corporate Intelligence Section
        corp_matches = [m for m in data.get('matches', []) if m.get('metadata', {}).get('corporate')]
        if corp_matches:
            html += "<h2>CORPORATE & BUSINESS INTELLIGENCE</h2><div class='box'><table>"
            html += "<tr><th>ENTITY/PLATFORM</th><th>ROLE DETECTED</th><th>LINK</th></tr>"
            for match in corp_matches:
                roles = ", ".join(match['metadata']['corporate']).upper()
                html += f"<tr><td>{match['platform']}</td><td><span class='alert'>{roles}</span></td><td><a href='{match['url']}' target='_blank'>VIEW RECORD</a></td></tr>"
            html += "</table></div>"

        # Zophiel Intelligence Section
        zophiel_data = data.get('zophiel_intelligence', {})
        confirmed_intel = zophiel_data.get('confirmed_intelligence', [])
        
        if confirmed_intel:
            html += "<h2>ZOPHIEL DEEP WEB INTELLIGENCE (CONFIRMED)</h2><div class='box'><table>"
            html += "<tr><th>CONFIDENCE</th><th>TITLE</th><th>LINK</th></tr>"
            for item in confirmed_intel:
                html += f"<tr><td>{item.get('confidence_score', 0)}%</td><td>{item.get('title', 'N/A')}</td><td><a href='{item.get('url')}' target='_blank'>VIEW SOURCE</a></td></tr>"
                if item.get('extracted_pii'):
                     pii_str = str(item['extracted_pii'])
                     html += f"<tr><td colspan='3' style='color:#ffcc00'><strong>PII EXTRACTED:</strong> {pii_str}</td></tr>"
            html += "</table></div>"
            
        # Network Graph / Link Analysis Section
        network_graph = zophiel_data.get('network_graph', {})
        if network_graph and network_graph.get('links'):
            html += "<h2>LINK ANALYSIS MATRIX (NETWORK GRAPH)</h2><div class='box'>"
            html += "<p><em>Visualizing high-confidence connections between the Target and discovered entities.</em></p>"
            html += "<table><tr><th>SOURCE NODE</th><th>RELATIONSHIP</th><th>TARGET NODE</th></tr>"
            
            # Group links by source to make it readable
            for link in network_graph['links']:
                # Simple logic to determine relationship name based on value
                rel_name = "CONNECTED_TO"
                val = link.get('value', 1)
                if val == 5: rel_name = "PII_MATCH"
                elif val == 8: rel_name = "IDENTITY_CORRELATION"
                elif val == 2: rel_name = "FOUND_IN_SOURCE"
                
                html += f"<tr><td><strong>{link['source']}</strong></td><td style='color:#00ccff; text-align:center;'>--[{rel_name}]--></td><td><strong>{link['target']}</strong></td></tr>"
            html += "</table></div>"

        # Timeline Section (Agency Level)
        timeline = zophiel_data.get('timeline', [])
        if timeline:
            # Sort by year
            timeline.sort(key=lambda x: x['year'])
            html += "<h2>PATTERN OF LIFE TIMELINE</h2><div class='box'><table>"
            html += "<tr><th>YEAR</th><th>EVENT CONTEXT</th><th>SOURCE</th></tr>"
            for t in timeline:
                html += f"<tr><td><span class='alert'>{t['year']}</span></td><td>{t['event']}</td><td>{t['source']}</td></tr>"
            html += "</table></div>"

        if 'public_records' in data:
            html += "<h2>PUBLIC RECORDS & BACKGROUND CHECKS</h2><div class='box'><table>"
            html += "<tr><th>SOURCE</th><th>SEARCH LINK</th></tr>"
            for rec in data.get('public_records', []):
                html += f"<tr><td>{rec['source']}</td><td><a href='{rec['url']}' target='_blank'>EXECUTE QUERY</a></td></tr>"
            html += "</table></div>"

        html += "<h2>EMAIL PERMUTATION & BREACH VECTORS</h2><div class='box'><ul>"
        for email in data.get('emails', []):
            html += f"<li>{email} <span class='alert'>[CHECK BREACH]</span></li>"
        html += "</ul></div>"
        
        return html

    def _render_profile_synthesis(self, data):
        """Generates a narrative profile based on findings."""
        matches = data.get('matches', [])
        platforms = [m['platform'] for m in matches]
        
        roles = []
        if "GitHub" in platforms or "StackShare" in platforms or "HubDocker" in platforms:
            roles.append("Software Developer / Engineer")
        if "Xbox Gamertag" in platforms or "Steam" in platforms or "Twitch" in platforms:
            roles.append("Gamer / Interactive Media User")
        if "Academia.edu" in platforms or "ResearchGate" in platforms:
            roles.append("Academic Researcher / Student")
        if "LinkedIn" in platforms:
            roles.append("Corporate Professional")
            
        if not roles:
            roles.append("Low Digital Footprint (Privacy Conscious)")
            
        role_str = ", ".join(roles)
        
        # Address Guidance
        address_note = "Exact residential address is PII protected. Consult 'PUBLIC RECORDS' section below for Property Search (Zillow/County) and Voter Registration links."
        if any("florida" in r['url'].lower() for r in data.get('public_records', [])):
             address_note += " <span class='alert'>FLORIDA REGISTRY LINKS ACTIVE.</span>"

        return f"""
        <div class="box" style="border-left: 5px solid #00ccff;">
            <h2 style="margin-top:0; border:none; color:#00ccff;">SYNTHESIZED INTELLIGENCE PROFILE</h2>
            <table style="border:none;">
                <tr><td style="border:none; width: 150px;"><strong>PRIMARY ROLE:</strong></td><td style="border:none;">{role_str}</td></tr>
                <tr><td style="border:none;"><strong>DIGITAL ACTIVITY:</strong></td><td style="border:none;">Active across {len(platforms)} distinct platforms including {', '.join(platforms[:3])}.</td></tr>
                <tr><td style="border:none;"><strong>HOME ADDRESS:</strong></td><td style="border:none;">{address_note}</td></tr>
                <tr><td style="border:none;"><strong>CONFIDENCE:</strong></td><td style="border:none;">MEDIUM-HIGH (Based on Handle Correlation)</td></tr>
            </table>
        </div>
        """

    def _render_phone_section(self, data):
        # data expected: {'number': '', 'carrier': '', 'risk_score': 0, 'socials': []}
        html = f"""
        <h2>CARRIER INTELLIGENCE</h2>
        <div class='box'>
            <p><strong>NUMBER:</strong> {data.get('number')}</p>
            <p><strong>CARRIER:</strong> {data.get('carrier')}</p>
            <p><strong>LINE TYPE:</strong> {data.get('line_type')}</p>
            <p><strong>LOCATION:</strong> {data.get('location')}</p>
            <p><strong>RISK SCORE:</strong> <span class='alert'>{data.get('risk_score')}/100</span></p>
        </div>
        """
        
        html += "<h2>SOCIAL REVERSE SEARCH</h2><div class='box'><ul>"
        for social in data.get('socials', []):
            html += f"<li><strong>{social['platform']}:</strong> <a href='{social['url']}' target='_blank'>INITIATE TRACE</a></li>"
        html += "</ul></div>"
        
        return html
