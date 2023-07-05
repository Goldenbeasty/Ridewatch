import json
import os
import configparser # however much I would like to use toml due to it's higher type safety and other features, the tomllib module was first shipped with python in 3.11, unfortunately it is too soon, while the latest Debian/stable ships 3.11, outdated systems exist
import shutil
import time

import webops
import dbmanagement
import mdit

configpath = "/app/config.ini"

DATA_OUTPUT_VERSION = 1

configpath = os.path.abspath(configpath)


def import_configparser():
    # check if the config.ini file exists
    if not os.path.exists(configpath):
        print(configpath)
        print(os.listdir())
        print("No config found")
        if not os.path.exists("./example-config.ini"):
            print("example config file not found, unable to configure")
            raise(FileNotFoundError(f"example-config.ini file not found at {os.path.abspath('./example-config.ini')}"))
        print("Copying the example configuration")
        shutil.copy("./example-config.ini", configpath)

    # load the config in the configpath
    config = configparser.ConfigParser()
    config.read(configpath)

    return config

def main():
    #check_paths_to_use()
    config = import_configparser()
    resp = webops.get_API_data(config, config["metainfo"]["apikey"], int(config["metainfo"]["category"]), int(config["metainfo"]["city"]), int(config["metainfo"]["type"]))
    if resp == None: # no connectivity (prolly)
        exit(f"404 (prolly at {int(time.time())})")
    header, rows = resp

    # Translate list of values to dict
    for index, row in enumerate(rows):
        rows[index] = webops.translate_web_list_to_dict(row)
    appenddata = rows
    newdata = []
    for timecheck in appenddata:
        isnew = dbmanagement.check_and_store_registration_time(timecheck)
        if isnew:
            newdata.append(timecheck)
    dbmanagement.update_is_taken_flag(appenddata)
    if len(newdata) != 0:
        if config["metainfo"]["enable_discord_integration"]:
            ENABLE_DISCORD = True
            import discord
        else:
            ENABLE_DISCORD = False
        if ENABLE_DISCORD:
            sendbuffer = []
            for unit in newdata:
                if "Automatic" not in unit["ridetype"]:
                    sendbuffer.append(unit)
            if len(sendbuffer) != 0:
                discord.send_alert_new_times(sendbuffer, config=config)
        mdit.mdit(appenddata, "/app/.cache/latest.md")


if __name__ == "__main__":
    main()
