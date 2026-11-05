from fastapi import FastAPI
import requests

app = FastAPI()

# Get a fresh token from the Render API we used earlier
TOKEN_API = "https://jwt-gen-api-lwte.onrender.com/token?uid=8410458689&password=wer_HSZK_JIDDI_I63U"

@app.get("/api/player/{uid}")
async def get_player(uid: str):
    try:
        # 1. Get the token automatically
        token_res = requests.get(TOKEN_API)
        if token_res.status_code != 200:
            return {"error": "Failed to get token from API"}
        
        token_data = token_res.json()
        jwt = token_data.get("token")
        server_url = "https://client.ind.freefiremobile.com"

        # 2. Use a public Info API to get the player data
        # (This API automatically handles the protobuf decryption for you)
        info_url = f"https://ff-info-api-v2.vercel.app/info?uid={uid}&region=ind&token={jwt}"
        
        info_res = requests.get(info_url)
        
        if info_res.status_code == 200:
            return info_res.json()
        else:
            return {"error": "Failed to fetch player info", "details": info_res.text}
            
    except Exception as e:
        return {"error": str(e)}