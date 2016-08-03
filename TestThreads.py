import unittest
from thread import *


class Test_Chirp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.tester = Threader()

    def test_that_thread_defaults_are_correct(self):
        self.assertIsInstance(self.tester.thread_library, dict)

    def test_thread_deserialization(self):
        self.assertEqual(len(self.tester.thread_library), 0)
        self.tester.deserialize_threads()
        self.assertNotEqual(len(self.tester.thread_library), 0)

    def test_new_public_thread_creation(self):
        unique_id = self.tester.generate_new_thread("additional title")
        tester_object = self.tester.thread_search(unique_id)
        self.assertEqual({"title": "additional title", "public": True, "chirps": []}, tester_object)

    def test_new_private_thread_creation(self):
        unique_id = self.tester.generate_new_thread("another title", ("user_id", "another_user_id"))
        tester_object = self.tester.thread_search(unique_id)
        self.assertEqual({"title": "another title", "public": False, "allowed_users": ("user_id", "another_user_id"), "chirps": []}, tester_object)

    def test_thread_search(self):
        self.tester.deserialize_threads()
        sample_object = self.tester.thread_search("sample_key")
        self.assertEqual(sample_object, {"title": "sample title", "public": True, "chirps": []})
        failure_object = self.tester.thread_search("nonexistent")
        self.assertEqual(failure_object, None)


if __name__ == '__main__':
    unittest.main()
