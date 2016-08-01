import pickle

# I'm going to start with everyone sharing one user, and have all tweets be public.


class Birdyboard:

    def __init__(self):
        self.user_name = "Megan"  # later I will set this to None and have the login menu reassign it.
        self.public_chirps = []
        self.chirp_to_display = None

    # TODO: add a decorator here that will print a title heading so I can use it for both the logged in menu and the unlogged in menu?
    def unlogged_in_menu_print(self):
        """
        prints the choices for an unlogged-in user, at start of app. calls the unlogged_in_menu_next_step method to determine where to go next.
        Arguments: none
        """
        print("1. view chirps\n2. new chirp (public)\n'x' to exit.")

    def unlogged_in_menu_next_step(self):
        """
        requests input from an unlogged-in user as part of the unlogged-in menu. looking for one of the options printed in the unlogged_in_menu_print.
        Arguments: none
        """
        next_step = input(">> ")

        if len(next_step) > 1:
            print("you only need to type one character!")
            self.unlogged_in_menu_next_step()
        elif next_step not in ["1", "2", "x"]:
            print("please choose one of the options shown above.")
            self.unlogged_in_menu_next_step()
        elif next_step == "1":
            self.unlogged_in_view_chirps()
            self.view_chirps_next_step()
        elif next_step == "2":
            # TODO: remove this from options, I don't want people chirping without true login.
            self.unlogged_in_new_chirp()
            # TODO: handle logging in.
        elif next_step == "x":
            print("goodbye.")
            exit()

    def unlogged_in_view_chirps(self):
        # load the 'chirps' .txt file.
        self.all_chirps = self.deserialize_chirps_library()
        # assign the public part of the .txt file to an object.
        self.public_chirps = self.all_chirps["public"]
        # print the first chirp in the public list for each public thread.
        # formatted.
        [print(str(self.public_chirps.index(chirp) + 1) + ". " + chirp[0][0] + ": " + chirp[0][1]) for chirp in self.public_chirps]

    def view_chirps_next_step(self):
        next_step = input("enter the number of the chirp you'd like to view the full thread for.\n'x' to go back.\n>> ")

        if next_step == "x":
            print("going back.")
            self.unlogged_in_menu_print()
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
                        self.view_full_chirp(chirp_index)
                        self.go_back_from_tweet_thread()
                    else:
                        print("your number is not in the list of chirps.")
                        self.view_chirps_next_step()
                except IndexError:
                    print("your number is not in the list of chirps.")
                    self.view_chirps_next_step()
                finally:
                    pass

    def view_full_chirp(self, chirp_index):
        self.chirp_to_display = self.public_chirps[chirp_index]
        [print(chirp[0] + ": " + chirp[1]) for chirp in self.chirp_to_display]

    def go_back_from_tweet_thread(self):
        next_step = input("'x' to go back.\n>> ")

        if next_step == "x":
            print("going back.")
            self.chirp_to_display = None
            self.unlogged_in_view_chirps()
        else:
            print("command not recognized.")
            self.go_back_from_tweet_thread()

    def deserialize_chirps_library(self):
        # TODO: change default library to reflect the lack of messages in a more meaningful way. these are just test messages.
        # TODO: add a 'delete thread' option so I can get rid of these default messages?
        try:
            with open('chirps.txt', 'rb') as chirps:
                chirp_library = pickle.load(chirps)

        except FileNotFoundError:
                chirp_library = {"public": [[("username", "sample_text")]]}
        except EOFError:
                chirp_library = {"public": [[("username", "sample text"), ("another_username", "more sample text.")], [("username", "second thread"), ("username", "second thread second message.")]]}
        return chirp_library


if __name__ == '__main__':
    app = Birdyboard()
    app.unlogged_in_menu_print()
    # I've separated out the input so I can re-run it alone for easier error handling.
    app.unlogged_in_menu_next_step()
