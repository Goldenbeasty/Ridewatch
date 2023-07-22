# Ridewatch

This program is made to automatically scrape the e-autokool backend for free times

## Setup

You will need `docker` and `git`

Clone the repo

```bash
git clone https://github.com/goldenbeasty/ridewatch
```

Copy and configure the `example-config.ini` to `config.ini`

Start the containers

```bash
docker compose up -d
```
The program outputs a beautified output in `./.cache/latest.md` in markdown format if you wish to display it on a desktop widget for example

## Configuration wildcards

| Value    | cat    | city    | type    |
|---------------- | --------------- | --------------- | --------------- |
| 0   | wildcard    | wildcard    | invalid    |
| 1   | A   | Tallinn   | Square, Urban   |
| 2   | A   | Tartu   | Slippery ride   |
| 3   | B   | Pärnu   | Square, Urban   |
| 4   | -   | Rakvere   | ECO    |
| 5   | -   | -    | Simulator    |
| 6   | C   | Jõhvi    | -    |
| 7   | -   | -    | -    |
| 8   | -   | -    | -    |
| 9   |    | Jõgeva    | -    |
| 10   |    | -    |     |
| 11   |    | -    |     |
| 12   |    | -    |     |
| 13   |    | -    |     |
| 14   |    | -    |     |


## Copyright

Copyright (C) 2023  Goldenbeasty

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

