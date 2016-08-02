

# I'm going to start with everyone sharing one user, and have all tweets be public.

# so the menu will be:
# View Chirps
# new chirp (public)

# structure of the chirps is going to be:
#
import pickle

# I'm going to start with everyone sharing one user, and have all tweets be public.


class Birdyboard:

    def __init__(self):
        self.user_name = None
        self.chirps_library = {"public": [], "private": []}
        self.current_chirp = None
        self.public_or_private = ""
        self.users = []

# ############################################
# ######## UNLOGGED IN TOP LEVEL MENU ########
# ############################################

    def unlogged_in_menu_print(self):
        """
        prints the choices for an unlogged-in user, at start of app.
        Arguments: none
        """
        print("Welcome. You are not logged in.\n")
        print("1. new user\n2. log in\n3. view public chirps\n'x' to exit.\n")

    def unlogged_in_menu_next_step(self):
        """
        requests input for top level menu functionality while the user is not logged in. Currently does not do anything for user login. secret fourth option to add a chirp but later that will be only an option if you're logged in.
        Arguments: none
        """
        next_step = input(">> ")
        # error handling.
        if len(next_step) > 1:
            print("you only need to type one character!")
            self.unlogged_in_menu_next_step()
        elif next_step not in ["1", "2", "3", "x"]:
            print("please choose one of the options shown above.")
            self.unlogged_in_menu_next_step()
        # allowed options.
        elif next_step == "1":  # create a user.
            print("creating a new user.")
            self.create_a_user_menu()
        elif next_step == "2":  # log in to a current user.
            print('log in to a current user will show up here.')
        elif next_step == "3":  # view public chirps. does not have the option of commenting.
            self.deserialize_chirps_library()
            self.view_public_chirps()
            self.view_chirps_next_step()
        elif next_step == "x":  # exit.
            print("goodbye.")
            exit()

# ##########################################
# ######## LOGGED IN TOP LEVEL MENU ########
# ##########################################

    def logged_in_menu_print(self):
        print("welcome " + self.user_name + "!")
        print("1. log out\n2. view public chirps\n3. view private chirps\n4. New public chirp thread\n5. new private chirp thread\n'x' to exit.\n")

    def logged_in_menu_next_step(self):
        next_step = input(">> ")
        # error handling.
        if len(next_step) > 1:
            print("you only need to type one character!")
            self.logged_in_menu_next_step()
        elif next_step not in ["1", "2", "3", "4", "5", "x"]:
            print("please choose one of the options shown above.")
            self.logged_in_menu_next_step()
        # allowed options.
        elif next_step == "1":  # log out
            print('logging out.')
            self.user_name = None
            self.unlogged_in_menu_print()
            self.unlogged_in_menu_next_step()
        elif next_step == "2":  # view public chirps.
            self.deserialize_chirps_library()
            self.view_public_chirps()
            self.view_chirps_next_step()
        elif next_step == "3":  # view private chirps.
            print("view private chirps will show up here.")
        elif next_step == "4":  # new public chirp.
            self.new_chirp_menu()
        elif next_step == "5":  # new private chirp.
            self.new_chirp_menu()
        elif next_step == "x":  # exit.
            print("goodbye.")
            exit()

# ###############################
# ######## CREATE A USER ########
# ###############################

    def create_a_user_menu(self):
        self.deserialize_users()
        print(type(self.users))
        user_name = input("user name: ")
        for user in self.users:
            if user_name == user["user_name"]:
                print("User name already taken!")
                self.what_if_user_name_is_taken()
        password = input("password: ")
        self.add_new_user(user_name, password)
        print("logging in " + user_name + ".")
        self.logged_in_menu_print()
        self.logged_in_menu_next_step()

    def what_if_user_name_is_taken(self):
        print("1. Choose from a list of created users.\n2. Try creating a user with a different name.")
        next_step = input(">> ")
        if next_step == "1":
            self.view_users_menu()
            self.users_menu_next_step()
        elif next_step == "2":
            self.create_a_user_menu()
        else:
            print("command not found.")
            self.what_if_user_name_is_taken()

    def add_new_user(self, user_name, password):
        self.deserialize_users()
        self.users.append({"user_name": user_name, "password": password})
        self.serialize_users()
        self.user_name = user_name


# ############################
# ######## VIEW USERS ########
# ############################

    def view_users_menu(self):
        self.deserialize_users()
        [print(str(self.users.index(user) + 1) + ". " + user["username"]) for user in self.users]
        self.users_menu_next_step()

    def users_menu_next_step(self):
        pass

# ####################################
# ######## VIEW PUBLIC CHIRPS ########
# ####################################

    def view_public_chirps(self):
        """
        this function is called if the user presses "3" on the unlogged-in menu, after deserialization. prints the first chirp of all public chirp threads, formatted to also show the user name, and print a readable index number for selection of 'view full chirp'.
        Arguments: none.
        """
        self.public_or_private = "public"

        print("******PUBLIC CHIRPS******")
        if len(self.chirps_library["public"]) > 0:
            [print(str(self.chirps_library["public"].index(chirp) + 1) + ". " + chirp[0][0] + ": " + chirp[0][1]) for chirp in self.chirps_library["public"]]
            print("\n")
        else:
            print("no public chirps yet!\n")

    def view_private_chirps(self):

        self.public_or_private = "private"

        print("******PRIVATE CHIRPS******")
        if len(self.chirps_library["private"]) > 0:
            [print(str(self.chirps_library["private"].index(chirp) + 1) + ". " + chirp[0][0] + ": " + chirp[0][1]) for chirp in self.chirps_library["private"]]
            print("\n")
        else:
            print("no private chirps yet!\n")

    def view_chirps_next_step(self):
        """
        menu that appears after all chirps are printed (view_chirps). Allows the user to view a full chirp thread based on the index, or to go back or exit.
        arguments: none
        """
        next_step = input("enter the number of the chirp you'd like to view the full thread for.\n'n' for new chirp.\n'b' to go back.\n'x' to exit.>> ")

        if next_step == "b":
            print("going back.")
            if self.user_name is not None:
                self.logged_in_menu_print()
                self.logged_in_menu_next_step()
            else:
                self.unlogged_in_menu_print()
                self.unlogged_in_menu_next_step()
        elif next_step == "x":
            print("goodbye.")
            exit()
        elif next_step == "n":
            pass
            # make a new tweet.
        else:  # select the number of the printed tweet.
            try:
                next_step == int(next_step)
            except ValueError:
                print("you didn't enter a number.")
                self.view_chirps_next_step()
            finally:
                try:
                    if int(next_step)-1 >= 0:
                        chirp_index = int(next_step)-1
                        # TODO: grab whether or not this is a public or private one and determine the correct private-tweet index.
                        self.view_full_chirp(self.public_or_private, chirp_index)
                        self.chirp_thread_menu()
                    else:
                        print("your number is not in the list of chirps.")
                        self.view_chirps_next_step()
                except IndexError:
                    print("your number is not in the list of chirps.")
                    self.view_chirps_next_step()
                finally:
                    pass

    def view_full_chirp(self, public_or_private, chirp_index):
        """
        displays a full chirp based on the index chosen in view_chirps_next_step. currently only handles public tweets. The numerical display of the public tweets makes sense, but grabbing the private tweets by index isn't going to work so I'm going to need to come up with another way to do that.
        Arguments: 1. string "public" or string "private" for location, 2. index number.
        """
        self.current_chirp = {"location": public_or_private, "index": chirp_index, "chirps": self.chirps_library[public_or_private][chirp_index]}
        [print(chirp[0] + ": " + chirp[1]) for chirp in self.current_chirp["chirps"]]
        print("\n")

    def chirp_thread_menu(self):
        """
        prints after view_full_chirp to ask whether the user would like to go back, exit, or add to the chirp thread.
        arguments: none
        """
        # TODO: add an 'add comment' option here.
        next_step = input("1. add a new chirp to this thread.\n'b' to go back.\n'x' to exit.\n>> ")

        if next_step not in["1", "x", "b"]:
            print("command not recognized.")
            self.chirp_thread_menu()
        elif next_step == "b":
            print("going back.")
            self.chirp_to_display = None
            self.view_public_chirps()
            self.view_chirps_next_step()
        elif next_step == "1":
            self.new_chirp_menu()
        elif next_step == "b":
            print("goodbye.")
            exit()

    def new_chirp_thread_menu(self):

        print("'b' to go back.\n'x' to exit.\n******NEW CHIRP THREAD:******")
        if self.public_or_private == "private":
            other_user = input("who would you like to send this chirp to? >> ")
            if chirp_to_add == "b":
                print("going back.")
            elif chirp_to_add == "x":
                print("goodbye.")
                exit()
        chirp_to_add = input("\nchirp text: >> ")
        if chirp_to_add == "b":
            print("going back.")
        elif chirp_to_add == "x":
            print("goodbye.")
            exit()
        else:
            if self.public_or_private == "public":
                self.add_new_public_chirp_thread(chirp_to_add)
                self.view_public_chirps()
                self.view_chirps_next_step()
            elif self.public_or_private == "private":
                self.add_new_private_chirp_thread(other_user, chirp_to_add)
                self.view_private_chirps()
                self.view_chirps_next_step()



    def new_chirp_menu(self):
        """
        UNFINISHED, will probably break out at a higher level. Currently, runs when '1' is chosen in chirp_thread_menu, or when option 4 is chosen in top level menu to start a new thread. either adds a completely new chirp thread with one item in it, or appends a chirp to an existing thread.
        Arguments: none
        """
        if self.current_chirp is not None:

            if self.public_or_private == "public":
                # TODO: nest the adding chirp into a further menu so you can view a thread without having to add to it.
                chirp_to_add = input("'b' to go back.\n'x' to exit.\nchirp text: >> ")
                if chirp_to_add == "b":
                    print("going back.")
                elif chirp_to_add == "x":
                    print("goodbye.")
                    exit()
                else:
                    self.add_to_existing_chirp_thread(chirp_to_add)
                self.view_full_chirp(self.public_or_private, self.current_chirp["index"])
                self.chirp_thread_menu()
                # TODO: handle private tweeting.
            elif self.current_chirp["location"] == "private":
                print("private chirps will go here.")
                self.chirp_thread_menu()

    def add_new_public_chirp_thread(self, text):
        """
        runs inside 'new chirp menu'. adds a new top level chirp thread to the public chirp thread list, using current user name and text passed in from menu. also makes sure the .txt file is as up to date as possible.
        Arguments: string of text. ex: "this is a chirp."
        """
        self.deserialize_chirps_library()  # this is in case the library has not been opened yet!
        self.chirps_library["public"].append([(self.user_name, text)])
        self.serialize_chirps_library()

    def add_new_private_chirp_thread(self, other_user, text):
        self.deserialize_chirps_library()
        self.chirps_library["private"].append({"users": (self.user_name, other_user), "chirps": [(self.user_name, text)]})
        self.serialize_chirps_library()

    def add_to_existing_chirp_thread(self, text):
        """
        runs inside 'new chirp menu'. adds a new chirp to a selected public chirp thread list, using current user name and text passed in from menu. also makes sure the .txt file is as up to date as possible.
        Arguments: string of text. ex: "this is a chirp."
        """
        self.chirps_library["public"][self.current_chirp["index"]].append((self.user_name, text))
        self.serialize_chirps_library()

    def deserialize_chirps_library(self):
        """
        opens chirps.txt file. handles what happens if there are no chirps.
        """
        try:
            with open('chirps.txt', 'rb') as chirps:
                self.chirps_library = pickle.load(chirps)

        except FileNotFoundError:
                self.chirps_library = {"public": [], "private": []}
        except EOFError:
                self.chirps_library = {"public": [], "private": []}

    def serialize_chirps_library(self):
        """
        saves new chirps to the chirps.txt file.
        Arguments: none
        """
        with open("chirps.txt", "wb+") as chirps:
            pickle.dump(self.chirps_library, chirps)

    def deserialize_users(self):
        """
        opens users.txt file. handles what happens if there are no users.
        """
        try:
            with open("users.txt", "rb") as users:
                self.users = pickle.load(users)
                print(self.users)
        except FileNotFoundError:
                print("file not found error.")
                self.users = [{"user_name": "megan", "password": "1234"}]
        except EOFError:
                print("end of file error.")
                self.users = [{"user_name": "megan", "password": "1234"}]

    def serialize_users(self):
        """
        saves new users to the users.txt file.
        Arguments: none
        """
        with open("users.txt", "wb+") as users:
            pickle.dump(self.users, users)


if __name__ == '__main__':
    app = Birdyboard()
    app.unlogged_in_menu_print()
    app.unlogged_in_menu_next_step()
