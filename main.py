import os
import requests
from typing import Any

APPLICATION_ID = os.getenv("APPLICATION_ID")
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
BASE_URL = "https://laws.e-gov.go.jp/api/2"


response = requests.get(f"{BASE_URL}/laws")

laws_list: list[dict[str, Any]] = []
law_dict: dict[str, dict[str, str]] = {}

try:
  if response.status_code == 200:
    laws_data = response.json()
    laws_list: list[dict[str, Any]] = laws_data.get("laws", [])
  else:
      laws_list = []
except requests.exceptions.RequestException as e:
    print(f"Error fetching laws data: {e}")
    laws_list = []

LAW_MASTER = {
    "労働基準法": "",
    "労働契約法": "",
    "消費者契約法": ""
}

def get_law_data(law_id:str, law_name:str) -> dict[str, str]:
    return  {
        "law_id":law_id, 
        "law_name": law_name
    }
    
for law in laws_list:
    law_name = law.get("current_Revision", {}).get("law_title")
    law_id = law.get("law_info",{}).get("law_id")
    if law_name in LAW_MASTER:
        law_dict[law_name] = get_law_data(law_id, law_name)
    print(f"Available laws: {list(law_dict.keys())}")   



