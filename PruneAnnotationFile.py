'''
Functionality:

The program opens up the CSVpath file and iterates through each row. For any filename that is not in the
imagesPath directory (or subdirectory within) that row is discarded from teh outputFile. So the output
is a CSV that is same as the input CSV but with rows removed if teh images don't exist.

Inputs:

str CSVpath (which is the annotation CSV file path)

str imagesPath (which is the root path to a directory full of images and subdirectories)

str outputFile (which is the output CSV file name)

to run the function
python PruneAnnotationFile.py path/to/annotations.csv path/to/ImagesDir out.csv

'''
import pandas
import os
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('CSVpath', type=str, help='the annotation CSV file path')
parser.add_argument('imagesPath', type=str, help='the root path to a directory full of images and subdirectories')
parser.add_argument('outputFile', type=str, help='the output CSV file name')

parser.set_defaults(includeBackgrounds=False)
args = parser.parse_args()


cdir = args.imagesPath
df = pandas.read_csv(args.CSVpath)

image_names = []
for r,d,f in os.walk(cdir):
	for image in f:
		if image.endswith('.jpg'):
			image_names.append(image)
for index, row in df.iterrows():
	image = os.path.basename(df['file'][index])
	if not(image in image_names):
		df = df.drop([index], axis=0)
df.to_csv(args.outputFile, index=False)
