# Matrix enrollment script

This python project will take as input a csv file

```csv
| display name            | mxid                        | email     |
| ----------------------- | --------------------------- | --------- |
| John Doe - CHU de Nancy | @johndoe:eimis.beta.gouv.fr | jd@pm.com |
```

And a some configurations in an `.env` file

```env
HOMESERVER_URL=https://matrix.eimis.beta.gouv.fr
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secret
```

And will create the users on the homeserver.

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 src/main.py --dry-run --csv-file ./data/users.csv
```

(remove `--dry-run` to actually create the users)

Users can then go to their favorite client and click on `forgot password`.
