import urllib.request
import re

def check_agrobank():
    url = "https://agrobank.uz/uz/person/exchange_rates"
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
            print("Successfully fetched page.")
            
            # Check for dollar sign or typical rate structure
            title_match = re.search(r'<title>(.*?)</title>', html)
            print(f"Title: {title_match.group(1) if title_match else 'No Title'}")
            
            # Check for USD mentions
            if "USD" in html:
                print("Found 'USD' in HTML.")
            else:
                print("'USD' NOT found in HTML.")
                
            # Check for numbers that look like rates (e.g., 12000)
            rates = re.findall(r'\d{5}', html)
            if rates:
                print(f"Found potential rates: {rates[:5]}")
            else:
                print("No obvious rates found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_agrobank()
