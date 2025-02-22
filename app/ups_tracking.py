# ups_tracking.py
import requests
import uuid
import json
from app.ups_auth import get_ups_access_token

def track_ups_parcel(tracking_number):
    """
    Fetch tracking details using the UPS API.
    """
    access_token = get_ups_access_token()
    if not access_token:
        return {"error": "Failed to get UPS access token"}

    tracking_url = f"https://onlinetools.ups.com/api/track/v1/details/{tracking_number}"
    #tracking_url = f"https://wwwcie.ups.com/track/v1/details/{tracking_number}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'transId': str(uuid.uuid4()),  # Unique transaction ID
        'transactionSrc': 'ejusglobal',  # Application source name
        'Content-Type': 'application/json'
    }

    response = requests.get(tracking_url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        # return response.json()
        return data #response.json()
    else:
        return {"error": f"Tracking failed: {response.status_code}", "details": response.text}
