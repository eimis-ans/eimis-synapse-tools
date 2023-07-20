# Matrix enrollment script

This python project will take as input a csv file

```csv
| display_name            | username                        | email     |
| ----------------------- | --------------------------- | --------- |
| John Doe - CHU de Nancy | @johndoe:eimis.beta.gouv.fr | jd@pm.com |
```

And a some configurations in an `.env` file

```env
HOMESERVER_URL=https://matrix.eimis.beta.gouv.fr
SYNAPSE_SECRET="secret"
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secret
```

Find SYNAPSE_SECRET in your homeserver configuration

And will create the users on the homeserver.

## Install

```bash
pip install -r requirements.txt
```

## Usage

See all commands:

```bash
python3 src/main.py --help
python3 src/main.py import-users --help 
```

Main command:

```bash
python3 src/main.py --dry-run --csv-file ./data/users.csv
```

(remove `--dry-run` to actually create the users)

Users can then go to their favorite client and click on `forgot password`.

## Tests

```bash
python3 -m unittest discover src
``````
