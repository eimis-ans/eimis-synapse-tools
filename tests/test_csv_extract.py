import unittest
from src.eimis_synapse_tools.csv_extract import read_file


class TestCsvExtract(unittest.TestCase):
    def test_read_file(self):
        expected_entries = [
            {'email': 'jd@pm.com', 'username': 'johndoe', 'display_name': 'John Doe - CHU de Nancy'},
            {'email': 'hh@jj.gh', 'username': 'jane.doe', 'display_name': 'Jane Doe - Canceropole de Lorraine'},
        ]
        actual_entries = read_file('example.csv')
        self.assertEqual(actual_entries, expected_entries)
