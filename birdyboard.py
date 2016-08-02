import pickle


class Birdyboard:

    def __init__(self):
        self.users = []
        self.user_name = None

        self.chirps_library = {"public": [], "private": []}
        # these variables are assigned when a specific chirp thread is being viewed or added to.
        self.public_or_private = ""
        self.chirp_index = None

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
        if next_step == "1":  # create a user.
            print("creating a new user.")
            self.create_a_user_menu()
        elif next_step == "2":  # log in to a current user.
            self.view_users_menu()
            self.users_menu_next_step()
        elif next_step == "3":  # view public chirps. Will not have the option of commenting.
            self.deserialize_chirps_library()
            self.public_or_private = "public"
            self.view_chirps()
            self.view_chirps_next_step()
        elif next_step == "x":  # exit.
            print("goodbye.")
            exit()
        else:
            print("command not found.")
            self.unlogged_in_menu_next_step()

# ##########################################
# ######## LOGGED IN TOP LEVEL MENU ########
# ##########################################

    def logged_in_menu_print(self):
        print("welcome " + self.user_name + "!")
        print("1. log out\n2. view public chirps\n3. view private chirps\n4. New public chirp thread\n5. new private chirp thread\n'x' to exit.\n")

    def logged_in_menu_next_step(self):
        next_step = input(">> ")
        if next_step == "1":  # log out
            print('logging out.')
            self.user_name = None
            self.unlogged_in_menu_print()
            self.unlogged_in_menu_next_step()
        elif next_step == "2":  # view public threads.
            self.deserialize_chirps_library()
            self.public_or_private = "public"
            self.view_chirps()
            self.view_chirps_next_step()
        elif next_step == "3":  # view private threads.
            self.public_or_private = "private"
            self.view_chirps_next_step()
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
        self.deserialize_users()
        user_name = input("user name: ")
        if user_name == "b":
            print("going back")
            self.unlogged_in_menu_print()
            self.unlogged_in_menu_next_step()
        elif user_name == "x":
            print("goodbye.")
            exit()
        else:
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
        print("'b' to go back.\n'x' to exit.\n1. Choose from a list of created users.\n2. Try creating a user with a different name.")
        next_step = input(">> ")
        if next_step == "1":
            self.deserialize_users()
            self.view_users_menu()
            self.users_menu_next_step()
        elif next_step == "2":
            self.create_a_user_menu()
        elif next_step == "b":
            print("going back.")
            self.unlogged_in_menu_print()
            self.unlogged_in_menu_next_step()
        elif next_step == "x":
            print("goodbye.")
            exit()
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
# I am fully aware that this is a completely insecure way to handle a password system.

    def view_users_menu(self):
        """
        prints a list of users (after deserialization) that are currently created on the app.
        Arguments: None
        """
        [print(str(self.users.index(user) + 1) + ". " + user["user_name"]) for user in self.users]

    def users_menu_next_step(self):
        """
        prints after 'view users menu'. creates input for which existing user is being selected and error handles.
        arguments: None
        """
        next_step = input("'b' to go back.\n'x' to exit.\nChoose a user to log into.\n>> ")
        if next_step == "b":
            print("going back.")
            self.unlogged_in_menu_print()
            self.unlogged_in_menu_next_step()
        elif next_step == "x":
            print("goodbye.")
            exit()
        else:
            try:
                next_step = int(next_step)
            except ValueError:
                print("you didn't enter a number.")
                self.users_menu_next_step()
            finally:
                # TODO: fix this. it doesn't work.
                try:
                    if int(next_step)-1 >= 0:
                        user_index = int(next_step)-1
                        self.enter_password(user_index)
                    else:
                        print("your number is not in the list of users.")
                        self.users_menu_next_step()
                except IndexError:
                    print("your number is not in the list of users.")
                    self.users_menu_next_step()
                finally:
                    pass

    def enter_password(self, user_index):
        """
        runs as part of users_menu_next_step. receives the index number error-handled by users_menu_next_step, receives user-input for a password and error handles that, and passes both into check_password to verify. if check_password returns true, takes you to the logged-in top-level menu. If it returns false, asks you again. Also gives you the option to go directly to the 'create new user' menu.

        Argument: integer value that represents the index of a user in the self.users list.
        """
        print("'x' to exit.\n'b' to go back.\n'n' to create new user.")

        password_try = input("password: ")
        if password_try == "b":
            print("going back.")
            self.view_users_menu()
            self.users_menu_next_step()
        elif password_try == "x":
            print("goodbye.")
            exit()
        elif password_try == "n":
            print("new user menu.")
            self.create_a_user_menu()
        else:
            verify = self.check_password(user_index, password_try)
            if verify is True:
                self.logged_in_menu_print()
                self.logged_in_menu_next_step()
            else:
                print("incorrect Password.")
                self.enter_password()

    def check_password(self, user_index, password_try):
        """
        runs as part of enter_password. receives the user index number passed through from users_menu_next_step and the password entered in enter_password, and checks to see if they are equal. if they are, assigns the user and returns 'true' to enter_password for continuation.

        Arguments: 1. integer value that represents the index of a user in the self.users list, and 2. string to check agains the password for the user with the matching index.

        """
        current_user = self.users[user_index]
        if password_try == current_user["password"]:
            print("logging in to " + current_user["user_name"] + ".")
            self.user_name = current_user["user_name"]
            return True
        else:
            return False

# ########################################
# ######## VIEW ALL CHIRPS ###############
# ########################################

    def view_chirps(self):
        """
        this function is called if the user chooses a 'view chirp' option in the top level menu. prints the first chirp of all chirp threads (either 'public' or 'private' depending on what the top-level public_or_private variable is set to), formatted to also show the user name, and print a readable index number for selection of 'view full chirp'.

        Arguments: none.
        """
        print("******" + self.public_or_private.upper() + " CHIRPS******")
        if len(self.chirps_library[self.public_or_private]) > 0:
            if self.public_or_private == "public":
                [print(str(self.chirps_library[self.public_or_private].index(chirp) + 1) + ". " + chirp[0][0] + ": " + chirp[0][1]) for chirp in self.chirps_library[self.public_or_private]]
                print("\n")
            elif self.public_or_private == "private":
                [print(str(self.chirps_library[self.public_or_private].index(chirp) + 1) + ". " + chirp["chirps"][0][0] + ": " + chirp["chirps"][0][1]) for chirp in self.chirps_library[self.public_or_private] if self.user_name in chirp["users"]]
        else:
            print("no " + self.public_or_private + " chirps yet!\n")

    def view_chirps_next_step(self):
        """
        menu that appears after all chirps are printed (view_chirps). Allows the user to view a full chirp thread based on the index, or to go back or exit.
        arguments: none
        """
        next_step = input("enter the number of the chirp you'd like to view the full thread for.\n'n' for new chirp thread.\n'b' to go back.\n'x' to exit.>> ")

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
            self.new_chirp_thread_menu()
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
            self.logged_in_menu_print()
            self.logged_in_menu_next_step()
        elif next_step == "x":
            print("goodbye.")
            exit()
        else:
            if self.public_or_private == "private":
                self.view_users_menu()
                self.private_chirp_thread_menu()
            else:
                formatted_chirp = [(self.user_name, next_step)]
                self.add_new_thread(formatted_chirp)
                self.view_chirps()
                self.view_chirps_next_step()

    def private_chirp_thread_menu(self):
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
                        self.logged_in_menu_print()
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
    app.unlogged_in_menu_print()
    app.unlogged_in_menu_next_step()
