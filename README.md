# EIMIS Synapse tools

![Gitmoji](https://img.shields.io/badge/gitmoji-%20%F0%9F%98%9C%20%F0%9F%98%8D-FFDD67.svg)
![python](https://img.shields.io/badge/language-Python-3776AB?logo=Python)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## Configuration

And a some configurations in an `.env` file

```env
HOMESERVER_URL=https://matrix.example.com
SYNAPSE_SECRET=
ADMIN_USERNAME=
ADMIN_PASSWORD=
```

Find `SYNAPSE_SECRET` in your homeserver configuration

And will create the users on the homeserver.

## Prerequisites

- `Python3` and `pip` installed
- a Synapse server available with its Synapse secret
- a user having admin rights on Synapse homeserver
- [Poetry](https://python-poetry.org/) installed

## Install

```bash
pip install -r requirements.txt
```

## Usage

### Help

See all commands:

```bash
python3 src/main.py --help
```

### Import users

This python project will take as input a csv file

```csv
| display_name            | username                    | email     |
| ----------------------- | --------------------------- | --------- |
| John Doe - CHU de Nancy | @johndoe:eimis.beta.gouv.fr | jd@pm.com |
```

Then the command:

```bash
python3 src/main.py import-users --dry-run --csv-file ./data/users.csv
```

(remove `--dry-run` to actually create the users)

Users can then go to their favorite client and click on `forgot password`.

### Discovery room

```bash
python3 src/main.py setup-discoveryroom --help
python3 src/main.py setup-discoveryroom  -r matrix.develop.eimis.incubateur.net 
``````

## Tests

```bash
python3 -m unittest discover src
``````
