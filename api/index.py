from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

# Import protobuf handlers from the 0xMe/FreeFire-Api project
from api.Proto.main_pb2 import GetPlayerPersonalShow
from api.Proto.AccountPersonalShow_pb2 import AccountPersonalShowInfo
from api.Utilities.until import encrypt_payload, decrypt_payload

app = FastAPI()

# You must generate a valid JWT using a guest account first.
# See: https://github.com/0xMe/FreeFire-Api/blob/main/Api/Account.py
ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInN2ciI6IjMiLCJ0eXAiOiJKV1QifQ.eyJhY2NvdW50X2lkIjoxOTAyMzc3NzE1OCwibmlja25hbWUiOiJSZ0JIMnJpSWdlTFMrdDJrM1lhNGh3PT0iLCJub3RpX3JlZ2lvbiI6IklORCIsImxvY2tfcmVnaW9uIjoiSU5EIiwiZXh0ZXJuYWxfaWQiOiJkNzNiZDRiYmQwZmU1YzIxZTQ1NjkwOTkxYTg4ZDA2OSIsImV4dGVybmFsX3R5cGUiOjQsInBsYXRfaWQiOjAsImNsaWVudF92ZXJzaW9uIjoiIiwiY2xpZW50X3ZlcnNpb25fY29kZSI6IiIsImVtdWxhdG9yX3Njb3JlIjoxMDAsImlzX2VtdWxhdG9yIjp0cnVlLCJjb3VudHJ5X2NvZGUiOiJVUyIsImV4dGVybmFsX3VpZCI6ODQxMDQ1ODY4OSwicmVnX2F2YXRhciI6MTAyMDAwMDA3LCJzb3VyY2UiOjAsImxvY2tfcmVnaW9uX3RpbWUiOjE3OTM4NTgwODAsImNsaWVudF90eXBlIjoxLCJzaWduYXR1cmVfbWQ1IjoiIiwidXNpbmdfdmVyc2lvbiI6MCwicmVsZWFzZV9jaGFubmVsIjoiIiwicmVsZWFzZV92ZXJzaW9uIjoiT0I1NSIsImV4cCI6MTc5MzkxODQxN30.gHlK9PXiBYEHwtpu6x-peiR40dSqHwUk318RFH6DWn8"
@app.get("/api/player/{uid}")
async def get_player(uid: str, server: str = "IND"):
    try:
        # 1. Build the protobuf request
        req = GetPlayerPersonalShow()
        req.a = int(uid)
        req.b = 0
        
        # 2. Encrypt and send to Garena's internal API
        encrypted_data = encrypt_payload(req.SerializeToString())
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/octet-stream",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-G973F Build/RP1A.200720.012)"
        }
        
        # Garena endpoint for personal show data
        url = f"https://client.{server.lower()}.freefiremobile.com/GetPlayerPersonalShow"
        response = requests.post(url, headers=headers, data=encrypted_data)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Garena API error")
            
        # 3. Decrypt and parse the response
        decrypted = decrypt_payload(response.content)
        info = AccountPersonalShowInfo()
        info.ParseFromString(decrypted)
        
        # 4. Return structured JSON for the bot
        return {
            "basic": {
                "name": info.basic_info.nickname,
                "uid": uid,
                "level": info.basic_info.level,
                "exp": info.basic_info.exp,
                "region": info.basic_info.region,
                "likes": info.basic_info.likes,
                "title": info.basic_info.title,
                "signature": info.basic_info.signature
            },
            "activity": {
                "gender": info.social_info.gender,
                "br_rank": info.basic_info.br_rank,
                "cs_rank": info.basic_info.cs_rank,
                "created_at": info.basic_info.created_at,
                "last_login": info.basic_info.last_login
            },
            "guild": {
                "id": info.clan_info.clan_id,
                "name": info.clan_info.clan_name,
                "level": info.clan_info.clan_level,
                "members": f"{info.clan_info.live_members}/{info.clan_info.max_members}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))