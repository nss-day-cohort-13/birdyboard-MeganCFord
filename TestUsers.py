import unittest
from user import *


class Test_User(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.tester = Usurper()

    def test_that_user_defaults_are_correct(self):
        self.assertIsInstance(self.tester.user_library, dict)

    def test_user_deserialization(self):
        self.de_tester = Usurper()
        self.assertEqual(len(self.de_tester.user_library), 0)
        self.de_tester.deserialize_users()
        self.assertNotEqual(len(self.de_tester.user_library), 0)

    def test_new_user_creation(self):
        unique_id = self.tester.generate_new_user("a_user", "my name")
        tester_object = self.tester.user_library[unique_id]
        self.assertEqual({"user_name": "a_user", "real_name": "my name"}, tester_object)

if __name__ == '__main__':
    unittest.main()
