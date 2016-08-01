import unittest
from birdyboard import *


class Test_Birdyboard(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_app = Birdyboard()

    def test_defaults(self):
        # TODO: eventually change this to test that default username equals None.
        self.assertEqual(self.test_app.user_name, "Megan")

    def test_that_public_tweets_load_correctly(self):
        self.assertIsInstance(self.test_app.chirps_library, dict)
        self.assertEqual(len(self.test_app.chirps_library), 2)
        self.test_app.deserialize_chirps_library()
        self.assertEqual(len(self.test_app.chirps_library), 2)
        self.assertNotEqual(len(self.test_app.chirps_library["public"]), 0)

    def test_view_full_public_tweet(self):
        self.public_tweet_test = Birdyboard()
        self.public_tweet_test.chirps_library = {"public": [[("hey", "what"), ("no", "thank you")], [("second", "text"), ("not", "sure how this will work.")]], "private": []}
        self.public_tweet_test.view_full_chirp("public", 0)
        self.assertEqual(self.public_tweet_test.current_chirp, {"location": "public", "index": 0, "chirps": [("hey", "what"), ("no", "thank you")]})

    def test_that_public_tweet_adds(self):
        pass

    def test_that_you_can_add_to_a_public_tweet(self):
        pass


if __name__ == '__main__':
    unittest.main()
