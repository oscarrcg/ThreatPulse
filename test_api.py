import requests
import config

url = "https://api.abuseipdb.com/api/v2/check"
headers = {
    "Key": config.ABUSEIPDB_KEY,
    "Accept": "application/json"
}
params = {
    "ipAddress": "45.155.205.233",
    "maxAgeInDays": 90
}

response = requests.get(url, headers=headers, params=params)
print("Status code:", response.status_code)
print("Respuesta completa:")
print(response.text)