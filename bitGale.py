import cmd

import effects
import imgio


class bitGaleShell(cmd.Cmd):
    intro = "Welcome to bitGale. Type 'help' for general help, or 'quit' to exit the program.\n"
    prompt = 'bitGale~: '
    file = None
    imageArray = []

    def preloop(self):
        self.imageArray = imgio.make_pixel_array(imgio.open_image())

    def do_help(self, rawInput):
        helpFile = None if rawInput == '' else imgio.parse(rawInput)
        imgio.show_help(helpFile)

    def do_sort(self, rawInput):
        flags = imgio.parse(rawInput)
        self.imageArray = effects.pixel_sort(self.imageArray, flags)

    def do_rgboff(self, rawInput):
        flags = imgio.parse(rawInput)
        self.imageArray = effects.rgb_offset(self.imageArray, flags)

    def do_save(self, rawInput):
        imgio.save_image(imgio.make_pil_image(self.imageArray))

    def do_show(self, rawInput):
        imgio.make_pil_image(self.imageArray).show()

if __name__ == '__main__':
    bitGaleShell().cmdloop()
