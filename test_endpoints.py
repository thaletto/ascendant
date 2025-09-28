"""
Simple test script to verify Horoscope AI Backend endpoints.
Run this after starting the server with: python run.py
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint."""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_user():
    """Test user creation."""
    print("Testing user creation...")
    user_data = {
        "name": "Test User",
        "birth_date": "1990-05-15T00:00:00",
        "birth_time": "14:30",
        "birth_place": "New York, NY"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        user = response.json()
        print(f"Created user: {user}")
        return user["id"]
    else:
        print(f"Error: {response.text}")
        return None

def test_get_user(user_id):
    """Test getting user."""
    print(f"Testing get user {user_id}...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_prediction(user_id):
    """Test prediction creation."""
    print(f"Testing prediction creation for user {user_id}...")
    prediction_data = {
        "user_id": user_id,
        "prediction_type": "daily"
    }
    response = requests.post(f"{BASE_URL}/predict/", json=prediction_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        prediction = response.json()
        print(f"Created prediction: {prediction}")
        return prediction["id"]
    else:
        print(f"Error: {response.text}")
        return None

def test_chat_stream(user_id):
    """Test chat streaming."""
    print(f"Testing chat stream for user {user_id}...")
    chat_data = {
        "user_id": user_id,
        "message": "Tell me about my sun sign"
    }
    response = requests.post(f"{BASE_URL}/chat/stream", json=chat_data, stream=True)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Streaming response:")
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))
    else:
        print(f"Error: {response.text}")
    print()

def main():
    """Run all tests."""
    print("🚀 Testing Horoscope AI Backend Endpoints")
    print("=" * 50)
    
    # Test basic endpoints
    test_root()
    test_health()
    
    # Test user management
    user_id = test_create_user()
    if user_id:
        test_get_user(user_id)
        
        # Test predictions (may fail without OpenAI API key)
        prediction_id = test_create_prediction(user_id)
        
        # Test chat (may fail without OpenAI API key)
        test_chat_stream(user_id)
    
    print("✅ Tests completed!")

if __name__ == "__main__":
    main()
