import unittest

from rules import all_unique, check_email, check_username

class TestSum(unittest.TestCase):

    def test_all_unique(self):
        entries = [{'email': 'a', 'username': 'b', 'phone': 'c'}, {'email': 'd', 'username': 'e', 'phone': 'f'}]
        result, duplicated = all_unique(entries, 'email' )
        self.assertTrue(result, "All emails are unique")
        self.assertIsNone(duplicated, "No duplicated email")

        entries = [{'email': 'a', 'username': 'b', 'phone': 'c'}, {'email': 'a', 'username': 'e', 'phone': 'f'}]
        result, duplicated = all_unique(entries, 'email' )
        self.assertFalse(result, "duplicate emails")
        self.assertEqual(duplicated, 'a', "duplicated email is a")

    def test_check_email(self):
        self.assertTrue(check_email("test.lala@gml.com"))
        self.assertTrue(check_email("test-user@jj.gh"))
        self.assertFalse(check_email("test.lala.com"))

    def test_check_username(self):
        self.assertFalse(check_username("@user1:matrix.org"))
        self.assertFalse(check_username("user1//matrix.org"))
        self.assertFalse(check_username("use r1"))
        self.assertTrue(check_username("user1"))
        self.assertTrue(check_username("user1-pouet"))
        self.assertTrue(check_username("user1_pouet"))
        self.assertTrue(check_username("user1_pou.et"))

if __name__ == '__main__':
    unittest.main()
