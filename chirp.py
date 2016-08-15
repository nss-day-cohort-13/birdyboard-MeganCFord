import pickle
import uuid


class Chirper:
    """
    Handles the retrieval and creation of individual 'chirp' messages in birdyboard.py.
    all chirps are saved into a dictionary with a unique UUID key, and a unique thread ID from thread.py.

    Methods: deserialize_chirps, generate_new_chirp, serialize_chirps, generate_chirp_list.
    """

    def __init__(self):
        self.chirp_library = {}

    def deserialize_chirps(self):
        """
        Opens chirps.txt file. Handles what happens if there are no chirps.
        ========
        Method Arguments: None
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

    def generate_new_chirp(self, user_name, thread_id, text):
        """
        Adds a new chirp to the chirp library. Returns a unique key value for the new chirp so it can be added to its associated conversation. Runs deserialization and serialization functions.
        ========
        Method arguments: user id (top-level variable created in birdyboard when user logs in), conversation id, and string text for message.
        """
        chirp_key = str(uuid.uuid4())

        self.deserialize_chirps()
        self.chirp_library[chirp_key] = {"user": user_name, "message": text, "thread_id": thread_id}
        self.serialize_chirps()

        return chirp_key

    def serialize_chirps(self):
        """
        Saves new chirps to the chirps.txt file.
        ========
        Method arguments: none
        """
        with open("chirps.txt", "wb+") as chirps:
            pickle.dump(self.chirp_library, chirps)

    def generate_chirp_list(self, thread_id):
        """
        Receives a unique thread ID and prints. DOES NOT save the chirp list into a temp dict, since they don't need to be accessed or anything.
        ========
        Method arguments: the unique id of the thread being viewed.
        """
        self.deserialize_chirps()
        temp_chirps = []
        for key, value in self.chirp_library.items():
            if thread_id == value["thread_id"]:
                print("{0}: {1}".format(value["user"], value["message"]))
                temp_chirps.append(key)
        if len(temp_chirps) == 0:
            print("no chirps yet!")
