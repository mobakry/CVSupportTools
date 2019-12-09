'''
A function convert the Airbus ship detection challenge data to a standard CSV bounding box format.
The Airbus data is in run-length encoding format. We want a bounding box for each ship in our format.
If an image has no ships in it, it still gets a row in our CSV, but x0,y0,x1,y1, and class are empty.
If there is more than one ship per image, then each ship gets its own row (with the same image name) in our CSV format.
The ship dataset is huge, so I just copied over the first 220 images into the Airbus_ship folder which contains the images and the run length-encoded
annotation file.
'''
import numpy as np
import pandas
import cv2
from pandas import DataFrame
import argparse
import os


# Function to convert RLE format to pixels
def RLencToPixels(runs):
    p1 = []  # Run-start pixel locations
    p2 = []  # Run-lengths

    # Separate run-lengths and pixel locations into seperate lists
    x = str(runs).split(' ')
    i = 0
    for m in x:
        if i % 2 == 0:
            p1.append(m)
        else:
            p2.append(m)
        i += 1

    # Get all absolute pixel values
    pixels = []
    for start, length in zip(p1, p2):
        i = 0
        length = int(length)
        pix = int(start)
        while i < length:
            pixels.append(pix)
            pix += 1
            i += 1
    return pixels

# Function to draw bounding box around masked portion in binary image obtained from rle_encoded file
'''
-------Inputs---------
df : .csv file contains image masks in run-length encoding format
image_size : The size of the images
Class : Images class
output_path : the path where the output file will be saved
Return : .csv file contains bounds boxes in a standard format
'''
def BoxingBimg(df, image_size, Class, output_path):

    image_size = image_size.split('*')

    # columns
    image_names = []
    left_side = []
    upper_side = []
    right_side = []
    lower_side = []
    class_name = []

    # Iterate over dataframe
    for index, row in df.iterrows():

        pixels = RLencToPixels(df['EncodedPixels'][index])
        image_names.append(df['ImageId'][index])

        # constructing binary image from pixels
        img = np.zeros(int(image_size[0])*int(image_size[1]))  # Background (768 * 768)
        img[pixels] = 1  # mask
        img = np.reshape(img, (int(image_size[0]), int(image_size[1]))).T.astype('uint8') * 255

        # find contours and get the external one

        contours, hier = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:  # image has no ships
            left_side.append(' ')
            upper_side.append(' ')
            right_side.append(' ')
            lower_side.append(' ')
            class_name.append(' ')

        else:
            x, y, w, h = cv2.boundingRect(contours[0])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            left_side.append(x)
            upper_side.append(y)
            right_side.append(x + w)
            lower_side.append(y + h)
            class_name.append(args.Class)

    bounding_box = {'file': image_names, 'x0': left_side, 'y0': upper_side, 'x1': right_side, 'y1': lower_side,
                    'class': class_name}
    df = DataFrame(bounding_box, columns=['file', 'x0', 'y0', 'x1', 'y1', 'class'])

    df.to_csv(os.path.join(output_path,'output2.csv'), index=False, header=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('CSVpath', type=str, help='the rle CSV file path')
    parser.add_argument('Class', type=str, help='the object class name')
    parser.add_argument('ImageSize', type=str, help='Size of the images eg:768*768')
    parser.add_argument('OutPath', type=str, help='Output file path')

    args = parser.parse_args()

    df = pandas.read_csv(args.CSVpath)

    
    BoxingBimg(df, args.ImageSize, args.Class, args.OutPath)
