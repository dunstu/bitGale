from PIL import Image

imgReadOK = False
while not imgReadOK:
    try:
        imgDir = input("Path location of image to open:")
        userImg = Image.open(imgDir)
        imgReadOK = True
    except IOError:
        print("File not found!")

userImg.show()
