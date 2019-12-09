'''
Functionality:

The programm takes in image masks and calculates the bounding box around the masked portion.
In folder called masks you will find black and white images. It is these white mask areas
we are going to to calculate the smallest containing bounding box for.

Inputs:
 str imagesPath : the root path to a directory full of image masks
 str Class 	: the object class name
 
 
to run the function
python CalcBoundingBox.py path/to/images class_name
'''

import cv2
import numpy as np
import os
from pandas import DataFrame
import argparse

'''
'x0 is :' :['left  side of bounding box in pixels'],
'y0 is :' :['upper  side of bounding box in pixels'], 
'x1 is :' :['right  side of bounding box in pixels'], 
'y1 is :' :['lower  side of bounding box in pixels'],
'class is :' :['object class name']  
'''

def calc_BounBox(path,Class_name):
	image_names = []
	left_side=[]
	upper_side=[]
	right_side=[]
	lower_side=[]
	class_name=[]
	for r,d,f in os.walk(path):
		for image in f:
			if image.endswith(('.jpg', '.png', '.ttif')):
				image_names.append(os.path.join(path,image))
				img = cv2.imread(os.path.join(path,image))
				
				ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
		            127, 255,0)
				# find contours and get the external one

				contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

				c = contours[0]

				x,y,w,h = cv2.boundingRect(c)
				cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)

				left_side.append(x)
				upper_side.append(y)
				right_side.append(x+w)
				lower_side.append(y+h)
				class_name.append(Class_name)
				cv2.imshow("contours", img)
				cv2.waitKey(0)

				cv2.destroyAllWindows()
	bounding_box = {'file':image_names, 'x0':left_side, 'y0': upper_side, 'x1': right_side, 'y1': lower_side, 'class':class_name}
	df = DataFrame(bounding_box, columns=['file','x0','y0','x1','y1','class'])
	df.to_csv('output2.csv',index=False, header=True)
	
	

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('imagesPath', type=str, help='the root path to a directory full of image masks')
	parser.add_argument('Class', type=str, help='the object class name')

	parser.set_defaults(includeBackgrounds=False)
	args = parser.parse_args()


	path = args.imagesPath
	Class_name = args.Class 
	calc_BounBox(path,Class_name)
