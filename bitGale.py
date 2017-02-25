import cmd

import effects
import imgio


class bitGaleShell(cmd.Cmd):
    intro = "Welcome to bitGale. Type 'help' for general help, or 'quit' to exit the program.\n"
    prompt = 'bitGale~: '
    file = None
    imageArray = []
    savedLastChange = False

    def preloop(self):
        self.imageArray = imgio.make_pixel_array(imgio.open_image())

    def do_help(self, rawInput):
        helpFile = None if rawInput == '' else imgio.parse(rawInput)
        imgio.show_help(helpFile)

    def do_sort(self, rawInput):
        flags = imgio.parse(rawInput)
        self.imageArray = effects.pixel_sort(self.imageArray, flags)
        self.savedLastChange = False

    def do_rgboff(self, rawInput):
        flags = imgio.parse(rawInput)
        self.imageArray = effects.rgb_offset(self.imageArray, flags)
        self.savedLastChange = False

    def do_save(self, rawInput):
        imgio.save_image(imgio.make_pil_image(self.imageArray))
        self.savedLastChange = True

    def do_show(self, rawInput):
        imgio.make_pil_image(self.imageArray).show()

    def do_quit(self, rawInput):
        while not self.savedLastChange:  # If effects have been applied since last save, ask user to save
            okToQuit = input("You have some unsaved changes. Do you still want to quit?(y,n)")
            if okToQuit == 'y':
                print("Exiting bitGale...")
                return True
            else:
                print('Returning to shell.')
                return False

if __name__ == '__main__':
    bitGaleShell().cmdloop()
