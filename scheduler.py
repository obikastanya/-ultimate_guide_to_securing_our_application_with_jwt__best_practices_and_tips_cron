
import os
import time
import traceback

import schedule
import requests

CRON_USER = os.getenv("CRON_USER")
CRON_PASSWORD = os.getenv("CRON_PASSWORD")
        

def remove_revoked_token_thats_already_expired():
    try:
        TARGET ='http://127.0.0.1:8080'
        
        request_session = requests.session()
        request_session.auth =(CRON_USER, CRON_PASSWORD)

        login_response = request_session.post(f'{TARGET}/login')
        if login_response.status_code != 200:
            raise Exception("Credential error")
        
        data = login_response.json()
        access_token = data.get("access_token")

        request_headers = {
            "Authorization":f"Bearer {access_token}"
        }

        remove_token_response = requests.delete(f'{TARGET}/token/revoked/clear', headers=request_headers)
        if remove_token_response.status_code != 200:
            raise Exception("Failed to remove tokens")
        print("Expired token has been removed...")
    except:
        traceback.print_exc()

schedule.every(1).minutes.do(remove_revoked_token_thats_already_expired)

while True:
    schedule.run_pending()
    time.sleep(1)
