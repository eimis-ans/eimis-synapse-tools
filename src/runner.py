import logging

from csv_extract import read_file
from synapse_client import SynapseClient

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def do_import_users(csv_file_path):
    logging.info("Importing users from " + csv_file_path + "...")

    entries = read_file(csv_file_path)

    logging.info("file read. Connect to Synapse...")
    mx_client = SynapseClient()

    for entry in entries:
        mx_client.create_user(entry["mxid"], entry["display_name"], entry["email"])