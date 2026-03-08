import requests

url = "https://api-finflux.onrender.com/usuarios"

response = requests.get(url)
print(response.status_code)
print(response.json())