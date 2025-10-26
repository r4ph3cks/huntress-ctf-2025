import requests

params = {
    "client_id": "YOUR_CLIENT_ID",
    "response_type": "code",
    "redirect_uri": "https://localhost/callback",
    "scope": "openid profile email",
    "state": "12345",
    "nonce": "67890"
}

url = "https://login.microsoftonline.com/4rhdc6.onmicrosoft.com/oauth2/v2.0/authorize"
response = requests.get(url, params=params)

print(response.url)  # Shows full URL with parameters
print(response.status_code)
print(response.text)  # Print the response content