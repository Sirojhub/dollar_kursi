import requests

def test_cbu():
    urls = [
        "https://cbu.uz/oz/arkhiv-kurs-valyut/json",  # No trailing slash
        "https://cbu.uz/oz/arkhiv-kurs-valyut/json/", # With trailing slash
        "https://cbu.uz/uz/arkhiv-kurs-valyut/json",
        "https://cbu.uz/ru/arkhiv-kurs-valyut/json"
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
                print(f"Content-Type: {response.headers.get('Content-Type')}")
                try:
                    data = response.json()
                    print(f"Items: {len(data)}")
                    break
                except:
                    print("Not JSON!")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_cbu()
