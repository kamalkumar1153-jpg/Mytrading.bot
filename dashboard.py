import requests
import os
import time
import json
from datetime import datetime

def update_github(nifty, sensex, time_now):
    try:
        data = {"nifty": nifty, "sensex": sensex, "time": time_now}
        with open('data.json', 'w') as f:
            json.dump(data, f)
        # GitHub Auto-Sync
        os.system("git add data.json && git commit -m 'Price Sync' && git push origin main > /dev/null 2>&1")
    except:
        pass

def main():
    # Token file se read karega
    if not os.path.exists('token.txt'):
        print("❌ Error: token.txt file nahi mili!")
        return
    
    with open('token.txt', 'r') as f:
        token = f.read().strip()
    
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
    instruments = 'NSE_INDEX|Nifty 50,BSE_INDEX|SENSEX'

    while True:
        try:
            url = f'https://api.upstox.com/v2/market-quote/ltp?instrument_key={instruments}'
            res = requests.get(url, headers=headers).json()
            
            if 'data' in res:
                nifty = res['data']['NSE_INDEX:Nifty 50']['last_price']
                sensex = res['data']['BSE_INDEX:SENSEX']['last_price']
                now = datetime.now().strftime('%H:%M:%S')

                print("\033[H\033[J")
                print("==============================================")
                print(f"      🚀  KAMAL PRO TERMINAL v52.0         ")
                print("==============================================")
                print(f"NIFTY 50  : ₹{nifty}")
                print(f"SENSEX    : ₹{sensex}")
                print("-" * 46)
                print(f"CLOUD SYNC: ✅ ACTIVE | {now}")
                print("==============================================")

                update_github(nifty, sensex, now)
            else:
                print("⚠️ Token Expired! Please update token.txt")

        except Exception as e:
            print(f"❌ Connection Error: {e}")
        
        time.sleep(60) # 1 minute wait

main()
