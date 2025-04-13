import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:5000"
USERNAME = "yapa920@gmail.com"
PASSWORD = "Alvin1234567"

def login():
    """Login to the system and get access token"""
    print("Logging in...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": USERNAME, "password": PASSWORD}
        )
        response.raise_for_status()
        print("Login successful!")
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"\nLogin failed: {e}")
        if hasattr(e.response, 'text'):
            print(f"Error details: {e.response.text}")
        return None

def get_all_records(token):
    """Get all flood records"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/history/all",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to get records: {e}")
        if hasattr(e.response, 'text'):
            print(f"Error details: {e.response.text}")
        return None

def print_record(record):
    """Format and print a single record"""
    print("\n" + "="*80)
    print(f"Date: {record['date']}")
    print(f"Location: Latitude {record['location']['latitude']}, Longitude {record['location']['longitude']}")
    print(f"Affected Areas: {record['affected_areas']}")
    if record['river_level']:
        print(f"Water Level: {record['river_level']} meters")
    if record['comments']:
        print(f"Comments: {record['comments']}")
    print("="*80)

def main():
    # Login and get token
    token = login()
    if not token:
        print("Could not get access token, exiting")
        return

    # Get all records
    records = get_all_records(token)
    if not records:
        print("Failed to retrieve records")
        return

    # Print records
    print(f"\nFound {len(records)} flood records:")
    for record in records:
        print_record(record)

if __name__ == "__main__":
    main() 