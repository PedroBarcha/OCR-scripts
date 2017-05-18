import os,glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

NUM_INTERACTIONS=16000 #training interactions
SAVE_FREQ=500 #training model save frequency
NUM_FOLDS=10
MODEL="e-3" #e-3, e-5 or regular
TEST_SET="modelval" #modelval (e-3 and e-5) or modeltest (regular)
FOLDS_PATH="/home/banshee/Pictures/ocr-images/Database/training/ocropus/k-fold/"

#plots the training and test errors for each model generated from training.
#the errors were formerly given by "modeltraining" and "modeltest" scripts.

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

	print i
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
	iteractions=range(0,30000,500)

	plt.plot(iteractions,test_errors_mean,'b')
	plt.plot(iteractions,training_errors_mean, 'g')

	blue_patch = mpatches.Patch(color='blue', label='Test Set')
	green_patch = mpatches.Patch(color='green', label='Training Set')
	plt.legend(handles=[green_patch,blue_patch])
	plt.xlabel("Iteracoes")
	plt.ylabel("Taxa de Erro (%)")
	plt.show()

num_models=NUM_INTERACTIONS/SAVE_FREQ #number of models per fold
test_errors_mean=[0]*num_models
training_errors_mean=[0]*num_models

#for each dir
for k in range (1,NUM_FOLDS+1):
	os.chdir(str(k)+"/models/"+MODEL)

	#get error arrays
	training_errors=(wrapErr("modeltraining"))
	test_errors=(wrapErr("modelval"))

	#sum the errors of the same interaction
	for i in range (0,num_models):
		test_errors_mean[i]+=test_errors[i]
		training_errors_mean[i]+=training_errors[i]

	del training_errors
	del test_errors
	os.chdir(FOLDS_PATH)


#calculate the mean of the error for each interaction
for i in range (0,num_models):
	test_errors_mean[i]=test_errors_mean[i]/num_models
	training_errors_mean[i]=training_errors_mean[i]/num_models

#plot chart
plotErrors(training_errors_mean,test_errors_mean)

#print best models
min1=100.0
min2=100.0
min3=100.0
min1_index=0
min2_index=0
min3_index=0
for i in range (0,num_models):
	if (test_errors_mean[i]<min1):
		min3=min2
		min3_index=min2_index
		min2=min1
		min2_index=min1_index
		min1=test_errors_mean[i]
		min1_index=i
	elif (test_errors_mean[i]<min2):
		min3=min2
		min3_index=min2_index
		min2=test_errors_mean[i]
		min2_index=i

	elif (test_errors_mean[i]<min3):
		min3=test_errors_mean[i]
		min3_index=i

print ("test erro inicial medio: " + str(test_errors_mean[0]))
print ("test global minimum1: " + str(min1) + ", with " + str((min1_index+1)*500) + "interactions")
print ("test global minimum2: " + str(min2) + ", with " + str((min2_index+1)*500) + "interactions")
print ("test global minimum3: " + str(min3) + ", with "  + str((min3_index+1)*500) + "interactions")






