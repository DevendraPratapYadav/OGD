"""
Train neural network regression model using degree-rank data on log scale
Devendra - 2014CSB1010
"""

import os, struct
from array import array as pyarray
import math
from numpy import *
from pylab import *
import numpy as np
import sys
from csv import reader
import re
from collections import Counter
from sklearn.multioutput import MultiOutputRegressor

np.set_printoptions(threshold='nan')

from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler

pri=1

#print list vertically
def printV(lst):
    for x in lst:
        print x;

def doShuffle(degree,rank):
	
	# Shuffle degree and rank array together
	shuf = np.arange(0,len(degree));
	np.random.shuffle(shuf);

	comb=zip(shuf,degree);
	comb=sorted(comb);

	degree=[x[1] for x in comb];

	comb=zip(shuf,rank);
	comb=sorted(comb);

	rank=[x[1] for x in comb];

	
	degree = array(degree);
	rank = array(rank);
	
	return degree,rank
	
def doSort(degree,rank):
	
	comb=zip(degree,rank);
	comb=sorted(comb);

	degree=[x[0] for x in comb];

	rank=[x[1] for x in comb];
	
	degree = array(degree);
	rank = array(rank);
	
	return degree,rank
	
# read degree,rank from file
def load_all(filename, inCol, outCol):

	degree=[]; rank=[]; freq=[];
	doubleCols = [];
	Labels = [];
	with open(filename) as afile:
		r = reader(afile)
		c=0
		rr = [None]*2;
		for line in r:
			c+=1;
			if (c==1):
				line = ",".join(line);
				Labels = re.split('\|', line);
				continue;
			if (c>3):
				break;
			rr[c-2] = re.split('\|',line[0]);
			
		
		colType = map(float,rr[0]);
		if (pri>1):
			print 'colType: \n',colType;
		
		if (len(colType)!=len(rr[1])):
			print 'ERROR : Column type array length not equal to data length.'
			return [],[],[],[],[];
	
	
	for x in xrange(0,len(colType)):
		if (colType[x]==0):
			doubleCols.append(x);
	
	for x in xrange(0,len(colType)):
		if (colType[x]==2):
			colType[x]= 0;
	
	colType = array(colType);
	isString = colType[inCol];
	
	inLabels = array(Labels)[inCol];
	outLabels = array(Labels)[outCol];
	
	
	with open(filename) as afile:
		r = reader(afile)
		c=0
		cRank=1;
		for line in r:
			c+=1;
			if (c<3):
				continue;
    
			inp=re.split('\|',line[0]);
			
			nullPresent = 0;
			for x in xrange(0,len(inp)):
				if ( ((x in inCol) or (x in outCol)) and inp[x]=='None' ):
					nullPresent=1;
					print 'Row ',c, ' removed';
			
			if (nullPresent>0):
				continue;
			
			#inp[doubleCols] = map(float,inp[doubleCols]);
			
			#print inp
			
            #degree.append(map(float,inp[ inCol ]));
            #rank.append(map(float,inp[ outCol ]));
			
			inp = array(inp);
			
			deg = list(inp[ inCol ]);
			ran = map(float,list(inp[ outCol ]));
			
			for uu in xrange(0,len(isString)):
				if (isString[uu]==0):
					deg[uu] = float(deg[uu]);
			
			#print deg
			#print ran
			degree.append(deg);
			rank.append(ran);
   
	
	#printV(zip(degree,rank));
	
	return degree,rank,isString,inLabels,outLabels;

def removeStrings(data,isString):
	#data = array(data);
	uniqData = [None]*len(data[0]);
	
	#if (len(data.shape)==1):
	#	data = data.reshape(-1,1);
	data2 = array(data);
	#print 'Remove Strings from: \n',data
	for x in xrange(0,len(data[0])):
		if (  isString[x]==1 ):
			Dict = {};
			ustr = unique(data2[:,x]);
			uniqData[x] = ustr;
			
			for ind in xrange(0,len(ustr)):
				Dict[ ustr[ind] ]=ind;
			
			for rr in xrange(0,len(data)):
				data[rr][x] = Dict[ data[rr][x] ];
			#printV(data);
	
	
	return data, uniqData;


def addStrings(data,uniqData):
	ndata = [0]*data.shape[0];
	ndata = [ ([0]*data.shape[1]) for x in ndata];
	
	for x in xrange(0, len(uniqData)):
		if (uniqData[x] == None):
			for rr in xrange(0,len(data[:,x])):
				ndata[rr][x] = data[rr,x];
		else:
			for rr in xrange(0,len(data[:,x])):
				ndata[rr][x] = uniqData[x][ int(data[rr,x])];
			
	#printV(ndata);
	return ndata;
	
	
def normalizeColumns(degree):
	scalers = [None] * degree.shape[1];
	for x in xrange(0,degree.shape[1]):
		scaler = MinMaxScaler(feature_range=(0, 1))
		scaler = scaler.fit(degree[:,x].reshape(-1,1));
		degree[:,x] = list(scaler.transform(degree[:,x].reshape(-1,1)));
		scalers[x] = scaler;
	
	return degree,scalers;

def normalizeValues(degree,scalers):
	
	for x in xrange(0,degree.shape[1]):
		degree[:,x] = list(scalers[x].transform(degree[:,x].reshape(-1,1)));#scalers[x].transform(degree[:,x]);
		
	return degree;
	
def deNormalizeColumns(degree,scalers):
	
	for x in xrange(0,degree.shape[1]):
		degree[:,x] = list(scalers[x].inverse_transform(degree[:,x].reshape(-1,1)));#scalers[x].inverse_transform(degree[:,x]);
		
	return degree;

def deNormalizeValue(val, scalers):
	val = scalers.inverse_transform(val);
	return val;
	
def apply_regression(filename, inCol, outCol, predValues):
	# read input output columns from filename
	degree,rank,isString,inLabels,outLabels = load_all(filename, inCol, outCol);

	print 'Labels: ',inLabels,'\n', outLabels;
	
	printV(zip(degree,rank))
	#TODO : check that output column can't be string
	
	if (len(degree)==0 or len(rank)==0 ):
		print 'ERROR : Input or Output data is empty.'
		return [];
	
	
	# REPLACE STRINGS with numbers
	#degree, uniqDegree = removeStrings(degree,isString);
	
	degree = array(degree); rank = array(rank);
	#degree = addStrings(degree, uniqDegree);
	
	"""
	print 'Degree: ';
	printV(degree);
	print 'uniqDegree: ';
	printV(uniqDegree);
	"""
	
	
	degree,Dscalers = normalizeColumns(degree);
	#print degree;
	rank,Rscalers = normalizeColumns(rank);
	
	#printV(zip(degree,rank));
	"""
	degree= deNormalizeColumns(degree,Dscalers);
	rank= deNormalizeColumns(rank,Rscalers);
	
	printV(zip(degree,rank));
	"""
	
	# generate prediction inputs
	order = [];
	pv = [];
	for e in predValues:
		v = linspace(e[1], (e[1]+(e[2]-1)*e[3]), e[2] );
		v=v.reshape(-1,1);
		if (len(pv)==0):
			pv=v;
		else:
			pv=hstack((pv,v));
		order.append(e[0]);
	
	#print 'Order:',order
	#print 'Predicted Values:\n',pv
	
	runs=1;

	# convert both degree,rank to log scale for better prediction accuracy
	#rank = [ log(x) for x in rank ]
	#degree = [ log(x) for x in degree ]

	degree = array(degree);
	rank = array(rank);
	#freq = array(freq);
	
	"""
	# normalize degrees and ranks between [0,1]
	MaxDegree = max(degree)*2;
	MinDegree = min(degree);
	MaxRank = max(rank);
	degree = array( [(x)/float(MaxDegree) for x in degree] );
	rank = rank/float(MaxRank);
	"""
	if (pri>3):
		printV(zip(degree,rank))
	
	print degree.shape, rank.shape

	N = len(degree)

	AvgErr = 0;
	AvgWerr = 0;

	for rr in xrange(0,runs):

		degree,rank=doShuffle(degree,rank);
		
		"""
		ff = open('in.txt','w');
		
		ff.write(str(MaxRank)+'\n');
		
		for e in zip(degree,rank):
			ff.write(str(e[0])+' '+str(e[1])+'\n');
		"""
		
		if (len(inCol)==1):
			degree = degree.reshape(-1,1);
		if (len(rank.shape)==1):
			rank = rank.reshape(-1,1);
		
		printV( zip(degree,rank) )
		
		
		# split data into training and testing instances
		splitRatio=0.9 # splitRatio determines how many instances are used for training and testing. eg: 0.2 means 20% train, 80% test
		spl= int(splitRatio*N); #split location for train-test
		
		trI=array(degree[:spl]); trL=array(rank[:spl]); # trI - training instances, trL - training labels
		teI=array(degree[spl:]); teL=array(rank[spl:]); # teI - testing instances, teL - testing labels
		
		trI=trI.astype('float'); teI=teI.astype('float');
		
		
		"""
		print 'Train data:\n'
		printV(zip(trI,trL));
		print 'Test data:\n'
		printV(zip(teI,teL));
		print '\n\n\n'
		"""
		print trI.shape, trL.shape;

		print "Train : ",int(splitRatio*N),"\t Test: ",int((1.0-splitRatio)*N)
		
		
		useSVM=1;
		NoInputs = 1;
		ignoreExtra =1;
		svr=SVR();
		
		"""
		if (useSVM==0):
		
			# set parameters of neural network regression model
			nn = MLPRegressor(hidden_layer_sizes=(20), activation='tanh', solver='lbfgs', alpha=0.0001, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.001, max_iter=500, shuffle=True, random_state=None, tol=0.00001, verbose=False, momentum=0.5, early_stopping=True, validation_fraction=0.15)
		else:
		"""
		mysvr = SVR(C=100, cache_size=200, epsilon=0.00001, gamma=2,kernel='rbf', max_iter=-1, shrinking=True, tol=0.000001, verbose=False)
		# gamma is fitting parameter, small gamma-> simpler curve, >gamma-> complex curve
		
		#create multioutput regressor
		svr = MultiOutputRegressor(mysvr);
		
		# train NN regression model
		
		svr.fit(trI,trL);
		
		
		# test model to get accuracy
		
		res = svr.score(teI,teL);
		# 'res' represents how well regression model is learned.
		# It is defined as (1 - u/v), where u is the residual sum of squares ((y_true - y_pred) ** 2).sum()
		# and v is the total sum of squares ((y_true - y_true.mean()) ** 2).sum()
		
		if (pri>0):
			print 'Accuracy measure: ', res
			
		# predict label/rank for test instances/degrees for calculating error
		
		yres = svr.predict(teI);
		
		sum=0;
		wsum=0;
		if (pri>2):
			print 'Predicted','\t','Actual Rank'
			
		linSum = 0;
		"""
		# calculate deviation from true vaue for each test instance
		for e in sorted(zip(yres,teL,teI)):
			
			prank = max(1, (e[0]*MaxRank)) # predicted rank
			trank =  (e[1]*MaxRank) # true rank
			
			sum+=abs(prank-trank)
			
			lrank =0 ;
			
			if (pri>2):
				print int(prank),"\t", trank, '\t',e[2],'\t',lrank
			
		if (pri>2):
			print 'Avg error: ',(sum/len(yres))
		
		AvgErr+=(sum/len(yres))
		AvgWerr+=(wsum/len(yres))
	if (pri>2):
		print 'Avg error: ',(AvgErr/runs)
	"""
	
	#pv = array( [(x)/float(MaxDegree) for x in pv] );
	pv = normalizeValues(pv,Dscalers);
	
	Pred = svr.predict(pv);
	#printV(zip(pv,Pred));
	
	#print(pv)
	
	"""
	Pred = ( [(x)*MaxRank for x in Pred] );
	yres = ( [(x)*MaxRank for x in yres] );
	pv = array( [(x)*float(MaxDegree) for x in pv] );
	teI = array( [(x)*float(MaxDegree) for x in teI] );
	trI = array( [(x)*float(MaxDegree) for x in trI] );
	teL = ( [(x)*MaxRank for x in teL] );
	trL = ( [(x)*MaxRank for x in trL] );
	"""
	if (len(Pred.shape)==1):
		Pred = Pred.reshape(-1,1);
	
	Pred = deNormalizeColumns(Pred,Rscalers);
	trI = deNormalizeColumns(trI,Dscalers);
	trL = deNormalizeColumns(trL,Rscalers);
	teI = deNormalizeColumns(teI,Dscalers);
	teL = deNormalizeColumns(teL,Rscalers);
	pv = deNormalizeColumns(pv,Dscalers);
	
	#printV(zip(pv,Pred));
	#printV(zip(teI,teL));
	
	# show plot of predicted rank(dotted line) and actual rank (continuous line).
	# NOTE : x-axis is degree. Both degree(x-axis) and rank(y-axis) are on log scale and normalized
	
	#z=array(sorted(zip(teL,yres,teI[:,0])));
	#plt.plot(z[:,2],z[:,1],'x',ms=3)
	#plt.plot(z[:,2],z[:,0],'-',ms=2)
	plt.clf();
	
	
	zz = (sorted(zip(trI[:,0],trL)));
	Xd = [x[0] for x in zz];
	Yd = [x[1] for x in zz];
	
	plt.plot(Xd,Yd,'s-',ms=2)
	
	plt.gca().set_prop_cycle(None)
	#plt.plot(teI[:,0],teL,'x',ms=3)
	
	plt.plot(array(pv)[:,0],Pred,'o-',ms=5)
	
	plt.gca().set_prop_cycle(None)
	
	for i in xrange(0,Pred.shape[1]):
		plt.plot(Xd[0], Yd[0][0], 'o-', label=outLabels[i])
	
	
	plt.plot(Xd[0], Yd[0][0], '', label='Accuracy:'+(str(max(0,99*float("{0:.2f}".format(res))) )  )+'%')
	
	
	plt.legend(loc='upper left')
	plt.xlabel(inLabels[0])
	#plt.ylabel('Mortality Rate')
	# plt.show()
	savefig('D:\\xampp\\htdocs\\ogd\\visual.jpg');
	
	limitPrecision = vectorize(lambda x:float("{0:.2f}".format(x)))
	
	Pred = limitPrecision(Pred);
	
	pv = pv.tolist();
	Pred = Pred.tolist();
	#printV(zip(pv,Pred));
	
	#Pred = [e[0] for e in Pred]
	#pv = [e[0] for e in pv]
	# result = [ [e[0],e[1]] for e in zip(pv,Pred) ]
	result = [ e[0]+[',']+e[1] for e in zip(pv,Pred) ]
	#result = result.tolist();
	# print result;
	return result;

#Pr = apply_regression('data.txt',[1],[3,4,5],[[0,2010,20,1]]);
# printV (Pr);