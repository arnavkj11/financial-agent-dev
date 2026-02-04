import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"
EMAIL = "arnav.jain@test.com"
PASSWORD = "password123"

def login():
    print(f"Logging in as {EMAIL}...")
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": EMAIL, "password": PASSWORD})
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("Login Successful!")
        return token
    else:
        print(f"Login Failed: {response.text}")
        sys.exit(1)

def test_dashboard(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n--- Testing Dashboard API (Default / 30d) ---")
    resp = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
    print_response(resp)

    print("\n--- Testing Dashboard API (Last 1 Year) ---")
    resp = requests.get(f"{BASE_URL}/dashboard/stats?time_range=1y", headers=headers)
    print_response(resp)

    print("\n--- Testing Dashboard API (Filtered: Food & Travel) ---")
    resp = requests.get(f"{BASE_URL}/dashboard/stats?categories=Food&categories=Travel", headers=headers)
    print_response(resp)

def print_response(resp):
    if resp.status_code == 200:
        data = resp.json()
        print(f"Status: {resp.status_code}")
        print(f"Total Spent: ${data['total_spent']}")
        print(f"Top Category: {data['top_category']}")
        print(f"Breakdown: {len(data['category_breakdown'])} categories")
        print(f"Trend Points: {len(data['monthly_trend'])} points")
    else:
        print(f"Error {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    token = login()
    test_dashboard(token)
