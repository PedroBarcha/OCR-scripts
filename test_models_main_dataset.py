#test all 25 models (produced from the k-folds) on the main dataset

import os
import subprocess
from shutil import copyfile

FOLDS=25
FOLDS_PATH="/home/banshee/Pictures/ocr-images/Database/training/tesseract/books/test" #no '/' in the end
MAIN_DATASET_PATH="/home/banshee/Pictures/ocr-images/Database/training/tesseract/books/main_dataset" #no '/' in the end
TESSDATA_PATH="/usr/local/share/tessdata" #no '/' in the end
TRAINING_LANGUAGE="old"

for k in range(1,FOLDS+1):
	
	#checks whether there exists already the trained data in TESSDATA_PATH
	#if so, remove it
	traineddata=TESSDATA_PATH+'/'+TRAINING_LANGUAGE+".traineddata"
	if os.path.exists(traineddata):
  	  	os.remove(traineddata)
  	#then adds the fold's model to tessdata
  	sauce=FOLDS_PATH+'/'+str(k)+"/training/tessdata/"+TRAINING_LANGUAGE+".traineddata"
  	copyfile(sauce,TESSDATA_PATH+'/'+TRAINING_LANGUAGE+".traineddata")

  	#OCR 
	os.chdir(MAIN_DATASET_PATH+'/'+str(k)) #cd to fold's dir
	subprocess.call("tesseractall "+TRAINING_LANGUAGE, shell=True)

  	#evaluation
  	subprocess.call("ocrevaluation tesseract groundtruth", shell=True)