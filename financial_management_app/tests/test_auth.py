import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

test_pass = os.getenv("TEST_PASSWORD")
BASE_URL = os.getenv("BASE_URL")


def test_register():
    print("Testing Register...")
    payload = {
        "email": "testuser1@example.com",
        "name": "Test User 1",
        "password": test_pass,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(f"{BASE_URL}/register", json=payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during registration: {e}")
        return None

    try:
        response_json = response.json()
    except ValueError:
        print("Invalid JSON response.")
        return None

    if response.status_code == 201:
        assert (
            response_json.get("email") == payload["email"]
        ), f"Expected email {payload['email']}, got {response_json.get('email')}"
        assert (
            response_json.get("name") == payload["name"]
        ), f"Expected name {payload['name']}, got {response_json.get('name')}"
        if "id" in response_json:
            print(f"User created with ID: {response_json['id']}")
        else:
            print("Warning: 'id' is not returned in the response.")
        print("Register Test Passed!")
    else:
        print(f"Register Test Failed! Status Code: {response.status_code}")

    return response_json


def test_login():
    print("Testing Login...")
    payload = {"email": "testuser1@example.com", "password": test_pass}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(f"{BASE_URL}/login", json=payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during login: {e}")
        return None

    try:
        response_json = response.json()
    except ValueError:
        print("Invalid JSON response.")
        return None

    print("Login Test Passed!")
    return response_json


if __name__ == "__main__":
    print("Running Authentication Tests...")
    register_response = test_register()

    if register_response and register_response.get("email") == "testuser1@example.com":
        login_response = test_login()
        if login_response:
            print("Authentication Test Passed!")
        else:
            print("Login Test Failed!")
    else:
        print("Register Test Failed!")
