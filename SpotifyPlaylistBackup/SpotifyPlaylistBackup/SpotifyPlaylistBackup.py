import requests
import base64

## This is to get your access code
# Your client ID and client secret
client_id = 'XXXXX'
client_secret = 'XXXXX'

# Encode the client ID and client secret
auth_str = f"{client_id}:{client_secret}"
b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()

# Set up the request headers
headers = {
    "Authorization": f"Basic {b64_auth_str}"
}

# Set up the request body
data = {
    "grant_type": "client_credentials"
}

# Make the POST request to the token endpoint
response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']
    print(f"Access Token: {access_token}")
else:
    print(f"Failed to get access token: {response.status_code}")
    print(response.json())
