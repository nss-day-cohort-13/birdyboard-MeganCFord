import pickle
import uuid

# TODO: add time stamp to chirps.


class Chirper:
    """
    handles the retrieval and creation of individual 'chirp' messages in birdyboard.py.
    Methods: deserialize_chirps, generate_new_chirp, serialize_chirps, chirp_search.
    """

    def __init__(self):
        self.chirp_library = {}

    def deserialize_chirps(self):
        """
        opens chirps.txt file. handles what happens if there are no chirps.
        """
        try:
            with open('chirps.txt', 'rb') as chirps:
                self.chirp_library = pickle.load(chirps)
        except FileNotFoundError:
                self.chirp_library = {"sample_key": {"user": "a_user_id", "message": "text", "thread_id": "sample_key"}}
        except EOFError:
                self.chirp_library = {"sample_key": {"user": "a_user_id", "message": "text", "thread_id": "sample_key"}}
        finally:
            pass

    def generate_new_chirp(self, user_id, thread_id, text):
        """
        adds a new chirp to the chirp library. Returns a unique key value for the new chirp so it can be added to its associated conversation. Runs deserialization and serialization functions.
        Arguments: user id (top-level variable created in birdyboard when user logs in), conversation id, and string text for message.
        """
        chirp_key = str(uuid.uuid4())

        self.deserialize_chirps()
        self.chirp_library[chirp_key] = {"user": user_id, "message": text}
        self.serialize_chirps()

        return chirp_key

    def serialize_chirps(self):
        """
        saves new chirps to the chirps.txt file.
        Arguments: none
        """
        with open("chirps.txt", "wb+") as chirps:
            pickle.dump(self.chirp_library, chirps)

    def generate_chirps_list(self, thread_id):
        """
        receives a unique thread ID and prints.
        """
        print("generating chirps list here.")
