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

    ### This part is not required, since there will not be user input TODO make future config possible
    #if os.path.exists("./example-config.ini"): # this part checks for a newer version of the config file
    #    secparser = configparser.ConfigParser()
    #    secparser.read("./example-config.ini")
    #    if secparser["meta"]["name"] == config["meta"]["name"]: # since filename config.ini is not unique to this project, error check for the tag would be nice
    #        if int(secparser["meta"]["version"]) > int(config["meta"]["version"]):
    #            print("The example config file is on a newer version than current, manually upgrading is recomended")
    #            ### NOTE an auto update config file might be included in future versions of the codebase, currently as there are no outdated configs, such functionality is not needed.
    #            if int(secparser["meta"]["breaks"] >= config["meta"]["version"]):
    #                print("WARNING: extremely unstable behavior detected, currently using a config with breaking changes")
    #                r = input("Do you want to continue [y/N]")
    #                if r.lower() != "y":
    #                    exit("Exiting quietly")
    return config

def main():
    #check_paths_to_use()
    config = import_configparser()
    resp = webops.get_API_data(config, config["metainfo"]["apikey"], int(config["metainfo"]["category"]), int(config["metainfo"]["city"]), int(config["metainfo"]["type"]))
    if resp == None: # no connectivity (prolly)
        exit(f"404 (prolly at {int(time.time())})")
    header, rows = resp
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
            discord.send_alert_new_times(newdata, config=config)
        mdit.mdit(appenddata, "/app/.cache/latest.md")


if __name__ == "__main__":
    main()
