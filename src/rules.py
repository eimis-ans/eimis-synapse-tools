import re

from csv_extract import CSV_COLUMN_NAMES

email_regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
username_regex = re.compile(r"^[a-zA-Z0-9-_.]+$")

def check_entries(entries):
    """ Returns badly formatted entries."""
    for entry in entries:
        for key in CSV_COLUMN_NAMES:
            if not key in entry:
                raise Exception(f"Missing key: {key}")
            if not check_email(entry['email']):
                raise Exception(f"Bad email: {entry['email']}")
            if not check_username(entry['username']):
                raise Exception(f"Bad username: {entry['username']}")
            if not entry['display_name']:
                raise Exception(f"Missing display_name: {entry['display_name']}")

def check_duplicates(entries):

    for key in CSV_COLUMN_NAMES:
        result, duplicated = all_unique(entries, key)
        if not result:
            raise Exception(f"Duplicate : {key}: {duplicated}")
        
def all_unique(list, key):
    """ Returns True if there are no duplicate values in the list."""
    seen = set()
    for i in list:
        if i[key] in seen:
            return False, i[key]
        seen.add(i[key])
    return True, None

def check_email(email):
    return email_regex.match(email)

def check_username(username):
    return username_regex.match(username)