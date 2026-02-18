import requests
import re
from colorama import Fore, init

init(autoreset=True)

URL = "https://abs.twimg.com/responsive-web/client-web/main.1ab552da.js"

def analyze_bundle():
    print(f"{Fore.CYAN}[*] Downloading JS Bundle: {URL}")
    r = requests.get(URL)
    content = r.text
    
    print(f"{Fore.GREEN}[+] Downloaded {len(content)} bytes")
    
    # 1. Search for 'add_response' context
    print(f"{Fore.YELLOW}[*] Searching for 'add_response' context...")
    matches = re.finditer(r".{0,100}add_response.{0,100}", content)
    for m in matches:
        print(f"    MATCH: {m.group(0)}")

    # 2. Search for 'grok-transaction' context
    print(f"{Fore.YELLOW}[*] Searching for 'grok-transaction' context...")
    matches = re.finditer(r".{0,100}grok-transaction.{0,100}", content)
    for m in matches:
        print(f"    MATCH: {m.group(0)}")
        
    # 3. Search for GraphQL Query IDs (Twitter uses long hashes)
    # They look like: queryId:"MaybeAHash",operationName:"Grok..."
    print(f"{Fore.YELLOW}[*] Searching for GraphQL Definitions...")
    # Regex to find object definitions with operationName and queryId
    # e.g., {queryId:"xxx",operationName:"xxx",operationType:"mutation"}
    
    # Simplified regex to catch json-like structures with operationName
    regex = r'\{queryId:"[a-zA-Z0-9]+",operationName:"[a-zA-Z0-9_]+"'
    matches = re.finditer(regex, content)
    for m in matches:
        val = m.group(0)
        if "Grok" in val or "Conversation" in val or "Message" in val or "AI" in val:
            print(f"    GQL_TARGET: {val}")

if __name__ == "__main__":
    analyze_bundle()
