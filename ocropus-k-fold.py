import os,glob,random
from shutil import copy

#for each fold
for k in range (1,11):
	#creates traind and test dirs in k dir if they dont exist
	if not os.path.exists("k-fold/"+str(k)+"/training"):
  	  os.makedirs("k-fold/"+str(k)+"/training")
	if not os.path.exists("k-fold/"+str(k)+"/test"):
   	 os.makedirs("k-fold/"+str(k)+"/test")

   	#for each book
	for dir in range (1,12):
		num_frases=0
		frases=[]
		os.chdir(str(dir))

		#creates list containing the name of the gt files
		for file in glob.glob("*.gt.txt"):
			num_frases+=1
			frases.append(file.replace(".gt.txt",""))

		num_training=(7*num_frases)/10
		for i in range (0,num_training):
			idx=random.randrange(0,num_frases)
			copy(frases[idx]+".gt.txt", "../k-fold/"+str(k)+"/training")
			copy(frases[idx]+".bin.png", "../k-fold/"+str(k)+"/training")
			copy(frases[idx]+".txt", "../k-fold/"+str(k)+"/training")
			frases.pop(idx)
			num_frases-=1

		for i in range (0,num_frases):
			copy(frases[i]+".gt.txt", "../k-fold/"+str(k)+"/test")
			copy(frases[i]+".bin.png", "../k-fold/"+str(k)+"/test")
			copy(frases[i]+".txt", "../k-fold/"+str(k)+"/test")

		os.chdir("..")
	
