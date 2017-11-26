from pylab import *
import numpy as np
from csv import reader
import re
import matplotlib.pyplot as plt

np.set_printoptions(threshold='nan')

pri = 1;


def showColorMappedImage(i1, ShowNow):
	plt.figure();
	plt.imshow(i1, cmap='jet', interpolation='nearest');
	if (ShowNow == 1):
		plt.show();


# print list vertically
def printV(lst):
	for x in lst:
		print x;


"""
# read input,output from file
def load_all(filename):

    input=[]; Labels = [];
    with open(filename) as afile:
        r = reader(afile)
        c=0
        cRank=1;
        for line in r:
            c+=1;
            if (c==1):
				Labels = line;

            inp=re.split('\t| ',line[0]);

            input.append(map(float,inp));

            #freq.append(float(inp[2]));

    return input,Labels;
"""


# read degree,rank from file
def load_all(filename, inCol, outCol):
	degree = [];
	rank = [];
	freq = [];
	doubleCols = [];
	Labels = [];
	with open(filename) as afile:
		r = reader(afile)
		c = 0
		rr = [None] * 2;
		for line in r:
			c += 1;
			print line;
			if (c == 1):
				line = ",".join(line);
				Labels = re.split('\|',line);
				continue;
			if (c > 3):
				break;
			rr[c - 2] = re.split('\|', line[0]);
		
		colType = map(float, rr[0]);
		if (pri > 1):
			print 'colType: \n', colType;
		
		if (len(colType) != len(rr[1])):
			print 'ERROR : Column type array length not equal to data length.'
			return [], [], [];
	
	for x in xrange(0, len(colType)):
		if (colType[x] == 0):
			doubleCols.append(x);
	
	colType = array(colType);
	isString = colType[outCol];
	
	# remove string columns from output
	nOutCol = [];
	for x in xrange(0, len(outCol)):
		if (isString[x] == 0):
			nOutCol.append(outCol[x]);
	
	outCol = nOutCol;
	nLabels = [];
	
	for x in outCol:
		nLabels.append(Labels[x]);
	
	Labels = nLabels;
	
	with open(filename) as afile:
		r = reader(afile)
		c = 0
		cRank = 1;
		for line in r:
			c += 1;
			if (c < 2):
				continue;
			
			inp = re.split('\|', line[0]);
			
			nullPresent = 0;
			for x in xrange(0, len(inp)):
				if (((x in inCol) or (x in outCol)) and inp[x] == 'None'):
					nullPresent = 1;
					print 'Row ', c, ' removed';
			
			if (nullPresent > 0):
				continue;
			
			inp = array(inp);
			ran = map(float, list(inp[outCol]));
			
			# print deg
			# print ran
			rank.append(ran);
	
	# printV(zip(degree,rank));
	
	return rank, Labels;


def findCorrelation(filename, input, output):
	# read filename containing data from commandline argument
	input, Labels = load_all(filename, input, output);
	print 'Labels: ', Labels;
	
	input = transpose(array(input));
	
	# print shape(input);
	
	Corr = corrcoef(input);
	
	NumCols = Corr.shape[0];
	
	"""
	Labels = linspace(1,NumCols,NumCols);
	Labels = Labels.astype(int)+64;
	Labels = map(chr,Labels);
	print Labels;

	#Labels = ['asadsbd','adgsbtrse','serntse6n4','45nnsn5y','45n4'];
	"""
	
	print 'Correlation matrix: \n', Corr;
	
	CorrImg = repeat(Corr, 10, axis=0);
	CorrImg = repeat(CorrImg, 10, axis=1);
	
	fig, ax1 = plt.subplots(1, 1)
	cax = ax1.imshow(CorrImg, cmap='jet', interpolation='nearest')
	ax1.set_xticklabels([''])
	ax1.set_yticklabels([''])
	for i in xrange(0, NumCols):
		ax1.text(4 + i * 10, -2, Labels[i], ha="left", va="bottom", rotation=30, size=10)
		ax1.text(-2, 4 + i * 10, Labels[i], ha="right", va="top", rotation=0, size=10)
	
	# ax1.annotate('local max', xy=(2, 1), xytext=(0,0), rotation=45)
	# plt.show();
	
	"""
	ColorBar = linspace(1,0,10);
	ColorBar = ColorBar.reshape(-1,1);
	ColorBar= repeat(ColorBar, 5 ,axis=0);
	ColorBar= repeat(ColorBar, 5 ,axis=1);

	ax2.imshow(ColorBar, cmap='jet', interpolation='nearest')
	ax2.set_xticklabels([''])
	start, end = ax1.get_xlim()
	ax2.yaxis.set_ticks(np.arange(0, 55, 5))
	ax2.set_yticklabels([1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0])
	ax2.set_title('Correlation Color Map')
	"""
	
	figure = plt.gcf()  # get current figure
	figure.set_size_inches(10, 8)
	# figure.tight_layout()
	
	cbar = fig.colorbar(cax, ax=ax1, orientation=u'vertical')
	
	plt.savefig('C:\\xampp1\\htdocs\\ogd\\corr.png', dpi=100, bbox_inches="tight");
	# plt.show();
	return Corr;


# result = findCorrelation('data.txt', [1], [2, 3, 4, 5, 6, 7])