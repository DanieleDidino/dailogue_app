import requests
from uuid import UUID, uuid4

# Heroku app URL
url = "https://dailogue-app-fff9453c6e01.herokuapp.com/"

# Heroku app URL for methods (POST, GET, etc.)
url_mgs = "https://dailogue-app-fff9453c6e01.herokuapp.com/api/messages/"


def test_heroku_service():
    # url = "https://dailogue-app-fff9453c6e01.herokuapp.com/"

    expected_status_code = 200
    expected_content = '{"message":"Welcome to Dailogy API"}'
    
    response = requests.get(url)
    
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"
    assert expected_content in response.text, "Expected content not found in response"


def test_heroku_transform_message():
    # url = "https://dailogue-app-fff9453c6e01.herokuapp.com/api/messages/"

    expected_status_code = 200
    expected_message = "First message"

    response = requests.post(url_mgs, json={"original_text": expected_message})

    data = response.json()
    
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"
    assert data["original_text"] == expected_message,  "Got unexpected 'original_test'"
    assert UUID(data["id"])  # Check if id is a valid UUID, "GOt unvalid ID"
    assert isinstance(data["original_text"], str), "unexpected type, 'original_test' must be a string"
    assert isinstance(data["prompt"], str), "unexpected type, 'prompt' must be a string"
    assert isinstance(data["transformed_text"], str), "unexpected type, 'transformed_text' must be a string"
