

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
        self.user_name = "Megan"  # later I will set this to None and have the login menu reassign it.
        self.chirps_library = {"public": [], "private": []}
        self.current_chirp= None

    # TODO: add a decorator here that will print a title heading so I can use it for both the logged in menu and the unlogged in menu?
    def unlogged_in_menu_print(self):
        """
        prints the choices for an unlogged-in user, at start of app.
        Arguments: none
        """
        print("1. new user\n2. log in\n3. view public chirps\n'x' to exit.")

    def unlogged_in_menu_next_step(self):
        """
        requests input for top level menu functionality while the user is not logged in. Currently does not do anything for user login. secret fourth option to add a chirp but later that will be only an option if you're logged in.
        Arguments: none
        """
        next_step = input(">> ")

        if len(next_step) > 1:
            print("you only need to type one character!")
            self.unlogged_in_menu_next_step()
        elif next_step not in ["1", "2", "3", "4", "x"]:
            print("please choose one of the options shown above.")
            self.unlogged_in_menu_next_step()
        elif next_step == "3":
            self.deserialize_chirps_library()
            self.view_chirps()
            self.view_chirps_next_step()
        elif next_step == "4":
            # TODO: remove this from options, I don't want people chirping without true login.
            self.new_chirp_menu()
        elif next_step == "x":
            print("goodbye.")
            exit()
            # TODO: handle these two.
        elif next_step == "1":
            print('create a user page will show up here.')
            self.unlogged_in_menu_next_step()
        elif next_step == "2":
            print('log in to a current user will show up here.')
            self.unlogged_in_menu_next_step()

    def view_chirps(self):
        """
        this function is called if the user presses "3" on the unlogged-in menu, after deserialization. prints the first chirp of all public chirp threads, formatted to also show the user name, and print a readable index number for selection of 'view full chirp'.
        Arguments: none.
        """
        print("******ALL CHIRPS******")
        if len(self.chirps_library["public"]) > 0:
            print("PUBLIC:")
            [print(str(self.chirps_library["public"].index(chirp) + 1) + ". " + chirp[0][0] + ": " + chirp[0][1]) for chirp in self.chirps_library["public"]]
            print("\n")
        else:
            print("no public chirps yet!")
            print("\n")
        # TODO: print the private chirps.

    def view_chirps_next_step(self):
        """
        menu that appears after all chirps are printed (view_chirps). Allows the user to view a full chirp thread based on the index, or to go back or exit.
        arguments: none
        """
        next_step = input("enter the number of the chirp you'd like to view the full thread for.\n'b' to go back.\n'x' to exit.>> ")

        if next_step == "b":
            print("going back.")
            self.unlogged_in_menu_print()
            self.unlogged_in_menu_next_step()
        elif next_step == "x":
            print("goodbye.")
            exit()
        else:
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
                        self.view_full_chirp("public", chirp_index)
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
            self.view_chirps()
            self.view_chirps_next_step()
        elif next_step == "1":
            self.new_chirp_menu()
        elif next_step == "b":
            print("goodbye.")
            exit()


    def new_chirp_menu(self):
        """
        UNFINISHED, will probably break out at a higher level. Currently, runs when '1' is chosen in chirp_thread_menu, or when option 4 is chosen in top level menu to start a new thread. either adds a completely new chirp thread with one item in it, or appends a chirp to an existing thread.
        Arguments: none
        """
        # TODO: handle private chirps.
        if self.current_chirp is not None:

            if self.current_chirp["location"] == "public":
                # TODO: nest the adding chirp into a further menu so you can view a thread without having to add to it.
                chirp_to_add = input("'b' to go back.\n'x' to exit.\nchirp text: >> ")
                if chirp_to_add == "b":
                    print("going back.")
                elif chirp_to_add == "x":
                    print("goodbye.")
                    exit()
                else:
                    self.chirps_library["public"][self.current_chirp["index"]].append((self.user_name, chirp_to_add))
                    self.serialize_chirps_library()
                    self.chirp_to_display = None
                self.view_full_chirp(self.current_chirp["location"], self.current_chirp["index"])
                self.chirp_thread_menu()
                # TODO: handle private tweeting.
            elif self.current_chirp["location"] == "private":
                print("private chirps will go here.")
                self.chirp_thread_menu()
        else:
            print("'b' to go back.\n'x' to exit.\n******NEW CHIRP THREAD:******")
            chirp_to_add = input("\nchirp text: >> ")
            if chirp_to_add == "b":
                print("going back.")
            elif chirp_to_add == "x":
                print("goodbye.")
                exit()
            else:
                self.deserialize_chirps_library()
                self.chirps_library["public"].append([(self.user_name, chirp_to_add)])
                self.serialize_chirps_library()
        self.view_chirps()
        self.view_chirps_next_step()

    def serialize_chirps_library(self):
        """
        saves new chirps to the chirps.txt file.
        Arguments: none
        """
        with open("chirps.txt", "wb+") as chirps:
            pickle.dump(self.chirps_library, chirps)

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


if __name__ == '__main__':
    app = Birdyboard()
    app.unlogged_in_menu_print()
    app.unlogged_in_menu_next_step()
