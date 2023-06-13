import webops
import time
import os

### Protodef
# first non auto time

#first non auto double time

# total free times in the next 7 days

def mdit(data:dict, path: str) -> None: # it is function callers job to make sure the data variable has at least one valid time
    datalist = []
    limittime = int(time.time()) + (3600 * 24 * 7)
    for unit in data["avalable_times"]:
        if "Automatic" in unit["ridetype"]:
            continue
        if unit["time"] > limittime:
            continue
        datalist.append(unit)
    if len(datalist) == 0:
        return
    firstfreetime = datalist[0]

    # sort the times by instructor
    instructordb = {}
    for unit in datalist:
        if unit["instructor"] not in instructordb.keys():
            instructordb[unit["instructor"]] = []
        instructordb[unit["instructor"]].append(unit)

    consecutivetimesdb = []
    for instructor, times in instructordb.items():
        if len(times) < 2:
            continue
        lasttime = times[0]["time"]
        for i in range(1, len(times)):
            if times[i]["time"] <= lasttime + (4000):
                consecutivetimesdb.append([times[i - 1], times[i]])

    # find the earliest time
    if len(consecutivetimesdb) != 0:
        earlyindex = 0
        earlytime = consecutivetimesdb[0][0]["time"]
        for index, unit in enumerate(consecutivetimesdb):
            if unit[0]["time"] < earlytime:
                earlyindex = index
        firstdoubletime = consecutivetimesdb[earlyindex]
    else:
        firstdoubletime = None

    if firstdoubletime:
        dtstring = f"""**{webops.to_human_readable(firstdoubletime[0]["time"])}** with **{firstdoubletime[0]["instructor"]}**"""
    else:
        dtstring = "None"

    

    output_string = f"""First free time: **{webops.to_human_readable(firstfreetime["time"])}** with **{firstfreetime["instructor"]}**

First double time: {dtstring}

Total of **{len(datalist)}** free times in the next 7 days
    """
    outputpath = os.path.abspath(os.path.expanduser(path=path))
    with open(outputpath, "w") as f:
        f.write(output_string)
    print(output_string)




if __name__ == "__main__":
    import os
    import json

    data = json.load(open(os.path.expanduser("~/.local/share/ridewatch/latest.json")))
    mdit(data, "~/.local/share/ridewatch/first.md")
