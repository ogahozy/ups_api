# ups_auth.py
import os
import requests
import time

# UPS OAuth 2.0 credentials
#client_id = '5p6is4iJrn7Z9HATpEPAGBjSkQu4IVjfVIMrX1Qf6qI'
#client_secret ='4koSWw82tj7SLGr5T8PM3lh2pqI3KGQSJ6LByQhJzJT3NhnAQ4qFK'
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')

# UPS OAuth 2.0 token endpoint
TOKEN_URL = 'https://onlinetools.ups.com/security/v1/oauth/token'
#TOKEN_URL = 'https://wwwcie.ups.com/security/v1/oauth/token'

# Global cache for token
ups_token = {"access_token": None, "expires_at": 0}


def get_ups_access_token():
    """
    Fetch and cache UPS access token. Requests a new token only when expired.
    """
    current_time = time.time()

    # If token exists and is still valid, reuse it
    if ups_token["access_token"] and current_time < ups_token["expires_at"]:
        return ups_token["access_token"]

    # Request new token
    payload = {'grant_type': 'client_credentials'}
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "x-merchant-id": "7971Y1"}

    response = requests.post(TOKEN_URL, data=payload, headers=headers, auth=(client_id, client_secret))

    if response.status_code == 200:
        data = response.json()
        ups_token["access_token"] = data.get('access_token')
        ups_token["expires_at"] = current_time + int(data.get('expires_in', 14400))  # Default: 4 hours

        return ups_token["access_token"]
    else:
        print("Failed to fetch access token:", response.text)
        return None
