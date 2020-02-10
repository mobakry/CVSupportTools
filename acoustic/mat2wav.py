'''
This file converts audio files from ,amt format to .wav files

to use:
python mat2wav path/to/.matfiles path/to/outfiles
'''

import scipy.io as sio
import numpy as np
import os
from scipy.io.wavfile import write, read
import argparse


parser = argparse.ArgumentParser(description='')

parser.add_argument("FilesPath", type=str, help = 'Path to a directory contains .mat files')
parser.add_argument("OutPath", type=str, help = 'Path to output file')

args = parser.parse_args()

files_path = args.FilesPath
out_path = args.OutPath

for r,d,f in os.walk(files_path):
	for file in f:
		if file.endswith('.mat'):
			print(file)
			mat_contents = sio.loadmat(os.path.join(files_path,file))
			file_name = os.path.splitext(file)[0]
			np_file = mat_contents[file_name] 

			write(os.path.join(out_path,file_name+'.wav'), 650000, np_file)
			
