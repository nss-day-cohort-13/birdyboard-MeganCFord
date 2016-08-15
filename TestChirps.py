import unittest
from chirp import *


class Test_Chirp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.tester = Chirper()

    def test_that_chirp_defaults_are_correct(self):
        self.assertIsInstance(self.tester.chirp_library, dict)

    def test_chirp_deserialization(self):
        self.de_tester = Chirper()
        self.assertEqual(len(self.de_tester.chirp_library), 0)
        self.de_tester.deserialize_chirps()
        self.assertNotEqual(len(self.de_tester.chirp_library), 0)

    def test_new_chirp_creation(self):
        unique_id = self.tester.generate_new_chirp("another_user", "sample_key", "moar text.")
        tester_object = self.tester.chirp_library[unique_id]
        self.assertEqual({"user": "another_user", "message": "moar text.", "thread_id": "sample_key"}, tester_object)

if __name__ == '__main__':
    unittest.main()
