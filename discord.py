import requests
import configparser
from typing import List

def send_alert_new_times(times: List[dict], config: configparser.ConfigParser) -> None:
    message = 'New times dropped:\n' ### TODO add location
    for newtime in times:
        newline = f"""<t:{newtime["time"]}:f> with {newtime["instructor"]}"""
        message += newline

    data = {
        "content": message
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    webhook_url = config["passwd"]["discord_wh"]
    
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print("Failed to send message. Error code:", response.status_code)
