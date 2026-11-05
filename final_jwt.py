import requests

# Your OAuth data from direct_token.py
open_id = "d73bd4bbd0fe5c21e45690991a88d069"
access_token = "5d903cf05bb621a8edfa87a4e32b5c8db8c0756f4a1d946ebe0e72f48866dfb5"

# Garena's active MajorLogin servers
domains = [
    "https://loginbp.ggblueshark.com/MajorLogin",
    "https://loginbp.ggpolarbear.com/MajorLogin",
    "https://loginbp.ggdarkwolf.com/MajorLogin",
    "https://loginbp.ggwhitehawk.com/MajorLogin"
]

payload = {
    "open_id": open_id,
    "access_token": access_token,
    "platform": "2" # Android
}
headers = {
    "User-Agent": "GarenaMSDK/4.0.19P10(I2404 ;Android 15;en;US;)",
    "Content-Type": "application/x-www-form-urlencoded"
}

print("Searching for an active Garena server...")

for url in domains:
    print(f"Trying {url}...")
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            jwt = data.get("token")
            if jwt:
                print(f"\n✅ SUCCESS! Found on {url}")
                print("\nHERE IS YOUR REAL JWT:\n")
                print(jwt)
                break
    except Exception:
        print(f"❌ Failed to connect to {url}")

else:
    print("\nAll domains failed. Garena might have updated them again.")
