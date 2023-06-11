import requests
from bs4 import BeautifulSoup
import configparser
import datetime
from typing import List, Union, Tuple

### mappings between the table from the api and local storage
webrowmapping = {}
webrowmapping["time"] = 0
webrowmapping["location"] = 1
webrowmapping["ridetype"] = 2
webrowmapping["category"] = 3
webrowmapping["instructor"] = 4
webrowmapping["language"] = 5


def get_API_data(config: configparser.ConfigParser, apikey:str, cat: int, city: int, booktype:int) -> Union[Tuple[List, List], None]:
    params = {
        'api': '',
        'booking': '',
        'auth[apikey]': apikey,
        'cat': cat,
        'city': city,
        'type': booktype
    }
    try:
        r = requests.get(f"https://{config['host']['origin']}", params=params)
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print("An error occurred:", e)
        return None, None
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (status codes >= 400)
        print("HTTP Error:", e)
    except requests.exceptions.ConnectionError as e:
        # Handle connection errors
        print("Connection Error:", e)
    except requests.exceptions.Timeout as e:
        # Handle timeout errors
        print("Timeout Error:", e)

    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table element
    table = soup.find('table')

    # Extract table headers
    headers = [th.text for th in table.find('thead').find_all('th')]

    # Extract table rows
    rows = []
    for tr in table.find_all('tr'):
        # Skip the header row
        if tr.find('th'):
            continue
        row = [td.text for td in tr.find_all('td')]
        rows.append(row)

    return headers, rows

def to_unix_timestamp(time_string: str) -> int:
    time_format = "%d.%m.%Y %H:%M"
    datetime_obj = datetime.datetime.strptime(time_string, time_format)

    timestamp = int(datetime_obj.timestamp())
    return timestamp

def to_human_readable(timestamp: int) -> str:
    time_format = "%d.%m.%Y %H:%M"
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)

    time_string = datetime_obj.strftime(time_format)
    return time_string

def translate_web_list_to_dict(row: list[str]) -> dict:
    responseform = {}
    for key, value in webrowmapping.items():
        responseform[key] = row[value]
    responseform["time"] = to_unix_timestamp(responseform["time"])
    return responseform
