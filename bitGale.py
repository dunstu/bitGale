import cmd

import effects
import imgio


class bitGaleShell(cmd.Cmd):
    intro = 'Welcome to bitGale.\n'
    prompt = 'bitGale~~ '
    file = None
    imageArray = []

    def preloop(self):
        self.imageArray = imgio.make_pixel_array(imgio.open_image())

    def do_sort(self, rawInput):
        mode = rawInput
        self.imageArray = effects.pixel_sort(self.imageArray, mode)

    def do_rgboff(self, rawInput):
        mode, offset = rawInput.split()
        self.imageArray = effects.rgb_offset(self.imageArray, mode, int(offset))

    def do_save(self, rawInput):
        imgio.save_image(imgio.make_pil_image(self.imageArray))


if __name__ == '__main__':
    bitGaleShell().cmdloop()
