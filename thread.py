import pickle
import uuid


class Threader:
    """
    handles the retrieval and creation of chirp threads(lists of chirps) in birdyboard.py.
    Methods: deserialize_threads, generate_new_thread, serialize_threads, thread_search
    """

    def __init__(self):
        self.thread_library = {}
        self.temp_threads = {}

    def deserialize_threads(self):
        """
        opens threads.txt file. handles what happens if there are no threads.
        """
        try:
            with open('threads.txt', 'rb') as threads:
                self.thread_library = pickle.load(threads)
        except FileNotFoundError:
                self.thread_library = {"sample_key": {"title": "sample title", "public": True}}
        except EOFError:
                self.thread_library = {"sample_key": {"title": "sample title", "public": True}}
        finally:
            pass

    def generate_new_thread(self, title, user_ids=None):
        """
        generates a new public or private thread with a title and an empty chirp list. if a tuple of allowed user ids is passed as the second argument to this function, the thread is set to private and an allowed_users key is added. I bet eventually I could combine those two values ("if allowed_users exists, the thread is private") but this is more readable for me for right now.
        Returns the ID of the new thread so birdyboard can do something new with it.
        Arguments: 1. title of new thread. 2. (optional, used for private threads) Tuple with string ids of allowed users.
        """
        thread_key = str(uuid.uuid4())

        self.deserialize_threads()
        self.thread_library[thread_key] = {"title": title, "public": True}
        if user_ids is not None:
            self.thread_library[thread_key]["public"] = False
            self.thread_library[thread_key]["allowed_users"] = user_ids
        self.serialize_threads()

        return thread_key

    def serialize_threads(self):
        """
        saves new threads to the threads.txt file.
        Arguments: none
        """
        with open("threads.txt", "wb+") as threads:
            pickle.dump(self.thread_library, threads)

    def generate_public_threads_list(self):
        """
        this function prints a list of public thread titles when the user chooses 'view public chirps' option in the top level menu (either unlogged in or logged in). Deserializes threads, then generates a temporary threads dictionary with the printed indices, so the appropriate ID can be requested by the user entering an index number.

        Arguments: None
        """
        self.deserialize_threads()

        self.temp_threads = {}
        index = 1
        for key, value in self.thread_library.items():
            if value["public"] is True:
                self.temp_threads[index] = key
                print("{0}. {1}".format(index, value["title"]))
                index += 1

    def generate_private_threads_list(self, user_id):
        """
        this function prints a list of private thread titles when the user chooses 'view private chirps' option in the top level logged-in menu. Deserializes threads, then generates a temporary threads dictionary with the printed indices, so the appropriate ID can be requested by the user entering an index number.

        Arguments: unique user ID (automatically passed from birdyboard.py) to make sure the only private chirps printed are those involving the currently-logged in user.
        """

        self.deserialize_threads()

        self.temp_threads = {}
        index = 1
        for key, value in self.thread_library.items():
            if value["public"] is False:
                if user_id in value["allowed_users"]:
                    self.temp_threads[index] = key
                    print("{0}. {1}".format(index, value["title"]))
                    index += 1
        
