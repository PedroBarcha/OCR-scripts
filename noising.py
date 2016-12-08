#gaussian and salt and pepper noise adapted from Shubham Pachori code, available at
#http://stackoverflow.com/questions/14435632/impulse-gaussian-and-salt-and-pepper-noise-with-opencv
#
#multiplicative speclking adapted from fraxel code, available at 
#http://stackoverflow.com/questions/10310762/speckle-noise-generation
#
#image : ndarray
#    Input image data. Will be converted to float.
#mode : str
#    One of the following strings, selecting the type of noise to add:
#
#    'gauss'     Gaussian-distributed additive noise.
#    's&p'       Replaces random pixels with 0 or 1.
#    'speckle'   Multiplicative noise
#    'blur'      Gaussian blur

import numpy as np
import glob, os
import cv
from scipy import misc,ndimage

def noisy(image,noise_typ,filename):

    if noise_typ == "gauss":
        row,col= image.shape
        mean = 0
        deviation=30
        #var = 0.1
        #sigma = var**0.5
        gauss = np.random.normal(mean,deviation,(row,col))
        gauss = gauss.reshape(row,col)
        noisy = image + gauss
        misc.imsave(filename, noisy)

    elif noise_typ == "s&p":
        row,col = image.shape
        s_vs_p = 0.5
        amount = 0.01
        out = image
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        out[coords] = 255

        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[coords] = 0
        misc.imsave(filename, out)

    elif noise_typ =="speckle":
        mult_noise = cv.CreateImage((image.width,image.height), cv.IPL_DEPTH_32F, 1)
        cv.RandArr(cv.RNG(6), mult_noise, cv.CV_RAND_NORMAL, 1, 0.1)    
        cv.Mul(image, mult_noise, image)
        cv.SaveImage(filename, image)

    elif noise_typ=="blur":
        blur = ndimage.gaussian_filter(image, sigma=3)
        misc.imsave (filename,blur)


#!!!dont forget the '/' in the end of the paths!!!
inputPath="/home/banshee/Pictures/ocr-images/Database/300dpi/tiff/"
outputPath="/home/banshee/Pictures/ocr-images/Database/noising/"
imgType="*.tiff"

#currently, you need to have directories with the following names in your outputPath
#(chose the methods you want to apply [separate noisy images will be generated])
methods=["speckle","gauss","blur","s&p"]


os.chdir(inputPath) #python changes to the specified directory

for i in range (0,len(methods)):
     #open cv image manipulation
    if (methods[i]=="speckle"):
        for file in glob.glob(imgType): #for every .imgType file in the directory
            im = cv.LoadImage(inputPath+file, cv.CV_LOAD_IMAGE_GRAYSCALE)
            noisy(im,"speckle",outputPath+"speckle/"+file)
    #ndimage manipulation
    else:
        for file in glob.glob(imgType): #for every .imgType file in the directory
            im = misc.imread(inputPath+file,flatten=True)
            noisy(im,methods[i],outputPath+methods[i]+'/'+file)

