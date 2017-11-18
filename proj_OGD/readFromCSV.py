from csv import reader
import numpy as np

def printV(arr):
	for x in arr:
		print x;


def load_all(filename):
	with open(filename) as afile:
		r = reader(afile)
		c=0

		data = [];

		for line in r:
			data.append(line);

		data = np.transpose(np.array(data));

		return data;

# load_all('Datasets\BirthRate_StateWise_1971-2012_per1000.csv');

