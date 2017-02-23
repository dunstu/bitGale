import effects
import imgio


def main():
    # Testing space ... for now!
    #userImage = open_image()
    #print(userImage[0])
    #userImageSorted = pixel_sort(userImage, 'G')
    #print(userImageSorted[0])

    userImage = imgio.open_image()
    userImageArray = imgio.make_pixel_array(userImage)

    userImageArray = effects.rgb_offset(effects.rgb_offset(userImageArray, 'r', 10), 'g', 20)
    #userImageArray = effects.pixel_sort(userImageArray)
    imgio.save_image(imgio.make_pil_image(userImageArray))

main()
