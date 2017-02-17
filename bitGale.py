from PIL import Image

def open_image():
    '''
    Prompt user for directory, open image file (if found) and return as an array
    Directory for testing: D:\PyCharm\Projects\bitGale\testImg.jpg
    '''
    imgReadOK = False
    while not imgReadOK:
        try:
            # imgDir = input("Path location of image to open:")  # Commented out for testing purposes
            imgDir = 'D:\\PyCharm\\Projects\\bitGale\\testImg.jpg'
            userImg = Image.open(imgDir)
            imgReadOK = True
        except IOError:
            print("File not found!")

        rawPixels = list(userImg.getdata())
        width, height = userImg.size
        imgAsArray = [rawPixels[i * width:(i + 1) * width] for i in range(height)]
    return imgAsArray


def main():
    userImage = open_image()

main()
