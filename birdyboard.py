import pickle
from chirp import *
from thread import *
from user import *


class Birdyboard:

    def __init__(self):
        # construction of three subclasses.
        self.chirper = Chirper()
        self.threader = Threader()
        self.usurper = Usurper()

        self.user_name = ""
        self.user_id = ""

        self.public_or_private = "public"

# ###############################
# ######## MENU PRINTERS ########
# ###############################

        self.unlogged_in_menu = "Welcome. You are not logged in.\n1. new user\n2. log in\n3. view public chirps\n'x' to exit.\n"
        self.logged_in_menu = "1. log out\n2. view public chirps\n3. view private chirps\n4. New public chirp thread\n5. new private chirp thread\n'x' to exit.\n"

        def does_the_user_want_to_leave(self, input_text):
            # TODO: put a thing on here that can check if the input text was b or x. use as a menu decorator.
            pass

# ############################################
# ######## UNLOGGED IN TOP LEVEL MENU ########
# ############################################

    def unlogged_in_menu_next_step(self):
        """
        requests input for top level menu functionality while the user is not logged in. Handles whether the user would like to log in, create a user, exit, or view public chirps.
        Arguments: none
        """
        next_step = input(">> ")
        if next_step == "1":  # create a user.
            print("creating a new user.")
            self.create_a_user_menu()
        elif next_step == "2":  # log in to a current user.
            self.usurper.generate_users_list()
            self.users_menu_next_step()
        elif next_step == "3":  # view public chirps. Does not have the option of commenting.
            self.public_or_private = "public"
            self.threader.generate_public_threads_list()
            self.view_threads_next_step()
        elif next_step == "x":  # exit.
            print("goodbye.")
            exit()
        else:
            print("command not found.")
            self.unlogged_in_menu_next_step()

# ##########################################
# ######## LOGGED IN TOP LEVEL MENU ########
# ##########################################

    def logged_in_menu_next_step(self):
        """
        Top level menu to print when user logs in or when logged in user traverses back to top-level. requests a next-step input and handles whether the user would like to log out, exit, view a public chirp, view a private chirp, or create a new public or private thread.
        Arguments: None
        """
        next_step = input(">> ")
        if next_step == "1":  # log out
            print('logging out.')
            self.user_name = ""
            print(self.unlogged_in_menu)
            self.unlogged_in_menu_next_step()
        elif next_step == "2":  # view public threads.
            self.public_or_private = "public"
            self.threader.generate_public_threads_list()
            self.view_threads_next_step()
        elif next_step == "3":  # view private threads.
            self.public_or_private = "private"
            self.threader.generate_private_threads_list(self.user_id)
            self.view_threads_next_step()
        elif next_step == "4":  # new public thread.
            self.public_or_private = "public"
            self.new_chirp_menu()
        elif next_step == "5":  # new private thread.
            self.public_or_private = "private"
            self.new_chirp_menu()
        elif next_step == "x":  # exit.
            print("goodbye.")
            exit()
        else:
            print("command not found.")
            self.logged_in_menu_next_step()

# ###############################
# ######## CREATE A USER ########
# ###############################

    def create_a_user_menu(self):
        """
        menu that prints as part of creating a new user (accessible from unlogged_in_menu). requests a user input and checks the input against the users list to make sure it doesn't already exist. if it doesn't, continues to generate a new user and log them in, capturing their unique user ID and new user name to display.
        Arguments: None
        """
        self.user_name = input("user name: ")
        if self.user_name == "b":  # go back.
            print("going back")
            self.user_name = ""
            print(self.unlogged_in_menu)
            self.unlogged_in_menu_next_step()
        elif self.user_name == "x":  # exit.
            print("goodbye.")
            exit()
        else:  # check entered username agains list of existing usernames.
            self.usurper.deserialize_users()
            for key, value in self.usurper.user_library.items():
                if self.user_name == value["user_name"]:
                    print("User name already taken!")
                    self.what_if_user_name_is_taken()
            full_name = input("your actual name: ")
            self.user_id = self.usurper.generate_new_user(self.user_name, full_name)
            print("logging in " + self.user_name + ".")
            print(self.logged_in_menu)
            self.logged_in_menu_next_step()

    def what_if_user_name_is_taken(self):
        """
        Menu that runs if a user enters a username in create_a_user_menu that is already taken. Requests input from the user and handles whether they would like to go back, see a list of users to choose from, try again to create a new user, or exit.
        Arguments: None
        """
        print("'b' to go back.\n'x' to exit.\n1. Choose from a list of created users.\n2. Try creating a user with a different name.")
        next_step = input(">> ")
        if next_step == "1":  # choose from a list of created users.
            self.usurper.generate_users_list()
            self.users_menu_next_step()
        elif next_step == "2":  # try creating a new user again.
            self.create_a_user_menu()
        elif next_step == "b":  # go back.
            print("going back.")
            print(self.unlogged_in_menu)
            self.unlogged_in_menu_next_step()
        elif next_step == "x":  # exit.
            print("goodbye.")
            exit()
        else:  # error handle.
            print("command not found.")
            self.what_if_user_name_is_taken()


# ############################
# ######## VIEW USERS ########
# ############################

    def users_menu_next_step(self):
        """
        prints after list of users is generated to gather what the user would like to do next- go back, exit, or log in to one of the users.
        arguments: None
        """
        next_step = input("'b' to go back.\n'x' to exit.\nChoose a user to log into.\n>> ")
        if next_step == "b":  # go back.
            print("going back.")
            print(self.unlogged_in_menu)
            self.unlogged_in_menu_next_step()
        elif next_step == "x":  # exit
            print("goodbye.")
            exit()
        else:
            try:  # make sure input is a number.
                next_step = int(next_step)
            except ValueError:
                print("you didn't enter a number.")
                self.users_menu_next_step()
            finally:
                try:
                    self.user_id = self.usurper.temp_users[next_step]
                    self.user_name = self.usurper.user_library[self.user_id]["user_name"]
                    print("logging in " + self.usurper.user_library[self.user_id]["real_name"] + "\n Welcome " + self.user_name + "!")
                    print(self.logged_in_menu)
                    self.logged_in_menu_next_step()
                except KeyError:
                    print("your number is not in the list of users.")
                    self.users_menu_next_step()
                finally:
                    pass

# #####################################
# ######## VIEW THREADS ###############
# #####################################

    def view_chirps_next_step(self):
        """
        menu that appears after all chirps are printed (view_chirps). Allows the user to view a full chirp thread based on the index, or to go back or exit.
        arguments: none
        """
        if user_name is not None:
            next_step = input("enter the number of the chirp you'd like to view the full thread for.\n'n' for new chirp thread.\n'b' to go back.\n'x' to exit.\n>> ")
        else: 
            next_step = input("enter the number of the chirp you'd like to view the full thread for.\n'b to go back.\n'x' to exit.\n>> ")

        if next_step == "b":
            print("going back.")
            if self.user_name is not None:
                print(self.logged_in_menu)
                self.logged_in_menu_next_step()
            else:
                print(self.unlogged_in_menu)
                self.unlogged_in_menu_next_step()
        elif next_step == "x":
            print("goodbye.")
            exit()
        elif next_step == "n":
            if self.user_name is not None:
                self.new_chirp_thread_menu()
            else:
                pass
        else:  # select the number of the printed tweet.
            try:
                next_step == int(next_step)
            except ValueError:
                print("you didn't enter a number.")
                self.view_chirps_next_step()
            finally:
                # TODO: mess with this until it works.
                if int(next_step)-1 >= 0:
                    try:
                        self.chirp_index = int(next_step)-1
                        checker = self.chirps_library[self.public_or_private][self.chirp_index]
                        self.view_full_chirp()
                        self.full_chirp_menu()
                    except IndexError:
                        print("your number is not in the list of chirps.")
                        self.view_chirps_next_step()
                    finally:
                        pass
                else:
                    print("your number is not in the list of chirps.")
                    self.view_chirps_next_step()

# ########################################
# ######## VIEW FULL CHIRP THREAD ########
# ########################################

    def view_full_chirp(self):
        """
        displays a full chirp based on the index chosen in view_chirps_next_step- public or private depending on top public_or_private variable.
        Arguments: none
        """
        if self.public_or_private == "public":
            [print(chirp[0] + ": " + chirp[1]) for chirp in self.chirps_library[self.public_or_private][self.chirp_index]]
        elif self.public_or_private == "private":
            [print(chirp[0] + ": " + chirp[1]) for chirp in self.chirps_library[self.public_or_private][self.chirp_index]["chirps"]]

    def full_chirp_menu(self):
        """
        prints after view_full_chirp to ask whether the user would like to go back, exit, or add to the chirp thread.
        arguments: none
        """
        if self.user_name is not None:
            next_step = input("1. add a new chirp to this thread.\n'b' to go back.\n'x' to exit.\n>> ")
        else:
            next_step = input("'b' to go back.\n'x' to exit.\n>> ")

        if next_step == "b":
            print("going back.")
            self.current_chirp = None
            self.view_chirps()
            self.view_chirps_next_step()
        elif next_step == "x":
            print("goodbye.")
            exit()
        elif next_step == "1":
            if self.user_name is not None:
                self.add_to_chirp_menu()
            else:
                print("command not recognized.")  # to keep an un-logged in user from pressing 1 and finding a SECRET INROAD to chirping.
                self.chirp_thread_menu()
        else:
            print("command not recognized.")
            self.chirp_thread_menu()

# #############################
# ######## ADD COMMENT ########
# #############################

    def add_to_chirp_menu(self):
        """
        requests input from the user for a new chirp to add to the curreng thread. error handles. Runs as part of full_chirp_menu.
        Arguments: none
        """
        chirp_to_add = input("'b' to go back.\n'x' to exit.\nchirp text: >> ")
        if chirp_to_add == "b":
            print("going back.")
            self.chirp_thread_menu()
        elif chirp_to_add == "x":
            print("goodbye.")
            exit()
        else:
            self.add_to_chirp(chirp_to_add)
        self.view_full_chirp()
        self.full_chirp_menu()

    def add_to_chirp(self, text):
        """
        runs as part of add_to_chirp_menu. adds a chirp to the current thread (top level variable public_or_private and current_index).

        Arguments: string text. ex: "this is a chirp."
        """
        self.deserialize_chirps_library()
        if self.public_or_private == "public":
            self.chirps_library[self.public_or_private][self.current_index].append(self.user_name, text)
        elif self.public_or_private == "private":
            self.chirps_library[self.public_or_private][self.current_index]["chirps"].append(self.user_name, text)
        self.serialize_chirps_library()


# ##################################
# ######## NEW CHIRP THREAD ########
# ##################################

    def new_chirp_thread_menu(self):
        """
        prints when 'new chirp' is chosen from top level menu. Requests input text and handles, based on whether the thread will be public or private, whether to send the chirp directly to serialization or to request a user to send a private chirp to.
        Arguments: none
        """

        print("'b' to go back.\n'x' to exit.\n******NEW " + self.public_or_private + " CHIRP THREAD:******")
        next_step = input("title text: >>")
        if next_step == "b":
            print("going back.")
            print(self.logged_in_menu)
            self.logged_in_menu_next_step()
        elif next_step == "x":
            print("goodbye.")
            exit()
        else:
            if self.public_or_private == "private":
                self.generate_users_menu()
                self.private_chirp_thread_menu()
            else:
                formatted_chirp = [(self.user_name, next_step)]
                self.add_new_thread(formatted_chirp)
                self.view_chirps()
                self.view_chirps_next_step()

    def private_chirp_thread_menu(self):
        """
        menu that prints when you're creating a new private chirp.
        requests input for the name of the second user you'd like to chirp to- keeping in mind that you can only chirp to people who already exist-
        the text that you'd like to send to them, formats the whole thing,
        and adds that to the add_new_thread function.

        Arguments: none
        """
        next_step = input("'b' to go back.\n'x' to exit.\nTo which user would you like to send your chirp?\n>> ")
        if next_step == "b":
            print("going back.")
        elif next_step == "x":
            print("goodbye.")
            exit()
        else:
            try:
                int_next_step = int(next_step)-1
            except ValueError:
                print("you didn't enter a number.")
                self.private_chirp_thread_menu()
            finally:
                try:
                    if int_next_step < 0:
                        print("your number is not in the list of users.")
                        self.private_chirp_thread_menu()
                    else:
                        user_two = self.users[next_step]
                except IndexError:
                    print("your number is not in the list of users.")
                    self.private_chirp_thread_menu
                finally:
                    text = input("what would you like to say? \n>> ")
                    if next_step == "b":
                        print("going back.")
                        print(self.logged_in_menu)
                        self.logged_in_menu_next_step()
                    elif next_step == "x":
                        print("goodbye.")
                        exit()
                    else:
                        formatted_chirp = {"users": (self.user_name, user_two["user_name"]), "chirps": [(self.user_name, text)]}
                        self.add_new_thread(formatted_chirp)
                        self.view_chirps()
                        self.view_chirps_next_step()

    def add_new_thread(self, formatted_chirp):
        """
        runs inside 'new chirp menu's, both public and private. adds a new chirp to a selected public chirp thread list, using current user name and text passed in from menu. also makes sure the .txt file is as up to date as possible.

        Arguments: formatted new-thread object from either new_chirp_thread_menu or private_chirp_thread_menu.

        FORMAT: for a public chirp, it's simply a 2-item tuple in a list [(user_name, text)]. for a private chirp, it's a dictionary: {users:(user1, user2), "chirps": (user1, text)}
        """
        self.deserialize_chirps_library()
        self.chirps_library[self.public_or_private].append(formatted_chirp)
        self.serialize_chirps_library()

# ###############################
# ######## SERIALIZATION ########
# ###############################

    

    def deserialize_users(self):
        """
        opens users.txt file. handles what happens if there are no users.
        """
        try:
            with open("users.txt", "rb") as users:
                self.users = pickle.load(users)
        except FileNotFoundError:
                self.users = [{"user_name": "megan", "password": "1234"}]
        except EOFError:
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
    print(app.unlogged_in_menu)
    app.unlogged_in_menu_next_step()
