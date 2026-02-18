import requests
import json

URL = "https://jvlziovytepaojbzkjyp.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp2bHppb3Z5dGVwYW9qYnpranlwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgzMjkwNTEsImV4cCI6MjA4MzkwNTA1MX0.6mUmMH4JB5zBbJit0TCjK3jaNu2iwZyvDCEHY1gMtf0"

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}

# Common table names in Supabase/Postgres apps
candidates = [
    "users", "profiles", "accounts", "public_users",
    "posts", "comments", "replies", "likes", "reactions",
    "follows", "followers", "relationships",
    "messages", "direct_messages", "chats", "chat_rooms", "conversations",
    "notifications", "activities", "events",
    "transactions", "orders", "payments", "wallets", "balances",
    "products", "items", "inventory",
    "settings", "config", "app_config",
    "audit_logs", "logs", "errors",
    "reports", "feedback", "support_tickets",
    "banned_users", "blocked_users",
    "roles", "permissions", "admin"
]

print(f"[*] Probing {len(candidates)} potential tables on {URL}...")

found_tables = []

for table in candidates:
    url = f"{URL}/rest/v1/{table}?select=*&limit=1"
    try:
        # Use HEAD to check existence, or GET with limit 1
        resp = requests.get(url, headers=headers)
        
        if resp.status_code == 200:
            print(f"  [+] FOUND: '{table}' (200 OK)")
            found_tables.append(table)
            # Try to see if it has data
            data = resp.json()
            if data:
                print(f"      -> Contains data! Sample keys: {list(data[0].keys())}")
            else:
                print(f"      -> Empty.")
        elif resp.status_code == 401:
            print(f"  [!] LOCKED: '{table}' (401 Unauthorized - RLS likely)")
            # Even if locked, it exists!
            found_tables.append(f"{table} (LOCKED)")
        # 404 means table doesn't exist (usually)
        
    except Exception as e:
        print(f"  [!] Error probing {table}: {e}")

print("\n[*] Discovery Complete.")
print(f"[*] Tables identified: {found_tables}")
