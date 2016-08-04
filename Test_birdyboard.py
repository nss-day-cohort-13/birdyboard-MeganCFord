import unittest
from birdyboard import *
from user import *
from chirp import *
from thread import *


class Test_Birdyboard(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_app = Birdyboard()

    def test_the_init(self):
        self.assertIsInstance(self.test_app.threader, Threader)
        self.assertIsInstance(self.test_app.usurper, Usurper)
        self.assertIsInstance(self.test_app.chirper, Chirper)
        self.assertEqual(self.test_app.user_id, "")
        self.assertEqual(self.test_app.user_name, "")
        self.assertEqual(self.test_app.thread_id, "")
        self.assertEqual(self.test_app.public_or_private, "public")

if __name__ == '__main__':
    unittest.main()
