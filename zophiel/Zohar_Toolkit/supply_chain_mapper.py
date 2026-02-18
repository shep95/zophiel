from datetime import datetime, timedelta
from typing import Dict, List

# Note: The following are placeholders. A real implementation would require
# dedicated libraries for DNS lookups (e.g., dnspython), web scraping,
# package manager interactions, and vulnerability database lookups.

class SupplyChainMapper:
    """
    Map entire supply chain attack surface
    
    LAYERS:
    1. Direct dependencies (npm, pip packages)
    2. Infrastructure providers (AWS, Cloudflare)
    3. Third-party integrations (Stripe, Auth0)
    4. Contractors/vendors (from job postings, invoices)
    5. Open source maintainers (who can inject code)
    """

    def map_dependency_chain(self, target: str) -> Dict:
        """
        Build complete dependency graph
        """
        package_json = self._fetch_package_json(target)
        dep_tree = self._build_dependency_tree(package_json)
        risky_deps = self._identify_risky_dependencies(dep_tree)
        maintainers = self._map_maintainers(dep_tree)

        return {
            'total_dependencies': len(dep_tree),
            'risky_dependencies': risky_deps,
            'maintainer_count': len(maintainers),
            'supply_chain_risk_score': self._calculate_supply_chain_risk(risky_deps)
        }

    def _fetch_package_json(self, target: str) -> Dict:
        print(f"[!] Placeholder: Fetching package.json for {target}")
        return {
            "dependencies": {
                "express": "^4.17.1",
                "react": "^17.0.2",
                "old-and-unmaintained": "1.0.0"
            },
            "devDependencies": {
                "jest": "^27.0.0"
            }
        }

    def _build_dependency_tree(self, package_json: Dict) -> Dict:
        print("[!] Placeholder: Building full dependency tree")
        return {
            "express": {"version": "4.17.1", "maintainers": ["userA", "userB"], "last_commit_date": (datetime.now() - timedelta(days=30)).isoformat()},
            "react": {"version": "17.0.2", "maintainers": ["userC", "userD", "userE"], "last_commit_date": (datetime.now() - timedelta(days=15)).isoformat()},
            "old-and-unmaintained": {"version": "1.0.0", "maintainers": ["userF"], "last_commit_date": (datetime.now() - timedelta(days=800)).isoformat()},
            "single-maintainer-lib": {"version": "2.1.0", "maintainers": ["userG"], "last_commit_date": (datetime.now() - timedelta(days=100)).isoformat()},
            "vulnerable-lib": {"version": "3.0.1", "maintainers": ["userH", "userI"], "last_commit_date": (datetime.now() - timedelta(days=50)).isoformat()}
        }

    def _identify_risky_dependencies(self, dep_tree: Dict) -> List[Dict]:
        """
        Flag high-risk dependencies
        """
        risky = []
        for dep_name, dep_info in dep_tree.items():
            risk_score = 0
            risk_factors = []

            # Check maintenance status
            last_commit = dep_info.get('last_commit_date')
            if last_commit:
                days_since = (datetime.now() - datetime.fromisoformat(last_commit)).days
                if days_since > 730:  # 2 years
                    risk_score += 20
                    risk_factors.append('UNMAINTAINED')

            # Check maintainer count
            maintainer_count = len(dep_info.get('maintainers', []))
            if maintainer_count == 1:
                risk_score += 30
                risk_factors.append('SINGLE_MAINTAINER')

            # Check for recent maintainer changes (placeholder logic)
            if self._has_recent_maintainer_change(dep_name):
                risk_score += 40
                risk_factors.append('MAINTAINER_CHANGE')

            # Check known vulnerabilities (placeholder logic)
            vulns = self._check_vulnerabilities(dep_name, dep_info['version'])
            if vulns:
                risk_score += len(vulns) * 10
                risk_factors.append(f'KNOWN_VULNS_{len(vulns)}')

            if risk_score >= 30:
                risky.append({
                    'name': dep_name,
                    'version': dep_info['version'],
                    'risk_score': risk_score,
                    'risk_factors': risk_factors,
                    'maintainers': dep_info.get('maintainers', [])
                })
        return sorted(risky, key=lambda x: x['risk_score'], reverse=True)

    def _has_recent_maintainer_change(self, dep_name: str) -> bool:
        # Placeholder
        return dep_name == "vulnerable-lib"

    def _check_vulnerabilities(self, dep_name: str, version: str) -> List[str]:
        # Placeholder
        if dep_name == "vulnerable-lib":
            return ["CVE-2023-12345"]
        return []

    def _map_maintainers(self, dep_tree: Dict) -> Dict:
        # Placeholder
        maintainers = {}
        for dep, info in dep_tree.items():
            for m in info['maintainers']:
                if m not in maintainers:
                    maintainers[m] = []
                maintainers[m].append(dep)
        return maintainers

    def _calculate_supply_chain_risk(self, risky_deps: List[Dict]) -> float:
        if not risky_deps:
            return 0.0
        total_risk = sum(d['risk_score'] for d in risky_deps)
        return min(total_risk / 10, 100.0) # Normalize to a 0-100 score

    def map_infrastructure_providers(self, target: str) -> Dict:
        """
        Identify all infrastructure dependencies
        """
        providers = {
            'hosting': set(), 'cdn': set(), 'dns_provider': set(),
            'email': set(), 'payment': set(), 'auth': set(), 'analytics': set()
        }

        # DNS analysis
        dns_records = self._get_dns_records(target)
        if 'cloudflare' in str(dns_records).lower():
            providers['cdn'].add('Cloudflare')
        if 'fastly' in str(dns_records).lower():
            providers['cdn'].add('Fastly')
        if 'google' in str(dns_records['NS']).lower():
             providers['dns_provider'].add('Google Cloud DNS')

        # IP analysis for hosting
        ip = dns_records.get('A', [None])[0]
        if ip:
            ip_info = self._lookup_ip(ip)
            org = ip_info.get('organization', '').lower()
            if 'amazon' in org: providers['hosting'].add('AWS')
            elif 'microsoft' in org: providers['hosting'].add('Azure')
            elif 'google' in org: providers['hosting'].add('GCP')
        
        # JavaScript analysis for third-party services
        js_files_content = self._get_all_js_content(target)
        for content in js_files_content:
            if 'stripe' in content: providers['payment'].add('Stripe')
            if 'paypal' in content: providers['payment'].add('PayPal')
            if 'auth0' in content: providers['auth'].add('Auth0')
            if 'okta' in content: providers['auth'].add('Okta')
            if 'google-analytics' in content: providers['analytics'].add('Google Analytics')

        # Convert sets to lists for JSON serialization
        return {k: list(v) for k, v in providers.items()}

    def _get_dns_records(self, target: str) -> Dict:
        print(f"[!] Placeholder: Getting DNS records for {target}")
        return {
            'A': ['104.26.10.234'],
            'NS': ['dns.google.com'],
            'MX': ['smtp.google.com'],
            'TXT': ['"v=spf1 include:_spf.google.com ~all"']
        }

    def _lookup_ip(self, ip: str) -> Dict:
        print(f"[!] Placeholder: Looking up IP {ip}")
        return {'organization': 'AMAZON-02'}

    def _get_all_js_content(self, target: str) -> List[str]:
        print(f"[!] Placeholder: Fetching all JS content from {target}")
        return [
            '<script src="https://js.stripe.com/v3/"></script>',
            'var _gaq = _gaq || []; _gaq.push([\'_setAccount\', \'UA-XXXXX-Y\']);'
        ]
