import requests

def test_apis():
    urls = [
        "https://cbu.uz/oz/arkhiv-kurs-valyut/json/all/",
        "https://nbu.uz/exchange-rates/json/",
        "https://api.exchangerate-api.com/v4/latest/USD" # Third party free API just to check connectivity
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for url in urls:
        print(f"Testing {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS!")
                print(response.text[:100])
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_apis()
