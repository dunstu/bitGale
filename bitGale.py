from PIL import Image

def open_image():
    '''
    Prompt user for directory, open image file (if found) and return
    '''
    imgReadOK = False
    while not imgReadOK:
        try:
            imgDir = input("Path location of image to open:")
            userImg = Image.open(imgDir)
            imgReadOK = True
        except IOError:
            print("File not found!")
    return userImg
