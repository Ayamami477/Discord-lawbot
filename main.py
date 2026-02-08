import os
import asyncio
import httpx
import requests
import unicodedata
from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from contextlib import asynccontextmanager
import uvicorn

# --- 設定 ---
APPLICATION_ID = os.getenv("APPLICATION_ID")
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
BASE_URL = " https://laws.e-gov.go.jp/api/2"

async def get_lawdata(law_id,article_num):
    params = {'title': 'lawtitle', 'id': 'law_revision_id'}
    
async with httpx.AsyncClient() as client:
        r = await client.get(BASE_URL)
        data = r.json()
        law_name = data.law_title
        law_id   = data.law_revision_id
        httpx.AsyncClient(timeout=10.0)
LAW_MASTER = {
    "労働基準法": "",
    "労働契約法": "",
    "消費者契約法": ""
}

for law_name, law_id in LAW_MASTER.items():
   print(f"法律名:{law_name},法律id:{law_id}")

# --- 1. 署名検証用の関数 (Discordからの通信であることを証明する) ---
def verify_signature(body: bytes, signature: str, timestamp: str):
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    try:
        # timestamp + body の組み合わせを公開鍵でチェック
        verify_key.verify(f"{timestamp}{body.decode()}".encode(), bytes.fromhex(signature))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid request signature")

app = FastAPI()

@app.post("/interactions")
async def interactions(request: Request):
    # 2. Discordからのヘッダーを取得
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = await request.body()

    # 3. 署名が正しいか検証 (これがないとDiscordに拒絶される)
    verify_signature(body, signature, timestamp)

    data = await request.json()

    # 4. PINGへの応答 (Discord設定画面での「URL確認」用)
    if data.get("type") == 1:
        return {"type": 1}

    # 5. スラッシュコマンド (Type 2) の処理 (仮)
    if data.get("type") == 2:
        # ここで後で LAW_MASTER を使って API を叩く
        return {
            "type": 4, # 即レスポンス
            "data": {
                "content": "コマンドを受け付けました！現在、法律データを取得する準備をしています..."
            }
        }

if __name__ == "__main__":
    uvicorn.run(app,"0.0.0.0",port=8080)