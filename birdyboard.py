import pickle

# I'm going to start with everyone sharing one user, and have all tweets be public.


class Birdyboard:

    def __init__(self):
        self.user_name = "Megan"  # later I will set this to None and have the login menu reassign it.
        self.chirps_library = {}
        self.chirp_to_display = None

    # TODO: add a decorator here that will print a title heading so I can use it for both the logged in menu and the unlogged in menu?
    def unlogged_in_menu_print(self):
        """
        prints the choices for an unlogged-in user, at start of app. calls the unlogged_in_menu_next_step method to determine where to go next.
        Arguments: none
        """
        print("1. new user\n2. log in\n3. view public chirps\n'x' to exit.")

    def unlogged_in_menu_next_step(self):
        """
        requests input from an unlogged-in user as part of the unlogged-in menu. looking for one of the options printed in the unlogged_in_menu_print.
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
            # TODO: handle logging in.
        elif next_step == "x":
            print("goodbye.")
            exit()

    def view_chirps(self):
        print("******ALL CHIRPS******")
        if len(self.chirps_library["public"]) >0:
            [print(str(self.chirps_library["public"].index(chirp) + 1) + ". " + chirp[0][0] + ": " + chirp[0][1]) for chirp in self.chirps_library["public"]]
        else:
            print("no chirps yet!")

    def view_chirps_next_step(self):
        next_step = input("enter the number of the chirp you'd like to view the full thread for.\n'x' to go back.\n>> ")

        if next_step == "x":
            print("going back.")
            self.unlogged_in_menu_print()
            self.unlogged_in_menu_next_step()
        else:
            try:
                next_step == int(next_step)
            except ValueError:
                print("you didn't enter a number.")
                self.view_chirps_next_step()
            finally:
                try:
                    if int(next_step)-1 >= 0:
                        # TODO: grab whether or not this is a public or private one.
                        chirp_index = int(next_step)-1
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
        self.chirp_to_display = {"location": public_or_private, "index": chirp_index, "chirp list": self.chirps_library[public_or_private][chirp_index]}
        [print(chirp[0] + ": " + chirp[1]) for chirp in self.chirp_to_display["chirp list"]]

    def chirp_thread_menu(self):
        # TODO: add an 'add comment' option here.
        next_step = input("'x' to go back.\n>> ")

        if next_step == "x":
            print("going back.")
            self.chirp_to_display = None
            self.view_chirps()
            self.view_chirps_next_step()
        else:
            print("command not recognized.")
            self.go_back_from_tweet_thread()


    def new_chirp_menu(self):
        # TODO: handle private chirps.
        if self.chirp_to_display is not None:
            print("Add Chirp to thread:" + self.user_name)
        else:
            print("New Chirp Thread: " + self.user_name)
        chirp_to_add = input("chirp text: >> ")
        # add this chirp onto the public chirps list. deserialize if already not- you can add a new chirp without having viewed them, so just in case.
        self.deserialize_chirps_library()
        self.chirps_library["public"].append([(self.user_name, chirp_to_add)])
        self.serialize_chirps_library()
        self.view_chirps()
        self.view_chirps_next_step()

    def serialize_chirps_library(self):
        with open("chirps.txt", "wb+") as chirps:
            pickle.dump(self.chirps_library, chirps)

    def deserialize_chirps_library(self):
        # TODO: change default library to reflect the lack of messages in a more meaningful way. these are just test messages.
        # TODO: add a 'delete thread' option so I can get rid of these default messages?
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
