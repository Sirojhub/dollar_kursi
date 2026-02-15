import requests

def test_nbu():
    url = "https://nbu.uz/en/exchange-rates/json/"
    print(f"Testing {url}...")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Items: {len(data)}")
            for item in data:
                if item.get('code') == 'USD':
                    print(f"USD Buy: {item.get('nbu_buy_price')}, Sell: {item.get('nbu_cell_price')}, CB: {item.get('cb_price')}")
                    break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_nbu()
