import json
import requests
import configparser
from typing import List

DISCORD_MESSAGE_LENGTH_LIMIT = 2000

def send_alert_new_times(times: List[dict], config: configparser.ConfigParser) -> None:
    message = 'New times dropped:\n' ### TODO add location
    for newtime in times:
        newline = f"""<t:{newtime["time"]}:f> with {newtime["instructor"]}\n"""
        if len(message) + len(newline) > DISCORD_MESSAGE_LENGTH_LIMIT: # message length overflow protection
            send_discord_message(message, config)
            message = ""
        message += newline
    send_discord_message(message, config)

def send_discord_message(message: str, config: configparser.ConfigParser) -> None:
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
