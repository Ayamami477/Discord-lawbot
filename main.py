import os
import requests

APPLICATION_ID = os.getenv("APPLICATION_ID")
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
BASE_URL = "https://laws.e-gov.go.jp/api/2"


response = requests.get(f"{BASE_URL}/laws")

if response.status_code == 200:
    data = response.json()
    
LAW_MASTER = {
    "労働基準法": "",
    "労働契約法": "",
    "消費者契約法": ""
}

#for law_name, law_id in LAW_MASTER.items():
    
law_dict ={}
def get_law_data(law_id:str, law_name:str) -> dict[str, str]:
    return  {
        "law_id":law_id, 
        "law_name": law_name
    }
    




