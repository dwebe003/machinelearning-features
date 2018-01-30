#########################################################################################
#
#   File:       featureselection.py
#   Author:     David Weber (dwebe003)
#   Date:       11/27/2017
#   Version:    1.0
#

#   Algorithms: Forward Search
#               Backward Elimination
#               #
#
#
#########################################################################################
#imports & globals
from random import *
import math, copy

MODE = []

###########################################################################################################################
def doubleChecker(data):
	randomNums = []
	data1 = copy.deepcopy(data)
	data2 = copy.deepcopy(data)
	data3 = copy.deepcopy(data)
	data4 = copy.deepcopy(data)
	data5 = copy.deepcopy(data)
	
	for i in range(5):
		randomNum = randrange(0, 100 - i)
		del data1[randomNum]
		
	for i in range(5):
		randomNum = randrange(0, 100 - i)
		del data2[randomNum]
		
	for i in range(5):
		randomNum = randrange(0, 100 - i)
		del data3[randomNum]
		
	for i in range(5):
		randomNum = randrange(0, 100 - i)
		del data4[randomNum]
		
	for i in range(5):
		randomNum = randrange(0, 100 - i)
		del data5[randomNum]
	
	global MODE
	
	arr1 = []
	arr2 = []
	arr3 = []
	arr4 = []
	arr5 = []
	
	if MODE == "backwards":
		arr1 = backwardsElim(data1)
		arr2 = backwardsElim(data2)
		arr3 = backwardsElim(data3)
		arr4 = backwardsElim(data4)
		arr5 = backwardsElim(data5)
	elif MODE == "forwards":
		arr1 = featureSearch(data1)
		arr2 = featureSearch(data2)
		arr3 = featureSearch(data3)
		arr4 = featureSearch(data4)
		arr5 = featureSearch(data5)
	elif MODE == "mysearch":
		arr1 = mySearch(data1)
		arr2 = mySearch(data2)
		arr3 = mySearch(data3)
		arr4 = mySearch(data4)
		arr5 = mySearch(data5)
	
	print 'my arrays:'
	print arr1
	print arr2
	print arr3
	print arr4
	print arr5
	
	
	
	


###########################################################################################################################
def NearestNeighbor(data, currentSetOfFeatures, samplePoint, k):
	closest = 30.0
	index = 0
	
	features = copy.deepcopy(currentSetOfFeatures)
	
	global MODE
	
	if(MODE == "forwards"):
		features.append(k)
	elif(MODE == "backwards"):
		if k != 0:
			features.remove(k)
		#print 'set without k: ', features
	elif(MODE == "mysearch"):
		features.append(k)
		samples = []
		samples.append(samplePoint)
		count = 1
		for i in range(1, 30):
			if(samplePoint + i >= 100):
				samples.append(samplePoint - count)
				count += 1
			else:
				samples.append(samplePoint + i)
			
	
	for i in range(0, len(data)):
		
		if MODE != "mysearch":
			if(i != samplePoint):
				#calculate distance
				dist = 0
				for j in features:
					dist += (float(data[samplePoint][j]) - float(data[i][j])) * (float(data[samplePoint][j]) - float(data[i][j]))
				
				dist = math.sqrt(dist)
				if(dist < closest):
					closest = dist
					index = i
		else:
			if i not in samples:
				dist = 0
				for j in features:
					dist += (float(data[samplePoint][j]) - float(data[i][j])) * (float(data[samplePoint][j]) - float(data[i][j]))
				
				dist = math.sqrt(dist)
				if(dist < closest):
					closest = dist
					index = i
					
	return data[index][0]



###########################################################################################################################
def leave10out(data, currentSetOfFeatures, k, bestSoFar):
	
	numWrong = 0
	numCorrect = 0
	smallestErrorSoFar = len(data) - (bestSoFar * len(data))
	
	for i in range(0, len(data)):
		clas = NearestNeighbor(data, currentSetOfFeatures, i, k)
		
		if clas == data[i][0]:
			numCorrect += 1
		else:
			numWrong += 1
			
		if numWrong > smallestErrorSoFar:
			print 'Worse accuracy reached. Exiting early...'
			return 0
			
			
			
	
	accuracy = float(numCorrect) / float(len(data))
	return accuracy


###########################################################################################################################
def leave1out(data, currentSetOfFeatures, k, bestSoFar):
	
	numWrong = 0
	numCorrect = 0
	smallestErrorSoFar = len(data) - (bestSoFar * len(data))
	
	for i in range(0, len(data)):
		clas = NearestNeighbor(data, currentSetOfFeatures, i, k)
		
		if clas == data[i][0]:
			numCorrect += 1
		else:
			numWrong += 1
			
		if numWrong > smallestErrorSoFar:
			print 'Worse accuracy reached. Exiting early...'
			return 0
			
			
			
	
	accuracy = float(numCorrect) / float(len(data))
	return accuracy
	
	
	# divide dataset into K equal sized sections
	# Test algorithm K times, each time leave one K section out
	# this K section will not be used to BUILD the classifier but
	# will be used to TEST the classifer
	
	#accuracy = # correct classifications / # instances in database
	
	#confusion matrix
	# [ 	 CAT | DOG | PIG   ]
	# [ CAT  100    0     0    ]
	# [ DOG   9     90    1    ]
	# [ PIG   45    45    10   ]
	

###########################################################################################################################	

def	mySearch(data, kFold):	
	currentSetOfFeatures = []
	GlobalAccuracy = 0.0
	
	for i in range(1, len(data[0]) - 1):   	#iterates from 1 to 9th feature
		print 'On the ', i, ' level of the search tree...'
		featureToAdd = []
		bestSoFarAccuracy = 0.0
		
		for k in range(1, len(data[0]) - 1):	#iterates from 1 to 9th feature
			if k not in currentSetOfFeatures:
				
				print 'Considering adding the ', k, ' feature'
				print 'Current Set: ', currentSetOfFeatures
				accuracy = leaveKout(data, currentSetOfFeatures, k, bestSoFarAccuracy, kFold)
				print 'accuracy: ', accuracy
				if accuracy > bestSoFarAccuracy:
					bestSoFarAccuracy = accuracy
					if bestSoFarAccuracy > GlobalAccuracy:
						GlobalAccuracy = bestSoFarAccuracy
						print 'Global: ', GlobalAccuracy
						featureToAdd = k

				#print 'bestaccuracy: ', bestSoFarAccuracy
				#endif
			#endif
		#endfor
		if featureToAdd:
			currentSetOfFeatures.append(featureToAdd);
		
		print 'On level ', i, ' we added feature ', featureToAdd, ' to current set\n'
	
	#print 'currentSetOfFeatures: ', currentSetOfFeatures
	return currentSetOfFeatures, GlobalAccuracy


###########################################################################################################################
	

def	featureSearch(data):	
	currentSetOfFeatures = []
	GlobalAccuracy = 0.0
	
	for i in range(1, len(data[0]) - 1):   	#iterates from 1 to 9th feature
		print 'On the ', i, ' level of the search tree...'
		featureToAdd = []
		bestSoFarAccuracy = 0.0
		
		for k in range(1, len(data[0]) - 1):	#iterates from 1 to 9th feature
			if k not in currentSetOfFeatures:
				
				print 'Considering adding the ', k, ' feature'
				print 'Current Set: ', currentSetOfFeatures
				accuracy = leave1out(data, currentSetOfFeatures, k, bestSoFarAccuracy)
				print 'accuracy: ', accuracy
				if accuracy > bestSoFarAccuracy:
					bestSoFarAccuracy = accuracy
					if bestSoFarAccuracy > GlobalAccuracy:
						GlobalAccuracy = bestSoFarAccuracy
						print 'Global: ', GlobalAccuracy
						featureToAdd = k

				#print 'bestaccuracy: ', bestSoFarAccuracy
				#endif
			#endif
		#endfor
		if featureToAdd:
			currentSetOfFeatures.append(featureToAdd);
		
		print 'On level ', i, ' we added feature ', featureToAdd, ' to current set\n'
	
	#print 'currentSetOfFeatures: ', currentSetOfFeatures
	return currentSetOfFeatures, GlobalAccuracy
	
###########################################################################################################################
	

def	backwardsElim(data):	

	currentSetOfFeatures = []
	GlobalAccuracy = 0
	
	# set currentSet to have every feature
	for i in range(1, len(data[0]) - 1):
		currentSetOfFeatures.append(i)

	#calculate current bestAccuracy, starts at 75 %
	bestSoFarAccuracy = 0
	bestSoFarAccuracy = leave1out(data, currentSetOfFeatures, 0, bestSoFarAccuracy)
	
	for i in range(1, len(data[0]) - 1):   	#iterates from 1 to 9th level
		print 'On the ', i, ' level of the search tree...'
		featureToRemove = []
		
		for k in range(1, len(data[0]) - 1):	#iterates from 1 to 9th feature
			if k in currentSetOfFeatures:
				
				print 'Considering removing the ', k, ' feature'
				print 'Current Set: ', currentSetOfFeatures
				
				accuracy = leave1out(data, currentSetOfFeatures, k, bestSoFarAccuracy)
				
				print 'accuracy: ', accuracy
				if accuracy > bestSoFarAccuracy:
					bestSoFarAccuracy = accuracy
					featureToRemove = k

				#print 'bestaccuracy: ', bestSoFarAccuracy
				#endif
			#endif
		#endfor
		if not featureToRemove:
			continue
		else:
			currentSetOfFeatures.remove(featureToRemove);
		
		print 'On level ', i, ' we removed feature ', featureToRemove, ' from the current set\n'
	
	#print 'currentSetOfFeatures: ', currentSetOfFeatures
	return currentSetOfFeatures, bestSoFarAccuracy
	
	#doubleChecker(data, currentSetOfFeatures)


###########################################################################################################################

def getInput():
	
	arr1 = []
	arr2 = []
	filename = raw_input("Enter file name: ")
	file = open(filename, 'r')
	
	while True:
		line = file.readline()
		if line == '':
			break
		line = line.split()
		arr1.append(line)
			
	#arr = inFile.readline()
	#arr = arr.split()
	#print arr[0]
	
	return arr1

  	
###########################################################################################################################

def main():
	arr = getInput()
	#print len(arr)
	#featureSearch(arr)
	global MODE 
	MODE = "backwards"
	doubleChecker(arr)
	#backwardsElim(arr)
	
	print("\n\n")
	
if __name__ == '__main__':
	main()

