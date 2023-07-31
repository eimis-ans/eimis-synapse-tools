import csv
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

CSV_COLUMN_NAMES = ['email', 'username', 'display_name']


def read_file(csv_file):
    logging.info("Read file : " + csv_file + "...")

    line_count = 0
    all_entries = []
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            line_count += 1
            if line_count == 0:
                logging.info('read header...')
                continue
            all_entries += [row]

    logging.info(str(len(all_entries)) + " lines")
    return all_entries
