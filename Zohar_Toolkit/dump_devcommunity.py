import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = "https://devcommunity.x.com/admin/plugins/explorer/queries/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

resp = requests.get(url, headers=headers, verify=False)
with open("devcommunity_response.html", "w", encoding="utf-8") as f:
    f.write(resp.text)

print(f"Saved response to devcommunity_response.html. Length: {len(resp.text)}")
