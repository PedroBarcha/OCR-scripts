#plots the training and test errors for each model generated from training.
#the errors were formerly given by "modeltraining" and "modeltest" scripts.

#TODO: fazer o resultado inicial ser realmente o inicial, e nao para 500 interacoes

import os,glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

NUM_INTERACTIONS=16000 #training interactions (16k for e-3/e-5 and 30k for regular training)
SAVE_FREQ=500 #training model save frequency
NUM_FOLDS=10
MODEL="e-5" #e-3, e-5 or regular
TEST_SET="modelval" #modelval (e-3 and e-5) or modeltest (regular)
FOLDS_PATH="/home/banshee/Pictures/ocr-images/Database/training/ocropus/k-fold/"

#returns the 3 min values of an array
def minValues(values):
	#print best models
	min1=100.0
	min2=100.0
	min3=100.0
	min1_index=0
	min2_index=0
	min3_index=0

	for i in range (0,num_models):
		if (values[i]<min1):
			min3=min2
			min3_index=min2_index
			min2=min1
			min2_index=min1_index
			min1=values[i]
			min1_index=i
		elif (values[i]<min2):
			min3=min2
			min3_index=min2_index
			min2=values[i]
			min2_index=i
		elif (values[i]<min3):
			min3=values[i]
			min3_index=i

	return min1,min2,min3,min1_index,min2_index,min3_index

#returns error rates in a float array
def wrapErr(file):
	i=0
	errors= []
	with open(file) as model:
		for line in model:
			if (word_in("err",line)):
				error=enhanceLine(line)
				errors.append(error)
				i+=1

	return errors

#return only the value (percentage) of error
def enhanceLine(line):
	error=line.replace("err","")
	error=line.replace("err","")
	error=error.replace(" %","")
	error=error.replace("\n","")
	error=float(error)
	return error

#checks if a whole word is containied within a phrase
def word_in (word, phrase):
    return word in phrase.split()

def plotErrors (training_errors_mean, test_errors_mean):
	iteractions=range(0,NUM_INTERACTIONS,SAVE_FREQ)

	plt.plot(iteractions,test_errors_mean,'b')
	plt.plot(iteractions,training_errors_mean, 'g')

	blue_patch = mpatches.Patch(color='blue', label='Validation Set')
	green_patch = mpatches.Patch(color='green', label='Training Set')
	plt.legend(handles=[green_patch,blue_patch])
	plt.xlabel("Iteracoes")
	plt.ylabel("Taxa de Erro (%)")
	plt.show()

################# MAIN #################################
num_models=NUM_INTERACTIONS/SAVE_FREQ #number of models per fold
test_errors_mean=[0]*num_models
training_errors_mean=[0]*num_models

#for each dir
for k in range (1,NUM_FOLDS+1):
	os.chdir(str(k)+"/models/"+MODEL)

	#get error arrays
	training_errors=(wrapErr("modeltraining"))
	test_errors=(wrapErr(TEST_SET))

	#sum the errors of the same interaction
	for i in range (0,num_models):
		test_errors_mean[i]+=test_errors[i]
		training_errors_mean[i]+=training_errors[i]

	#for each model, print initial test error VS min error
	min1,min2,min3,min1_index,min2_index,min3_index=minValues(test_errors)
	print ("Model:"+str(k)+"\nInitial Test/CV Set Error:"+str(test_errors[0])+"\nMin1 Error:"+str(min1)+" for "+str((min1_index+1)*SAVE_FREQ)+" interactions")
	print ("Min2 Error:"+str(min2)+" for "+str((min2_index+1)*SAVE_FREQ)+" interactions")
	print ("Min3 Error:"+str(min3)+" for "+str((min3_index+1)*SAVE_FREQ)+" interactions")
	print ("Improvement of:"+str((1-(min1/test_errors[0]))*100)+"%\n")

	#return to primary state
	del training_errors
	del test_errors
	os.chdir(FOLDS_PATH)

#calculate the mean of the error for each interaction
for i in range (0,num_models):
	test_errors_mean[i]=test_errors_mean[i]/NUM_FOLDS
	training_errors_mean[i]=training_errors_mean[i]/NUM_FOLDS

#plot chart
plotErrors(training_errors_mean,test_errors_mean)

#get min avarages
min1,min2,min3,min1_index,min2_index,min3_index=minValues(test_errors_mean)

print ("test erro inicial medio: " + str(test_errors_mean[0]))
print ("test global minimum1: " + str(min1) + ", with " + str((min1_index+1)*SAVE_FREQ) + "interactions")
print ("test global minimum2: " + str(min2) + ", with " + str((min2_index+1)*SAVE_FREQ) + "interactions")
print ("test global minimum3: " + str(min3) + ", with "  + str((min3_index+1)*SAVE_FREQ) + "interactions")

print ("test 16k avarage: " + str(test_errors_mean[31]))
print ("test 13.5k avarage: " + str(test_errors_mean[26]))
print ("test 5k avarage: "  + str(test_errors_mean[9]))