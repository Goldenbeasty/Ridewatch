# Ridewatch

This program is made to automatically scrape the e-autokool backend for free times

## Setup

Setup a virtual enviroment

In the project directory run

```bash
python3 -m venv venv
```

Activate the virtual enviroment

```bash
. ./venv/bin/activate
```

install the nessesary project requirements

```bash
pip install -r requirements.txt
```


### Cronjob

On a linux system you can set up a cronjob to automatically run the script every 5 minutes 10:00-21:00 every day

You can edit your crontab by running

```bash
crontab -e
```

and add the following line to it

**Note that you should edit the path after `cd` to match where you copied the project** 

```bash
*/5 10-21 * * * cd ~/Documents/Code/myproj && ./venv/bin/python daemon.py
```

The program stores the times at `~/.local/share/ridewatch/ridelogs` for future statistics

The program outputs a beautified output in `~/.local/share/ridewatch/first.md` in markdown format for ease of display

## Licence

This codebase is licenced under the GNU GPL v3 Licence


