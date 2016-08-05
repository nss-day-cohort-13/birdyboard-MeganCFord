import pickle
from chirp import *
from thread import *
from user import *


class Birdyboard:
    """
    this app's functionality is a private/public message board. It constructs three subclasses which pull serialized data from three .txt files: users, threads, and chirps. All items in these three files are identified by a unique UUID.

    An unlogged in user can view available logins and view (but not add to) public threads and their associated chirps.
    A logged in user can log out, view lists of public and private threads (and add new threads), and view and add to chirps associated with threads. They can only view the private chirps they are part of.

    When a new private thread is created, the UUIDs of the two associated users are saved into its information so it is only accessible through its associated user set,
    and when a new chirp is created, the UUID of the thread is saved into its information so it is only accessible through its associated thread.

    Methods: unlogged_in_menu, logged_in_menu, create_a_user_menu, what_if_user_name_is_taken, users_menu, view_threads_menu, new_public_thread_menu, new_private_thread_menu, what_if_thread_name_is_taken, full_chirp_menu, and add_to_chirp_menu.

    """

    def __init__(self):
        # construction of three subclasses.
        self.chirper = Chirper()
        self.threader = Threader()
        self.usurper = Usurper()

        self.user_name = ""
        self.user_id = ""

        self.thread_id = ""

        self.public_or_private = "public"

# ###############################
# ######## MENU PRINTERS ########
# ###############################

        self.unlogged_in_options = "Welcome. You are not logged in.\n1. new user\n2. log in\n3. view public chirps\n'x' to exit.\n"
        self.logged_in_options = "1. log out\n2. view public chirps\n3. view private chirps\n4. New public chirp thread\n5. new private chirp thread\n'x' to exit.\n"

# ############################################
# ######## UNLOGGED IN TOP LEVEL MENU ########
# ############################################

    def unlogged_in_menu(self):
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
            self.users_menu()
        elif next_step == "3":  # view public chirps. Does not have the option of commenting.
            self.public_or_private = "public"
            self.threader.generate_public_threads_list()
            self.view_threads_menu()
        elif next_step == "x":  # exit.
            print("goodbye.")
            exit()
        else:
            print("command not found.")
            self.unlogged_in_menu()

# ##########################################
# ######## LOGGED IN TOP LEVEL MENU ########
# ##########################################

    def logged_in_menu(self):
        """
        Top level menu to print when user logs in or when logged in user traverses back to top-level. requests a next-step input and handles whether the user would like to log out, exit, view a public chirp, view a private chirp, or create a new public or private thread.
        Arguments: None
        """
        next_step = input(">> ")
        if next_step == "1":  # log out
            print('logging out.')
            self.user_name = ""
            print(self.unlogged_in_options)
            self.unlogged_in_menu()
        elif next_step == "2":  # view public threads.
            self.public_or_private = "public"
            self.threader.generate_public_threads_list()
            self.view_threads_menu()
        elif next_step == "3":  # view private threads.
            self.public_or_private = "private"
            self.threader.generate_private_threads_list(self.user_id)
            self.view_threads_menu()
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
            self.logged_in_menu()

# ###############################
# ######## CREATE A USER ########
# ###############################

    def create_a_user_menu(self):
        """
        menu that prints as part of creating a new user (accessible from unlogged_in_menu). requests a user input and checks the input against the users list to make sure it doesn't already exist. if it doesn't, continues to generate a new user and log them in, capturing their unique user ID and new user name to display.
        Arguments: None
        """
        user_name = input("user name: ")
        if user_name == "b":  # go back.
            print("going back")
            user_name = ""
            print(self.unlogged_in_options)
            self.unlogged_in_menu()
        elif user_name == "x":  # exit.
            print("goodbye.")
            exit()
        else:  # check entered username agains list of existing usernames.
            self.usurper.deserialize_users()
            for key, value in self.usurper.user_library.items():
                if user_name == value["user_name"]:
                    print("User name already taken!")
                    self.what_if_user_name_is_taken()
            full_name = input("your actual name: ")
            self.user_name = user_name
            self.user_id = self.usurper.generate_new_user(user_name, full_name)
            print("logging in " + user_name + ".")
            print(self.logged_in_options)
            self.logged_in_menu()

    def what_if_user_name_is_taken(self):
        """
        Menu that runs if a user enters a username in create_a_user_menu that is already taken. Requests input from the user and handles whether they would like to go back, see a list of users to choose from, try again to create a new user, or exit.
        Arguments: None
        """
        print("'b' to go back.\n'x' to exit.\n1. Choose from a list of created users.\n2. Try creating a user with a different name.")
        next_step = input(">> ")
        if next_step == "1":  # choose from a list of created users.
            self.usurper.generate_users_list()
            self.users_menu()
        elif next_step == "2":  # try creating a new user again.
            self.create_a_user_menu()
        elif next_step == "b":  # go back.
            print("going back.")
            print(self.unlogged_in_options)
            self.unlogged_in_menu()
        elif next_step == "x":  # exit.
            print("goodbye.")
            exit()
        else:  # error handle.
            print("command not found.")
            self.what_if_user_name_is_taken()


# ############################
# ######## VIEW USERS ########
# ############################

    def users_menu(self):
        """
        prints after list of users is generated to gather what the user would like to do next- go back, exit, or log in to one of the users.
        arguments: None
        """
        next_step = input("'b' to go back.\n'x' to exit.\nChoose a user to log into.\n>> ")
        if next_step == "b":  # go back.
            print("going back.")
            print(self.unlogged_in_options)
            self.unlogged_in_menu()
        elif next_step == "x":  # exit
            print("goodbye.")
            exit()
        else:
            try:  # make sure input is a number.
                next_step = int(next_step)
            except ValueError:
                print("you didn't enter a number.")
                self.users_menu()
            finally:
                try:
                    self.user_id = self.usurper.temp_users[next_step]
                    self.user_name = self.usurper.user_library[self.user_id]["user_name"]
                    print("logging in " + self.usurper.user_library[self.user_id]["real_name"] + "\n Welcome " + self.user_name + "!")
                    print(self.logged_in_options)
                    self.logged_in_menu()
                except KeyError:
                    print("your input is not in the list of users.")
                    self.users_menu()
                finally:
                    pass

# #####################################
# ######## VIEW THREADS ###############
# #####################################

    def view_threads_menu(self):
        """
        menu that appears after all chirp threads are printed (threader.generate_threads_list). Allows the user to view a full chirp thread based on the index, or to go back or exit.
        arguments: none
        """

        # deal with the fact that un-logged in users can see public chirp threadsbut only logged-in users can add a new thread. Also handle what happens if there are no threads to view.
        logged_in = False
        if len(self.user_name) > 0:
            logged_in = True

        print("'n' for new chirp thread.\n'b' to go back.\n'x' to exit.")

        if len(self.threader.temp_threads) == 0:
            print("no private chirps yet!")
        else:
            if logged_in is True:
                print("enter the number of the chirp you'd like to view the full thread for.")
                thread = input(">> ")
            else:
                thread = input(">> ")

        # handle input.
        if thread == "b":  # go back to either logged in or unlogged in menu.
            print("going back.")
            if logged_in is True:
                print(self.logged_in_options)
                self.logged_in_menu()
            else:
                print(self.unlogged_in_options)
                self.unlogged_in_menu()
        elif thread == "x":  # exit.
            print("goodbye.")
            exit()
        elif thread == "n":  # allow a user to create a new thread, but not an unlogged-in user.
            if logged_in is True:
                if self.public_or_private == "public":  # create a new public or private thread.
                    self.new_public_thread_menu()
                else:
                    self.usurper.generate_users_list()
                    self.new_private_thread_menu()
            else:
                pass
        else:  # select the number of the printed tweet.
            try:
                thread = int(thread)
            except ValueError:
                print("you didn't enter a number.")
                self.view_threads_menu_thread()
            finally:
                try:
                    self.thread_id = self.threader.temp_threads[thread]
                    self.chirper.generate_chirp_list(self.thread_id)
                    self.full_chirp_menu()
                except KeyError:
                    print("your input is not in the list of threads.")
                    self.view_threads_menu()
                finally:
                    pass

# ##################################
# ######## NEW CHIRP THREAD ########
# ##################################

    def new_public_thread_menu(self):
        """
        Prints when 'new public chirp' is chosen from top level menu, or from view chirps menu when self.public_or_private is set to public. Requests title text input and sends to thread.py appropriately.
        Arguments: none
        """

        print("'b' to go back.\n'x' to exit.\n")
        next_step = input("thread title: >>")
        if next_step == "b":  # go back
            print("going back.")
            print(self.logged_in_options)
            self.logged_in_menu()
        elif next_step == "x":  # exit
            print("goodbye.")
            exit()
        else:  # check entered username agains list of existing usernames.
            self.threader.deserialize_threads()
            for key, value in self.threader.thread_library.items():
                if next_step == value["title"]:
                    print("thread title already taken!")
                    self.what_if_thread_name_is_taken()
            self.thread_id = self.threader.generate_new_thread(next_step)
            self.chirper.generate_chirp_list(self.thread_id)
            self.full_chirp_menu()

    def new_private_thread_menu(self):
        """
        Prints when 'new private chirp' is chosen from top level menu, or from view chirps menu when self.public_or_private is set to private. handles who to send the chirp to, title text input, and sends both to thread.py appropriately.
        Arguments: none
        """
        next_step = input("'b' to go back.\n'x' to exit.\nTo which user would you like to send your chirp?\n>> ")
        if next_step == "b":  # go back
            print("going back.")
            print(self.logged_in_options)
            self.logged_in_menu()
        elif next_step == "x":  # exit
            print("goodbye.")
            exit()
        else:
            try:
                next_step = int(next_step)
            except ValueError:
                print("you didn't enter a number.")
                self.private_chirp_thread_menu()
            finally:
                try:
                    user_two = self.usurper.temp_users[next_step]
                except KeyError:
                    print("your number is not in the list of users.")
                    self.new_private_menu()
                finally:
                    title = input("what is the title of your new conversation? \n>> ")
                    if title == "b":  # go back
                        print("going back.")
                        self.new_private_thread_menu()
                    elif title == "x":  # exit
                        print("goodbye.")
                        exit()
                    else:  # check entered username agains list of existing usernames.
                        self.threader.deserialize_threads()
                        for key, value in self.threader.thread_library.items():
                            if next_step == value["title"] and self.user_id in value["allowed_users"]:
                                print("thread title already taken!")
                                self.what_if_thread_name_is_taken()
                        # send all the stuff to generate a new private chirp thread.
                        self.thread_id = self.threader.generate_new_thread(title, (self.user_id, user_two))
                        print(self.threader.thread_library[self.thread_id]["title"] + ":")
                        self.chirper.generate_chirp_list(self.thread_id)
                        self.full_chirp_menu()

    def what_if_thread_name_is_taken(self):
        """
        Menu that runs if a user enters a thread title in new_public_thread_menu or new_private_thread_menu that is already taken (in the case of a private thread, only in the threads that include the current user). Requests input from the user and handles whether they would like to go back, see a list of threads to choose from, try again to create a new thread, or exit.
        Arguments: None
        """
        print("'b' to go back.\n'x' to exit.\n1. Choose from a list of created threads.\n2. Try creating a thread with a different name.")
        next_step = input(">> ")
        if next_step == "1":  # choose from a list of created threads.
            self.usurper.generate_threads_list()
            self.view_threads_menu()
        elif next_step == "2":  # try creating a new thread again.
            if self.public_or_private == "public":
                self.new_public_thread_menu()
            else:
                self.new_private_thread_menu()
        elif next_step == "b":  # go back.
            print("going back.")
            self.view_threads_menu()
        elif next_step == "x":  # exit.
            print("goodbye.")
            exit()
        else:  # error handle.
            print("command not found.")
            self.what_if_thread_name_is_taken()

# ########################################
# ######## VIEW CHIRPS ########
# ########################################

    def full_chirp_menu(self):
        """
        prints after view_full_chirp to ask whether the user would like to go back, exit, or add to the chirp thread.
        arguments: none
        """
        if len(self.user_name) > 0:
            next_step = input("1. add a new chirp to this thread.\n'b' to go back.\n'x' to exit.\n>> ")
        else:
            next_step = input("'b' to go back.\n'x' to exit.\n>> ")

        if next_step == "b":  # go back
            print("going back.")
            self.thread_id = ""
            if self.public_or_private == "public":
                self.threader.generate_public_threads_list()
            else:
                self.threader.generate_private_threads_list(self.user_id)
            self.view_threads_menu()

        elif next_step == "x":  # exit
            print("goodbye.")
            exit()

        elif next_step == "1":  # add a chirp
            if self.user_name is not None:
                self.add_to_chirp_menu()
            else:
                print("command not recognized.")  # to keep an un-logged in user from pressing 1 and finding a SECRET INROAD to chirping.
                self.chirp_thread_menu()

        else:
            print("command not recognized.")
            self.chirp_thread_menu()

# #############################
# ######## ADD CHIRP ########
# #############################

    def add_to_chirp_menu(self):
        """
        requests input from the user for a new chirp to add to the current thread. error handles. Runs as part of full_chirp_menu, automatically sends user ID and thread ID along with chirp text to chirper class.
        Arguments: none
        """
        chirp_to_add = input("'b' to go back.\n'x' to exit.\nchirp text: >> ")
        if chirp_to_add == "b":  # go back.
            print("going back.")
            self.chirp_thread_menu()
        elif chirp_to_add == "x":  # exit.
            print("goodbye.")
            exit()
        else:
            self.chirper.generate_new_chirp(self.user_name, self.thread_id, chirp_to_add)
        print(self.threader.thread_library[self.thread_id]["title"] + ":")
        self.chirper.generate_chirp_list(self.thread_id)
        self.full_chirp_menu()

if __name__ == '__main__':
    app = Birdyboard()
    print(app.unlogged_in_options)
    app.unlogged_in_menu()
