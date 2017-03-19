import cmd

from PIL import Image

import effects
import imgio


class bitGaleShell(cmd.Cmd):
    intro = "Welcome to bitGale. Type 'help' for general help, or 'quit' to exit the program.\n"
    prompt = 'bitGale~: '
    file = None
    fullImage = Image.new('RGB', (0, 0))
    imageArray = []
    savedLastChange = False
    history = []

    def preloop(self):
        self.fullImage = imgio.open_image()
        self.imageArray = imgio.make_pixel_array(self.fullImage)

    def do_help(self, rawInput):
        validFlags = ['eff']
        # Empty dict here just makes the help function default to general help
        helpFile = {} if (rawInput == '' or rawInput == '?') else imgio.parse(rawInput, validFlags)
        imgio.show_help(helpFile)

    def do_sort(self, rawInput):
        validFlags = ['mode', 'thr', 'dir']
        flags = imgio.parse(rawInput, validFlags)
        if flags is not 'invalid':
            self.history.append(['sort', flags])
            self.imageArray = effects.pixel_sort(self.imageArray, flags)
            self.savedLastChange = False

    def do_rgboff(self, rawInput):
        validFlags = ['cnl', 'dis']
        flags = imgio.parse(rawInput, validFlags)
        if flags is not 'invalid':
            self.history.append(['rgboff', flags])
            self.imageArray = effects.rgb_offset(self.imageArray, flags)
            self.savedLastChange = False

    def do_rowshift(self, rawInput):
        validFlags = ['dis']
        flags = imgio.parse(rawInput, validFlags)
        if flags is not 'invalid':
            self.history.append(['rowshift', flags])
            self.imageArray = effects.row_shift(self.imageArray, flags)
            self.savedLastChange = False

    def do_eextend(self, rawInput):
        validFlags = ['dir', 'dis']
        flags = imgio.parse(rawInput, validFlags)
        if flags is not 'invalid':
            self.history.append(['rowshift', flags])
            self.imageArray = effects.edge_extend(self.imageArray, flags)
            self.savedLastChange = False

    def do_rotate(self, rawInput):
        validFlags = ['ang']
        flags = imgio.parse(rawInput, validFlags)
        if flags is not 'invalid':
            self.history.append(['rotate', flags])
            self.imageArray = imgio.rotate_image(self.imageArray, flags)
            self.savedLastChange = False

    def do_save(self, rawInput):
        imgio.save_image(imgio.make_pil_image(self.imageArray))
        self.savedLastChange = True

    def do_show(self, rawInput):
        imgToDisplay = imgio.make_pil_image(self.imageArray)
        imgToDisplay.show()
        self.imageArray = imgio.make_pixel_array(imgToDisplay)

    def do_quit(self, rawInput):
        while not self.savedLastChange:  # If effects have been applied since last save, ask user to save
            okToQuit = input("You have some unsaved changes. Do you still want to quit?(y/n)")
            if okToQuit == 'y':
                print("Exiting bitGale.")
                return True
            else:
                print('*** Returning to shell.')
                return False

if __name__ == '__main__':
    bitGaleShell().cmdloop()
