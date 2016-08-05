import pickle
import uuid


class Usurper:
    """
    Handles the retrieval and creation of users in birdyboard.py.
    All users are saved into a dictionary with a unique UUID key.
    Methods: deserialize_users, generate_new_user, serialize_users, generate_users_list.
    """

    def __init__(self):
        self.user_library = {}
        self.temp_users = {}

    def deserialize_users(self):
        """
        Opens users.txt file. handles what happens if there are no users.
        """
        try:
            with open('users.txt', 'rb') as users:
                self.user_library = pickle.load(users)
        except FileNotFoundError:
                self.user_library = {"sample_key": {"user_name": "a_user_name", "real_name": "sample name"}}
        except EOFError:
                self.user_library = {"sample_key": {"user_name": "a_user_name", "real_name": "sample name"}}
        finally:
            pass

    def serialize_users(self):
        """
        Saves new users to the users.txt file.
        Arguments: none
        """
        with open("users.txt", "wb+") as users:
            pickle.dump(self.user_library, users)

    def generate_new_user(self, user_name, real_name):
        """
        Adds a new user to the user library. Returns a unique key value for the new user so it can be added to its associated conversation. Runs deserialization and serialization functions.
        Arguments: 1. username string text, 2. string text for real name.
        """
        user_key = str(uuid.uuid4())

        self.deserialize_users()
        self.user_library[user_key] = {"user_name": user_name, "real_name": real_name}
        self.serialize_users()

        return user_key

    def generate_users_list(self):
        """
        Deserializes users.txt, then prints a menu of users. Saves the menu indices associated with the library keys into a temporary variable, so the user can select an option based on the index.
        Arguments: None
        """
        self.deserialize_users()

        self.temp_users = {}
        index = 1
        for key, value in self.user_library.items():
            self.temp_users[index] = key
            print("{0}. {1}".format(index, value["user_name"]))
            index += 1
