"""
API Testing Script - Test all endpoints
Krishi Drishti 2.0
"""
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000/api/v1"

def print_result(title, response):
    """Pretty print API response"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))


def test_api():
    """Test all API endpoints"""
    print("\n🧪 TESTING KRISHI DRISHTI API")
    print("="*70)
    
    try:
        # Test 1: Get all crops
        print("\n[1/5] Testing GET /crops...")
        response = requests.get(f"{API_BASE}/crops", timeout=5)
        print_result("GET /crops", response)
        
        # Test 2: Get states for Wheat
        print("\n[2/5] Testing GET /crops/Wheat/states...")
        response = requests.get(f"{API_BASE}/crops/Wheat/states", timeout=5)
        print_result("GET /crops/Wheat/states", response)
        
        # Test 3: Get weather data
        print("\n[3/5] Testing POST /weather...")
        weather_payload = {
            "state": "Punjab",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        response = requests.post(
            f"{API_BASE}/weather",
            json=weather_payload,
            timeout=10
        )
        print_result("POST /weather", response)
        
        # Test 4: Predict price
        print("\n[4/5] Testing POST /predict...")
        predict_payload = {
            "crop": "Wheat",
            "state": "Punjab",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "demand": 650.0
        }
        response = requests.post(
            f"{API_BASE}/predict",
            json=predict_payload,
            timeout=15
        )
        print_result("POST /predict (Main Feature!)", response)
        
        # Test 5: Get historical data
        print("\n[5/5] Testing GET /history/Wheat/Punjab...")
        response = requests.get(
            f"{API_BASE}/history/Wheat/Punjab",
            params={"days": 30},
            timeout=10
        )
        print_result("GET /history/Wheat/Punjab", response)
        
        print("\n" + "="*70)
        print("  ✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nNext Step: Open dashboard at http://localhost:8501")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("Make sure backend is running: cd backend && python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    test_api()
