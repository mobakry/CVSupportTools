'''
to use this file:
python multidownload file.csv x       ;as x is integer number refers to the number of threads to be created
'''



import pandas
import wget
from multiprocessing.dummy import Pool as ThreadPool
import argparse
import time

#calculate time as a measure to performance
start = time.time()

parser = argparse.ArgumentParser(description='')

parser.add_argument("CSVName", type=str, help='Csv file contains urls and outpaths')
parser.add_argument("--Threads", type=str, help='Number of threads(default = 2)')

args = parser.parse_args()

csv_name = args.CSVName
threads = int(args.Threads)


def download_image(li):
	wget.download(li[0],li[1])



def downloadparallel(li, threads=2):
	pool = ThreadPool(threads)
	pool.map(download_image, li)
	pool.close()
	pool.join()

if __name__ == "__main__":
	#list to hold url and path
	li = []
	#Read csv file and extract columns names
	df = pandas.read_csv(csv_name)
	column1 = df.columns[0]
	column2 = df.columns[1]

	#Create a list to be passed through threadpool.map
	for url,path in zip(df[column1], df[column2]):
		li.append([url,path])
	
	downloadparallel(li, threads)

	
	print('\nexcution time : {}'.format(time.time()-start))
