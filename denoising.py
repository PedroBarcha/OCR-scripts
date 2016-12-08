import numpy as np
import os,glob
import cv
from scipy import misc,ndimage,signal
import matplotlib.pylab as plt
from skimage import restoration as rt
from skimage.filters import rank
import time

#Apply diverse noise filters for different kinds of noises.
#The filter is applied for every image of imgType in the directories
#specified in input/outputPath

def denoise (im,method,filename): 
	if (method=="bilateral"): #applied for speckle/gaussia, noise (float64)
		denoised=rt.denoise_bilateral(im,multichannel=False)
	elif (method=="median"): #applied for speckle/gaussian noise/s&p
		denoised=ndimage.median_filter(im,3)
	elif (method=="gaussian"): #applied for gaussian noise/s&p
		denoised=ndimage.gaussian_filter(im,2)
	elif (method=="maximum"): #applied for speckle
		denoised=ndimage.maximum_filter(im,2)
	elif (method=="minimum"): #applied for specke
		denoised=ndimage.minimum_filter(im,3)		

	misc.imsave(filename,denoised)


#!!!dont forget the '/' in the end of the paths!!!
inputPath="/home/banshee/Pictures/ocr-images/Database/denoising/minMax/"
outputPath="/home/banshee/Pictures/ocr-images/Database/denoising/minMax/s&p/"
imgType="*.tiff"

#currently, you need to have directories with the following names in your outputPath
methods=["median","bilateral","gaussian","maximum","minimum"]

#and the following in your inputPath
noisy=["speckle","gauss","s&p"]
os.chdir(inputPath)

#apply the methods
for i in range(0,len(methods)):
	if (methods[i]=="gaussian"):#apply for gaussian noised images
		os.chdir(inputPath+"gauss")
		start = time.time()
		for file in glob.glob(imgType):
			im=misc.imread(file,flatten=True)
			denoise(im,methods[i],outputPath+methods[i]+'/'+"gauss"+file)
		end = time.time()
		print("gauss to",noisy[j],end - start)

	elif (methods[i]=="bilateral"): #apply for speckled and gaussian noised images
		for j in range (0,2):
			os.chdir(inputPath+noisy[1])
			start = time.time()
			for file in glob.glob(imgType):
				im=misc.imread(file,flatten=True).astype(np.float64)#float64 due to skimage issues
				denoise(im,methods[i],outputPath+methods[i]+'/'+noisy[1]+file)
			end = time.time()
			print(methods[i]," to ",noisy[1],end - start)

	elif (methods[i]=="median"): #apply for speckled,gaussian noised and s&p images
		for j in range (0,3):
			os.chdir(inputPath+noisy[j])
			start = time.time()
			for file in glob.glob(imgType):
				im=misc.imread(file,flatten=True)
				denoise(im,methods[i],outputPath+methods[i]+'/'+noisy[j]+file)
			end = time.time()
			print(methods[i]," to ",noisy[j],end - start)

	elif (methods[i]=="maximum"): #apply for speckled images
		os.chdir(inputPath+"speckle")
		start = time.time()
		for file in glob.glob(imgType):
			im=misc.imread(file,flatten=True)
			denoise(im,methods[i],outputPath+methods[i]+'/'+"speckle"+file)
		end = time.time()
		print("maximum to","speckle",end - start)

	elif (methods[i]=="minimum"): #apply for speckled images
		os.chdir(inputPath+"speckle")
		start = time.time()
		for file in glob.glob(imgType):
			im=misc.imread(file,flatten=True)
			denoise(im,methods[i],outputPath+methods[i]+'/'+"speckle"+file)
		end = time.time()
		print("minimum to","speckle",end - start)
