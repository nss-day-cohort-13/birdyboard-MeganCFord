# not sure what I'm testing yet but I know I need some kind of test suite.

import unittest
from birdyboard import *


class Test_Birdyboard(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_app = Birdyboard()

    def test_username_default(self):
        # TODO: eventually change this to test that default username equals None.
        self.assertEqual(self.test_app.user_name, "Megan")

    def test_that_public_tweets_load_correctly(self):
        self.assertIsInstance(self.test_app.public_chirps, list)
        self.assertEqual(len(self.test_app.public_chirps), 0)
        self.test_app.unlogged_in_view_chirps()
        # test that length is no longer 0 I guess?

if __name__ == '__main__':
    unittest.main()
