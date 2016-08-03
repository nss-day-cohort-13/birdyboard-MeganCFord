import unittest
from user import *


class Test_User(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.tester = Usurper()

    def test_that_user_defaults_are_correct(self):
        self.assertIsInstance(self.tester.user_library, dict)

    def test_user_deserialization(self):
        self.assertEqual(len(self.tester.user_library), 0)
        self.tester.deserialize_users()
        self.assertNotEqual(len(self.tester.user_library), 0)

    def test_new_user_creation(self):
        unique_id = self.tester.generate_new_user("a_user", "my name")
        tester_object = self.tester.user_search(unique_id)
        self.assertEqual({"user_name": "a_user", "real_name": "my name"}, tester_object)

    def test_user_search(self):
        self.tester.deserialize_users()
        sample_object = self.tester.user_search("sample_key")
        self.assertEqual(sample_object, {"user_name": "a_user_id", "real_name": "sample name"})
        failure_object = self.tester.user_search("nonexistent")
        self.assertEqual(failure_object, None)


if __name__ == '__main__':
    unittest.main()
