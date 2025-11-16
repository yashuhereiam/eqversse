"""
Quick test script to validate backend API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_backend():
    print("Testing Backend API...")
    
    # Test data
    test_data = {
        "childName": "Alex",
        "emotion": "Happy",
        "inattentiveness": "low",
        "hyperactivity": "low",
        "impulsiveness": "low"
    }
    
    # Test 1: Start story
    print("\n1. Testing /start_story...")
    try:
        response = requests.post(f"{BASE_URL}/start_story", json=test_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"   ✓ Story started. Session ID: {session_id}")
        else:
            print(f"   ✗ Failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print("   Make sure backend is running: python backend_api.py")
        return
    
    # Test 2: Get first episode
    print("\n2. Testing /get_episode...")
    try:
        response = requests.get(f"{BASE_URL}/get_episode?session_id={session_id}", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Episode {data.get('episode')}: {data.get('title')}")
            print(f"   Story: {data.get('story')[:50]}...")
            print(f"   Choices: {len(data.get('choices', []))} options")
        else:
            print(f"   ✗ Failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 3: Make a choice
    print("\n3. Testing /make_choice...")
    try:
        response = requests.post(f"{BASE_URL}/make_choice", 
                                json={"session_id": session_id, "choice_index": 0}, 
                                timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Choice made. XP: {data.get('xp')}")
        else:
            print(f"   ✗ Failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    print("\n✓ All backend tests passed!")
    print("\nNow test the frontend:")
    print("1. Run: cd frontend && npm start")
    print("2. Open http://localhost:3000")
    print("3. Fill out the form and start a story")

if __name__ == "__main__":
    test_backend()
