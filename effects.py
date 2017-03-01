import random


def pixel_sort(array, flags):
    '''
    Pixelsorting effect taking an image array, and the mode. Uses variation on merge sort algorithm
    Inputs: image - image array | mode - either sort by 'R', 'G', 'B' or 'C' (for combined average)
            direction - either 'up', 'down', 'left, 'right'
    '''
    # todo direction (lowest-highest, up/down, etc)

    # Interpret mode flag
    if 'm' in flags:
        # 3 is not handled as an index, but is looked for as a special mode in merge()
        index = 0 if flags['m'] == 'r' else 1 if flags['m'] == 'g' else 2 if flags['m'] == 'b' else 3
    else:
        index = 3

    # Interpret threshold flag
    threshold = int(flags['t']) if 't' in flags else 255 // 2

    # Function definitions for merge sort and getting sections
    def merge(left, right, index):
        result = []
        l = 0  # pointer to the left list
        r = 0  # pointer to the right list
        while l < len(left) and r < len(right):
            # Sort based on average of RGB values
            if index == 3:
                avgR = (left[l][0] + left[l][1] + left[l][2]) / 2
                avgL = (right[r][0] + right[r][1] + right[r][2]) / 2
                if avgR <= avgL:
                    result.append(left[l])
                    l += 1
                else:
                    result.append(right[r])
                    r += 1
            # Sort based on R(0), G(1), or B(2)
            else:
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
        if len(list) in [1, 0]:
            return list

        mid = len(list) // 2
        left = merge_sort(list[:mid], index)
        right = merge_sort(list[mid:], index)
        return merge(left, right, index)

    def get_threshold_breakpoints(array, index, threshold):
        allSections = []

        for y in range(len(array)):  # Run through the rows of the image
            noneOver = True  # This flag handles when a whole rule is under
            section = [0]  # Section is the current row's list of 'breakpoint' indices

            for x in range(1, len(array[y])):  # Run through the row, starting at the second pixel to avoid out of range
                # Calculate the value of the pixel. Index=3 is the combined average brightness, else use single channel
                pixel = (array[y][x][0] + array[y][x][1] + array[y][x][2]) / 3 if index == 3 else array[y][x][index]
                # Same, but for the pixel before.
                lastPixel = (array[y][x - 1][0] + array[y][x - 1][1] + array[y][x - 1][2]) / 3 if index == 3 else array[y][x - 1][index]

                if pixel > threshold:  # Ensures that if all pixels are under threshold, the row is sorted, not ignored
                    noneOver = False

                # If the current pixel is below, but the last was above the threshold, mark as a threshold breakpoint
                if pixel <= threshold < lastPixel:
                    section.append(x)
                elif pixel > threshold >= lastPixel:  # Similarity, mark if this pixel is above and the last below
                    section.append(x)

            if noneOver is True:  # If all pixels were below the threshold, set breakpoints to the edges of the image
                section.append(len(array[y])-1)

            allSections.append(section)  # Append this list of breakpoints to the master list to be returned

        return allSections

    sections = get_threshold_breakpoints(array, index, threshold)

    # Run through the rows of the image and the rows of the sections (Since they are the same length, this does both)
    for row in range(len(array)):
        zones = range(0, len(sections[row]) - 1, 2)  # Get the zones to sort for this row
        for edge in zones:  # Run through each zone
            # Set that zone equal to the sorted version of that row
            array[row][sections[row][edge]:sections[row][edge + 1]] = merge_sort(array[row][sections[row][edge]:sections[row][edge + 1]], index)
    return array


def rgb_offset(array, flags):
    '''
    Offsets a colour channel by a given magnitude in an array
    Inputs: c - channel to offset (either 'r', 'g', 'b') | d - displacement (0 < offset <= width of image)
    Returns: an array in the form [[(r, g, b), (r2, g2, b2)...][...]...]
    '''
    # Interpret mode flag as the index to operate on in each pixel
    if 'c' in flags:
        channel = 0 if flags['c'] == 'r' else 1 if flags['c'] == 'g' else 2 if flags['c'] == 'b' else 0
    else:
        channel = 0

    # Interpret offset flag as offset distance, and protect against non-int values
    if 'd' in flags:
        try:
            offset = int(flags['d'])
        except ValueError:
            print('*** Displacement not an integer!')
            return array

        # Check to see if the offset is greater than the width of the image (anything larger is invalid)
        if offset >= len(array[0]):
            print("Displacement wider than image, choose a smaller displacement!")
            return array
    else:
        offset = 1

    # Take 'offset' number of pixels and bubble them to the end of the row
    for y in range(len(array) - 1):
        for x in range(0, len(array[y]) - offset - 1, 1):
            array[y][x][channel], array[y][x+offset][channel] = array[y][x+offset][channel], array[y][x][channel]

        # Switch the last 'offset' number of pixel(s) in the current row with the first 'offset' number of pixel(s) in
        # the next row. (This code just handles the last few pixels so not to cause out of index error
        nextPixel = 0
        for endPixel in range(len(array[y]) - offset, len(array[y]), 1):
            array[y][endPixel][channel], array[y+1][nextPixel][channel] = array[y+1][nextPixel][channel], array[y][endPixel][channel]
            nextPixel += 1

    # This does the same as above for the last row without switching with the next row, to prevent Index out of range
    for x in range(0, len(array[y]) - offset - 1, 1):
        array[-1][x][channel], array[-1][x + offset][channel] = array[-1][x + offset][channel], array[-1][x][channel]
    return array


def row_shift(array, flags):
    # Interpret the max displacement
    try:
        displacementMax = int(flags['d']) if 'd' in flags else 10
    except ValueError:
        print('*** Displacement not an integer!')
        return array

    # Generate random indices that will act as the dividers between rows for offset 'sections'. Max
    indices = sorted([random.randint(0, len(array)) for num in range(random.randint(1, 10))])

    # Run through every other section of rows
    for edge in range(0, len(indices)-1, 2):
        # Interpret the shift direction
        direction = 'l->r' if random.randint(0, 1) == 0 else 'r->l'

        # Get a distance to displace for this section
        amount = random.randint(0, displacementMax)

        # Run through each row in that section
        for y in range(indices[edge], indices[edge+1]):
            # Set direction to run through the pixels in each row
            run = range(0, len(array[y])-amount-1, 1) if direction == 'l->r' else range(len(array[y])-1, amount, -1)
            for x in run:  # Bubble 'amount' number of pixels to the end
                if direction == 'l->r':
                    array[y][x], array[y][x+amount] = array[y][x+amount], array[y][x]
                else:
                    array[y][x], array[y][x-amount] = array[y][x-amount], array[y][x]
    return array
