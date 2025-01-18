import requests

BASE_URL = "http://127.0.0.1:5000"


def test_register():
    print("Testing Register...")
    payload = {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "SecurePassword123",
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/register", json=payload, headers=headers)

    # Mostrar la respuesta para depuración
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

    # Intentar decodificar la respuesta JSON
    try:
        response_json = response.json()
        if not response_json:
            print("Response JSON is None or invalid.")
            return None
    except ValueError:
        print("Error decoding JSON.")
        return None

    # Verificar que la respuesta tenga el código de estado correcto (201)
    if response.status_code == 201:
        # Verificar que los campos "email" y "name" estén presentes en la respuesta
        assert response_json.get("email") == payload["email"], "Email doesn't match"
        assert response_json.get("name") == payload["name"], "Name doesn't match"

        # Verificar si el campo "id" está presente
        if response_json and "id" not in response_json:
            print("Warning: 'id' is not returned in the response")
        else:
            print(f"User created with id: {response_json['id']}")

        print("Register Test Passed!")
    else:
        print("Register Test Failed!")

    return response_json


def test_login():
    print("Testing Login...")
    payload = {"email": "testuser@example.com", "password": "SecurePassword123"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/login", json=payload, headers=headers)

    # Mostrar la respuesta para depuración
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())

    return response


if __name__ == "__main__":
    print("Running Authentication Tests...")

    # Realizar el test de registro
    register_response = test_register()

    # Si el registro fue exitoso, proceder con el test de login
    if register_response and register_response.get("email") == "testuser@example.com":
        login_response = test_login()
        if login_response.status_code == 200:
            print("Authentication Test Passed!")
        else:
            print("Login Test Failed!")
    else:
        print("Register Test Failed!")
