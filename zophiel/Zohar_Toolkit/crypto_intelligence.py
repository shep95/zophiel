import os
import requests
import re
from typing import List, Dict

class CryptoIntelligenceEngine:
    """ 
    Track cryptocurrency wallets, smart contracts, and on-chain relationships 
    
    USE CASES: 
    1. Identify company crypto wallets (follow funding transactions) 
    2. Map business relationships (who pays whom) 
    3. Detect money laundering patterns 
    4. Track ransomware payments 
    5. Identify infrastructure payments (hosting, domains) 
    """ 
    
    def __init__(self):
        # API keys for blockchain explorers
        self.etherscan_api = os.getenv('ETHERSCAN_API_KEY')
        self.btc_explorer_api = os.getenv('BLOCKCHAIN_INFO_API')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.ETHERSCAN_API_BASE_URL = "https://api.etherscan.io/api"
        self.GITHUB_API_BASE_URL = "https://api.github.com"
        self.wallet_tags = {}  # { "address": ["tag1", "tag2"] }

    def discover_wallets(self, target_domain: str) -> List[Dict]:
        """Discovers crypto wallets associated with a domain."""
        wallets = []
        
        # Method 1: Website source
        try:
            response = requests.get(f'https://{target_domain}')
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Could not fetch {target_domain}: {e}")
            return wallets

    def analyze_wallet(self, wallet_address: str, blockchain: str) -> Dict:
        """Analyzes a single crypto wallet to get balance and transaction history."""
        analysis = {
            "address": wallet_address,
            "blockchain": blockchain,
            "balance": 0,
            "transactions": [],
            "error": None
        }

        if blockchain == 'Ethereum':
            try:
                analysis.update(self._analyze_ethereum_wallet(wallet_address))
            except requests.exceptions.RequestException as e:
                analysis["error"] = f"Could not analyze Ethereum wallet: {e}"

        elif blockchain == 'Bitcoin':
            # Placeholder for Bitcoin analysis using self.btc_explorer_api
            analysis["error"] = "Bitcoin analysis not yet implemented."
        
        # Placeholder for more advanced analysis
        # - Identify common counterparties (other wallets)
        # - Identify interactions with smart contracts (e.g., DeFi, NFTs)

        return analysis

    def tag_wallet(self, wallet_address: str, tag: str):
        """Adds a tag to a wallet address."""
        if wallet_address not in self.wallet_tags:
            self.wallet_tags[wallet_address] = []
        if tag not in self.wallet_tags[wallet_address]:
            self.wallet_tags[wallet_address].append(tag)

    def map_payment_flows(self, transactions: List[Dict]) -> Dict:
        """Maps payment flows between wallets based on transactions."""
        flow_graph = {}
        for tx in transactions:
            from_addr = tx.get('from')
            to_addr = tx.get('to')
            if from_addr and to_addr:
                if from_addr not in flow_graph:
                    flow_graph[from_addr] = []
                flow_graph[from_addr].append(to_addr)
        return flow_graph
        
        # Bitcoin addresses (regex)
        btc_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
        btc_addresses = re.findall(r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}', source_code)
        for addr in btc_addresses:
            findings.append(Finding(
                value=addr,
                type=FindingType.CRYPTO_WALLET,
                source_module="crypto_intelligence",
                target=target_domain,
                confidence=0.8,
                metadata={"blockchain": "Bitcoin", "source": "website_source"}
            ))

        eth_addresses = re.findall(r'0x[a-fA-F0-9]{40}', source_code)
        for addr in eth_addresses:
            findings.append(Finding(
                value=addr,
                type=FindingType.CRYPTO_WALLET,
                source_module="crypto_intelligence",
                target=target_domain,
                confidence=0.8,
                metadata={"blockchain": "Ethereum", "source": "website_source"}
            ))

        # Method 3: Search GitHub
        if self.github_token:
            headers = {"Authorization": f"token {self.github_token}"}
            query = f'"{target_domain}" AND ("0x" OR "bitcoin") in:file'
            params = {"q": query, "per_page": 100}
            try:
                response = requests.get(f"{self.GITHUB_API_BASE_URL}/search/code", headers=headers, params=params)
                response.raise_for_status()
                search_results = response.json()

                if 'items' in search_results:
                    for item in search_results['items']:
                        # Further analysis of the code snippet can be done here
                        # For now, just report the file
                        findings.append(Finding(
                            value=item['html_url'],
                            type=FindingType.CRYPTO_WALLET,
                            source_module="crypto_intelligence",
                            target=item['repository']['html_url'],
                            confidence=0.6,
                            metadata={"blockchain": "Unknown", "source": "github_code"}
                        ))
            except requests.exceptions.RequestException as e:
                print(f"Could not search GitHub: {e}")
        
        return findings

    def analyze_wallet(self, address: str, blockchain: str) -> Dict:
        """
        Deep analysis of a cryptocurrency wallet
        """
        if blockchain == 'Ethereum':
            return self._analyze_ethereum_wallet(address)
        elif blockchain == 'Bitcoin':
            # Placeholder for Bitcoin analysis
            return self._analyze_bitcoin_wallet(address)
        return {}

    def _analyze_ethereum_wallet(self, address: str) -> Dict:
        """ 
        Analyze Ethereum wallet using Etherscan API V2.
        """
        if not self.etherscan_api:
            print("Etherscan API key not configured.")
            return {}

        # Get balance
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest",
            "apikey": self.etherscan_api
        }
        try:
            balance_resp = requests.get(self.ETHERSCAN_API_BASE_URL, params=params).json()
            if balance_resp.get("status") != "1":
                print(f"Etherscan API Error: {balance_resp.get('message')}")
                return {}
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error fetching balance from Etherscan: {e}")
            return {}
        
        balance_wei = int(balance_resp['result'])
        balance_eth = balance_wei / 10**18
        
        # Get transaction history
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "apikey": self.etherscan_api
        }
        try:
            tx_resp = requests.get(self.ETHERSCAN_API_BASE_URL, params=params).json()
            if tx_resp.get("status") != "1":
                print(f"Etherscan API Error: {tx_resp.get('message')}")
                transactions = []
            else:
                transactions = tx_resp['result']
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error fetching transactions from Etherscan: {e}")
            transactions = []
        
        # Analyze patterns
        incoming_addrs = set()
        outgoing_addrs = set()
        total_received = 0
        total_sent = 0
        
        for tx in transactions:
            if tx['to'].lower() == address.lower():
                incoming_addrs.add(tx['from'])
                total_received += int(tx['value']) / 10**18
            else:
                outgoing_addrs.add(tx['to'])
                total_sent += int(tx['value']) / 10**18
        
        tags = self._check_wallet_tags(address, 'Ethereum')
        
        return {
            'address': address,
            'blockchain': 'Ethereum',
            'balance_eth': balance_eth,
            'transaction_count': len(transactions),
            'unique_senders': len(incoming_addrs),
            'unique_receivers': len(outgoing_addrs),
            'total_received': total_received,
            'total_sent': total_sent,
            'tags': tags
        }

    def _analyze_bitcoin_wallet(self, address: str) -> Dict:
        print("Bitcoin analysis not yet implemented.")
        return {}

    def _check_wallet_tags(self, address: str, blockchain: str) -> List[str]:
        print("Wallet tag checking not yet implemented.")
        return []

    def map_payment_flows(self, wallet: str) -> Dict:
        print("Payment flow mapping not yet implemented.")
        return {}
