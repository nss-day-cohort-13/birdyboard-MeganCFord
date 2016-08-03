import unittest
from chirp import *


class Test_Chirp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.tester = Chirper()

    def test_that_chirp_defaults_are_correct(self):
        self.assertIsInstance(self.tester.chirp_library, dict)

    def test_chirp_deserialization(self):
        self.assertEqual(len(self.tester.chirp_library), 0)
        self.tester.deserialize_chirps()
        self.assertNotEqual(len(self.tester.chirp_library), 0)

    def test_new_chirp_creation(self):
        unique_id = self.tester.generate_new_chirp("another_user", "moar text.")
        tester_object = self.tester.chirp_search(unique_id)
        self.assertEqual({"user": "another_user", "message": "moar text."}, tester_object)

    def test_chirp_search(self):
        self.tester.deserialize_chirps()
        sample_object = self.tester.chirp_search("sample_key")
        self.assertEqual(sample_object, {"user": "a_user_id", "message": "text"})
        failure_object = self.tester.chirp_search("nonexistent")
        self.assertEqual(failure_object, None)


if __name__ == '__main__':
    unittest.main()
