import unittest
from birdyboard import *


class Test_Birdyboard(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_app = Birdyboard()

    def test_defaults(self):
        self.assertEqual(self.test_app.user_name, None)

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
        self.public_adding_tweet = Birdyboard()
        self.public_adding_tweet.chirps_library = {"public": [[("hey", "what"), ("no", "thank you")], [("second", "text"), ("not", "sure how this will work.")]], "private": []}
        self.public_adding_tweet.add_new_public_chirp_thread("oh no.")
        self.assertIn([(None, "oh no.")], self.public_adding_tweet.chirps_library["public"], )

    def test_that_you_can_add_to_a_public_tweet(self):
        self.public_adding_tweet = Birdyboard()
        self.public_adding_tweet.chirps_library = {"public": [[("hey", "what"), ("no", "thank you")], [("second", "text"), ("not", "sure how this will work.")]], "private": []}
        self.public_adding_tweet.view_full_chirp("public", 0)
        self.public_adding_tweet.add_to_existing_chirp_thread("oh no!")
        self.assertIn((None, "oh no!"), self.public_adding_tweet.current_chirp["chirps"])
        self.assertIn((None, "oh no!"), self.public_adding_tweet.chirps_library["public"][0])

    def test_adding_user(self):
        self.user_add_test = Birdyboard()
        self.user_add_test.add_new_user("name", "password")
        self.assertIn({"user_name": "name", "password": "password"}, self.user_add_test.users)
        self.assertEqual(self.user_add_test.user_name, "name")



if __name__ == '__main__':
    unittest.main()
