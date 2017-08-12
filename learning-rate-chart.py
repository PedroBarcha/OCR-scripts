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

def plotErrors (test_errors_mean_e3,training_errors_mean_e3,test_errors_mean_e4,training_errors_mean_e4,test_errors_mean_e5,training_errors_mean_e5):
	iteractions=range(0,30000,500)

	plt.plot(iteractions,test_errors_mean_e3,'b')
	plt.plot(iteractions,training_errors_mean_e3, 'g')
	blue_patch = mpatches.Patch(color='blue', label='e-3 Validation Set')
	green_patch = mpatches.Patch(color='green', label='e-3 Training Set')

	plt.plot(iteractions,test_errors_mean_e4,'r')
	plt.plot(iteractions,training_errors_mean_e4, 'c')
	red_patch = mpatches.Patch(color='red', label='e-4 Test Set')
	cyan_patch = mpatches.Patch(color='cyan', label='e-4 Training Set')

	plt.plot(iteractions,test_errors_mean_e5,'m')
	plt.plot(iteractions,training_errors_mean_e5, 'y')
	magenta_patch = mpatches.Patch(color='magenta', label='e-5 Validation Set')
	yellow_patch = mpatches.Patch(color='yellow', label='e-5 Training Set')

	plt.legend(handles=[blue_patch,green_patch,red_patch,cyan_patch,magenta_patch,yellow_patch])
	plt.xlabel("Iteracoes")
	plt.ylabel("Taxa de Erro (%)")
	plt.show()

num_models=NUM_INTERACTIONS/SAVE_FREQ #number of models per fold
test_errors_mean_e3=[0]*num_models
training_errors_mean_e3=[0]*num_models
test_errors_mean_e4=[0]*num_models
training_errors_mean_e4=[0]*num_models
test_errors_mean_e5=[0]*num_models
training_errors_mean_e5=[0]*num_models

#####################################################
for k in range (1,NUM_FOLDS+1):
	os.chdir(str(k)+"/models/e-3")

	#get error arrays
	training_errors=(wrapErr("modeltraining"))
	test_errors=(wrapErr("modelval"))

	#sum the errors of the same interaction
	for i in range (0,num_models):
		test_errors_mean_e3[i]+=test_errors[i]
		training_errors_mean_e3[i]+=training_errors[i]

	del training_errors
	del test_errors
	os.chdir(FOLDS_PATH)


#calculate the mean of the error for each interaction
for i in range (0,num_models):
	test_errors_mean_e3[i]=test_errors_mean_e3[i]/num_models
	training_errors_mean_e3[i]=training_errors_mean_e3[i]/num_models
#####################################################################

#####################################################
for k in range (1,NUM_FOLDS+1):
	os.chdir(str(k)+"/models/e-5")

	#get error arrays
	training_errors=(wrapErr("modeltraining"))
	test_errors=(wrapErr("modelval"))

	#sum the errors of the same interaction
	for i in range (0,num_models):
		test_errors_mean_e5[i]+=test_errors[i]
		training_errors_mean_e5[i]+=training_errors[i]

	del training_errors
	del test_errors
	os.chdir(FOLDS_PATH)


#calculate the mean of the error for each interaction
for i in range (0,num_models):
	test_errors_mean_e5[i]=test_errors_mean_e5[i]/num_models
	training_errors_mean_e5[i]=training_errors_mean_e5[i]/num_models

#########################################################
for k in range (1,NUM_FOLDS+1):
	os.chdir(str(k)+"/models/regular")

	#get error arrays
	training_errors=(wrapErr("modeltraining"))
	test_errors=(wrapErr("modeltest"))

	#sum the errors of the same interaction
	for i in range (0,num_models):
		test_errors_mean_e4[i]+=test_errors[i]
		training_errors_mean_e4[i]+=training_errors[i]

	del training_errors
	del test_errors
	os.chdir(FOLDS_PATH)


#calculate the mean of the error for each interaction
for i in range (0,num_models):
	test_errors_mean_e4[i]=test_errors_mean_e4[i]/num_models
	training_errors_mean_e4[i]=training_errors_mean_e4[i]/num_models
############################################################################

#plot chart
plotErrors(test_errors_mean_e3,training_errors_mean_e3,test_errors_mean_e4,training_errors_mean_e4,test_errors_mean_e5,training_errors_mean_e5)

