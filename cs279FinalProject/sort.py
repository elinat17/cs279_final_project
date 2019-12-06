import re 
import os
import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.ndimage import label, generate_binary_structure
import collections 
from shutil import copyfile

def contour_files(dir): 
	filenames = []
	for filename in os.listdir(dir):
	    if filename.endswith('.contour'):
	       filenames.append(os.path.join(dir, filename))
	return filenames

def newmaxdir(files): 
	namedict = {} 

	for file in files:
		index = file.find('-') 
		start = file[:index]
		if start not in namedict: 
			namedict[start] = file 
		else: 
			currfilename = namedict[start] 
			currNumIndex = currfilename.find('-')
			currnum = currfilename[currNumIndex:-8]
			newnum = file[index:-8]
			if newnum > currnum: 
				namedict[start] = file 
	filelist = [] 
	for names in namedict: 
		filelist.append(namedict[names])
	return filelist 



usage = "Usage: python sort.py <path to dir> <path to new dir>"

if len(sys.argv) < 2:
  print (usage)
  exit(1)
folder = sys.argv[1]
path = sys.argv[2] 
files = contour_files(folder) 
newfiles = newmaxdir(files) 
os.makedirs(path)
for filename in newfiles:
	dest = path + filename[12:]
	copyfile(filename,dest) 

	# add to the new directory 




