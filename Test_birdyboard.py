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
        self.assertNotEqual(len(self.test_app.public_chirps), 0)

    def test_view_full_public_tweet(self):
        self.public_tweet_test = Birdyboard()
        self.public_tweet_test.public_chirps = [[("hey", "what"), ("no", "thank you")], [("second", "text"), ("not", "sure how this will work.")]]
        self.public_tweet_test.view_full_chirp(0)
        self.assertEqual(self.public_tweet_test.chirp_to_display, [("hey", "what"), ("no", "thank you")])

if __name__ == '__main__':
    unittest.main()
