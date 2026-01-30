"""
Test Script: API Key Valid Hai Ya Nahi?
Ye script check karega ki aapka OpenWeatherMap API key kaam kar raha hai
"""
import requests

# Aapka current API key
API_KEY = "6b1edcf5240c69d1d1f63b17130896a7"

# Test location: Lucknow, Uttar Pradesh
LAT = 26.8467
LON = 80.9462

print("=" * 60)
print("🔍 Testing OpenWeatherMap API Key...")
print("=" * 60)

try:
    # API call
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': LAT,
        'lon': LON,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    print(f"\n📡 Sending request to OpenWeatherMap...")
    print(f"   Location: Lucknow, UP ({LAT}, {LON})")
    
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n✅ SUCCESS! API Key is VALID and WORKING!\n")
        print("=" * 60)
        print("📊 Current Weather Data:")
        print("=" * 60)
        print(f"🌡️  Temperature: {data['main']['temp']}°C")
        print(f"💧 Humidity: {data['main']['humidity']}%")
        print(f"☁️  Weather: {data['weather'][0]['description']}")
        
        if 'rain' in data:
            rainfall = data['rain'].get('1h', 0) + data['rain'].get('3h', 0)
            print(f"🌧️  Rainfall: {rainfall} mm")
        else:
            print(f"🌧️  Rainfall: 0 mm (No rain)")
        
        print("\n✅ Aapka API key bilkul sahi kaam kar raha hai!")
        print("   Koi change karne ki zarurat NAHI hai.")
        
    elif response.status_code == 401:
        print("\n❌ ERROR: API Key INVALID hai!")
        print("   Kripya naya API key generate karein:")
        print("   https://openweathermap.org/api")
        
    elif response.status_code == 429:
        print("\n⚠️  WARNING: API Limit exceed ho gayi!")
        print("   Free plan: 1000 calls/day")
        print("   Thodi der baad try karein.")
        
    else:
        print(f"\n❌ ERROR: Status code {response.status_code}")
        print(f"   Response: {response.text}")

except requests.exceptions.Timeout:
    print("\n⚠️  Timeout: Server respond nahi kar raha.")
    print("   Internet connection check karein.")
    
except requests.exceptions.ConnectionError:
    print("\n⚠️  Connection Error: Internet nahi hai!")
    print("   WiFi/Network check karein.")
    
except Exception as e:
    print(f"\n❌ Unexpected Error: {e}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
