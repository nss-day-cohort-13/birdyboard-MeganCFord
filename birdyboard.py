import pickle

# I'm going to start with everyone sharing one user, and have all tweets be public.


class Birdyboard:

    def __init__(self):
        self.user_name = "Megan"  # later I will set this to None and have the login menu reassign it.
        self.public_chirps = list

    # TODO: add a decorator here that will print a title heading so I can use it for both the logged in menu and the unlogged in menu?
    def unlogged_in_menu_print(self):
        """
        prints the choices for an unlogged-in user, at start of app. calls the unlogged_in_menu_next_step method to determine where to go next.
        Arguments: none
        """
        print("welcome.\n1. view chirps\n2. new chirp (public)")
        #  I've separated out the input so I can re-run it alone for easier error handling.
        self.unlogged_in_menu_next_step()

    def unlogged_in_menu_next_step(self):
        """
        requests input from an unlogged-in user as part of the unlogged-in menu. looking for one of the options printed in the unlogged_in_menu_print.
        Arguments: none
        """
        next_step = input(">> ")
        if len(next_step) > 1:
            print("you only need to type one character!")
            self.unlogged_in_menu_next_step()
        elif next_step not in ["1", "2"]:
            print("please choose one of the options shown above.")
            self.unlogged_in_menu_next_step()
        elif next_step == "1":
            self.unlogged_in_view_chirps()
        elif next_step == "2":
            # TODO: remove this from options, I don't want people chirping without true login.
            self.unlogged_in_new_chirp()

    def unlogged_in_view_chirps(self):
        # load the 'chirps' .txt file. Do I want to run this in an init?
        self.all_chirps = self.deserialize_chirps_library()
        # assign the public part of the .txt file to an object.
        self.public_chirps = self.all_chirps["public"]
        # print the first chirp in the public list for each public thread.
        [print(chirp[0]) for chirp in self.public_chirps]
        # uh, I need to format this.
        # assign some kind of value to them, so that the user can access the full list.
        # go back option sends back to unlogged in menu print.

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

    def unlogged_in_view_full_tweet(self):
        pass
        # grab the value of the thread that the user chose. Do I want to assign it a value in the .txt, like as a dictionary?
        # print all the messages in the thread.
        # do not allow for new tweets- simply a go back option which sends back to view chirps.

if __name__ == '__main__':
    app = Birdyboard()
    app.unlogged_in_menu_print()
