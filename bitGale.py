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

def pixel_sort(image, mode):
    '''
    Inputs: image - image array | mode - either sort by 'R', 'G', 'B' or 'C' (for combined average)
            direction - either 'up', 'down', 'left, 'right'
    '''
    # todo direction (lowest-highest, up/down, etc)

    # Function definitions for merge sort
    def merge(left, right, index):
        result = []
        l = 0  # pointer to the left list
        r = 0  # pointer to the right list
        while l < len(left) and r < len(right):
            if index == 3:  # Sort based on weighted average of RGB
                avgR = (left[l][0] + left[l][1] + left[l][2]) / 2
                avgL = (right[r][0] + right[r][1] + right[r][2]) / 2
                if avgR <= avgL:
                    result.append(left[l])
                    l += 1
                else:
                    result.append(right[r])
                    r += 1
            else:  # Sort based on R, G, or B
                if left[l][index] <= right[r][index]:
                    result.append(left[l])
                    l += 1
                else:
                    result.append(right[r])
                    r += 1
        result += left[l:]
        result += right[r:]
        return result

    def merge_sort(list, index):
        if len(list) in [1, 0]:  # Handles trivial case
            return list
        mid = len(list) // 2
        left = merge_sort(list[:mid], index)
        right = merge_sort(list[mid:], index)
        return merge(left, right, index)

    index = 0 if mode == 'R' else 1 if mode == 'G' else 2 if mode == 'B' else 3  # 3 is handled as a special case
    sortedImage = []
    for row in image:
        sortedImage.append(merge_sort(row, index))
    return sortedImage


def main():
    # Testing space ... for now!
    userImage = open_image()
    print(userImage[0])
    userImageSorted = pixel_sort(userImage, 'R')
    print(userImageSorted[0])

main()
