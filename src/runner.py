import logging

from csv_extract import read_file

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def do_import_users(csv_file):
    logging.info("Importing users from " + csv_file + "...")

    entries = read_file(csv_file)
