import math
import os,glob,random
from shutil import copy
FOLDS=40
BOOKS=11
#path expected to have #books directories, each with the images+groundtruths
SOURCE_PATH="/home/banshee/Pictures/ocr-images/Database/training/tesseract/books"
DESTINATION_PATH="/home/banshee/Pictures/ocr-images/Database/training/tesseract/books/test"

#makes a pretty folded tree
def mkdir(FOLDS):
	for k in range (1, FOLDS+1):
		path=DESTINATION_PATH+'/'+str(k)
		#creates k
		if not os.path.exists(path):
    			os.makedirs(path)
		#creates train,test and cv dirs in k dir if they dont exist
		if not os.path.exists(path+"/training"):
  	  		os.makedirs(path+"/training")
		if not os.path.exists(path+"/test"):
   	 		os.makedirs(path+"/test")
   		#if not os.path.exists(path+"/cv"): #cross-validation set
   	 	#	os.makedirs(path+"/cv")

   	return


mkdir(FOLDS)

#for each fold
for k in range (1,FOLDS+1):
   	#for each book
	for dir in range (1,BOOKS+1):
		num_pages=0
		pages=[]
		os.chdir(SOURCE_PATH+'/'+str(dir))

		#creates list containing the name of the gt files (without extention)
		for file in glob.glob("*.box"):
			num_pages+=1
			pages.append(file.replace(".box",""))

		#training set = 60% of the pages
		num_training=int(math.ceil((3.0*num_pages)/5))
		for i in range (0,num_training):
			idx=random.randrange(0,num_pages)
			copy(pages[idx]+".box", DESTINATION_PATH+'/'+str(k)+"/training")
			copy(pages[idx]+".tiff", DESTINATION_PATH+'/'+str(k)+"/training")
			pages.pop(idx)
			num_pages-=1

		for i in range (0,num_pages):
			copy(pages[i]+".box", DESTINATION_PATH+'/'+str(k)+"/test")
			copy(pages[i]+".tiff", DESTINATION_PATH+'/'+str(k)+"/test")
