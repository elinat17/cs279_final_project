import numpy as np
import sys 
import os 
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import zscore
import collections 
import random


def contour_files(dir): 
	filenames = []
	for filename in os.listdir(dir):
	    if filename.endswith('.csv'):
	       filenames.append(os.path.join(dir, filename))
	return filenames

def strip_csv(filenames): 
	arr_of_arrs = []
	for file in filenames: 
		csv = pd.read_csv(file) 
		impcol = (csv[csv.columns[1]])
		dataarr = np.array(impcol)
		arr_of_arrs.append(dataarr)
	return arr_of_arrs

def twoArrs(hemFolder, allFolder): 
	csvshem= hemFolder
	filenameshem = contour_files(csvshem)
	hemarr = strip_csv(filenameshem)
	csvsall= allFolder
	filenameall= contour_files(csvsall)
	allarr = strip_csv(filenameall)

	hemlabel = len(hemarr[0]) *[0]
	alllabel = len(allarr[0]) * [1]
	identityarr = np.array(hemlabel + alllabel)
	totalarr = [] 

	for i in range(len(hemarr)): 
		a1 = hemarr[i]
		a2 = allarr[i]  
		newarr = np.concatenate((a1,a2))
		newarr = [float(i) for i in newarr]
		totalarr.append(newarr)
	area = [float(i) for i in totalarr[0]]
	pathlength = [float(i) for i in totalarr[1]]
	circularity = [] 
	for i in range(len(area)): 
		circularity.append(area[i]*4*3.14/(pathlength[i]*pathlength[i]))

	finalarr = zip(totalarr[0],totalarr[1], totalarr[2], circularity)

	return (finalarr,identityarr)
def testidArr(file): 
	csv = pd.read_csv(file) 
	impcol = (csv[csv.columns[0]])
	dataarr = np.array(impcol)
	identities = [] 
	for i in range(len(dataarr)):
		if dataarr[i].find('hem') != -1 :
			identities.append(0)
		else: 
			identities.append(1)
	return identities

def parseTest(testfolder): 
	testfiles = contour_files(testfolder)
	testarr = strip_csv(testfiles) 
	testidentities = testidArr(testfiles[0])
	area = [float(i) for i in testarr[0]]
	pathlength = [float(i) for i in testarr[1]]
	circularity = [] 
	for i in range(len(area)): 
		circularity.append(area[i]*4*3.14/(pathlength[i]*pathlength[i]))

	finalarr = zip(testarr[0],testarr[1], testarr[2], circularity)
	return (finalarr, testidentities)


def kmeanstrainArr():
	(finalarr1, identityarr1) = twoArrs('trainingSet/hemData/hemAnalysis/hemKMeansCSV', 'trainingSet/allData/allAnalysis/allKMeansCSV')
	(finalarr2, identityarr2) = twoArrs('trainingSet/hemData/hem2Analysis/hem2KMeansCSV', 'trainingSet/allData/all2Analysis/all2KMeansCSV')
	return (np.concatenate((finalarr1,finalarr2)), np.concatenate((identityarr1,identityarr2))) 
	#return (finalarr1,identityarr1)

def kmeanscalc():
	(finalarr,identityarr) = kmeanstrainArr() 
	# scaler = MinMaxScaler()
	# X_scaled = scaler.fit_transform(finalarr)
	kmeans = KMeans(n_clusters=2, max_iter=1000, algorithm = 'auto')
	kmeans.fit(finalarr)

	correct = 0
	for i in range(len(finalarr)):
	    predict_me = np.array(finalarr[i])
	    predict_me = predict_me.reshape(-1, len(predict_me))
	    prediction = kmeans.predict(predict_me)
	    if prediction[0] == identityarr[i]:
	        correct += 1

	kmeansscore =(float(correct)/len(finalarr))
	return (kmeans, kmeansscore)

def kmeanspredict(testfolder, kmeans):

	centroid = kmeans.cluster_centers_

	(testarr,idenarr) = parseTest(testfolder)
	randomindices = random.sample(range(0,len(testarr)),1000)
	newtestarr = [] 
	newindentityarr = []

	for index in randomindices: 
		newtestarr.append(testarr[index])
		newindentityarr.append(idenarr[index])


	#(finalarr2, identityarr2) = twoArrs('hem2Analysis/hem2KMeansCSV', 'all2Analysis/all2KMeansCSV')
	correct = 0
	randcorrect = 0 
	for i in range(len(newtestarr)):
	    predict_me = np.array(newtestarr[i])
	    predict_me = predict_me.reshape(-1, len(predict_me))
	    prediction = kmeans.predict(predict_me)
	    if prediction[0] == newindentityarr[i]:
	        correct += 1
	    if random.random() > 0.5: 
	    	randcorrect+=1

	kmeansscore =(float(correct)/len(newtestarr))
	#kmeans sometimes assigns 1 to healthy, 0 to unhealthy so account for this 
	if (kmeansscore < 0.5): 
		kmeansscore = 1.0-kmeansscore 


	randscore =(float(randcorrect)/len(newtestarr))
	print('kmeans: ' + str(kmeansscore))
	print(' random: ' + str(randscore))

	return (kmeansscore, randscore)

def overallTest(testfolder):
	(kmeansalgorithm, kmeansscore) = kmeanscalc() 
	avkmeans = [] 
	avrand = [] 
	for i in range(10):
		(kmeans, rand) = kmeanspredict(testfolder, kmeansalgorithm)
		avkmeans.append(kmeans)
		avrand.append(rand)

	kmean = np.mean(avkmeans)
	random = np.mean(avrand)

	print('average kmean for 10 iterations ' + str(kmean))
	print('average randomscore for 10 iterations ' + str(random))

