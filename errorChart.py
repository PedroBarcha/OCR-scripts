import os,glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


#returns error rates in a float array
def wrapErr(file):
	errors= []
	with open(file) as model:
		for line in model:
			if (word_in("err",line)):
				error=enhanceLine(line)
				errors.append(error)

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


test_errors=[]
training_errors=[]
test_errors_mean=[0]*60
training_errors_mean=[0]*60

#for eeach dir
for k in range (1,10):
	os.chdir(str(k))

	training_errors=(wrapErr("modeltraining"))
	test_errors=(wrapErr("modeltest"))

	#sum the errors of same interaction
	for i in range (0,60):
		test_errors_mean[i]+=test_errors[i]
		training_errors_mean[i]+=training_errors[i]

	del training_errors
	del test_errors
	os.chdir("..")


#calculate the mean of the error for each interaction
for i in range (0,60):
	test_errors_mean[i]=test_errors_mean[i]/10
	training_errors_mean[i]=training_errors_mean[i]/10

plotErrors(training_errors_mean,test_errors_mean)





