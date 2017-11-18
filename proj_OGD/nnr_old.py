"""
Train neural network regression model
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

np.set_printoptions(threshold='nan')

from sklearn.neural_network import MLPRegressor

# pri is used to control print statements used for debugging in code.+
pri = 1


# print list vertically
def printV(lst):
    for x in lst:
        print x;


# read input,output from file
def load_all(filename):
    input = []
    output = []
    freq = []
    with open(filename) as afile:
        r = reader(afile)
        c = 0
        cRank = 1
        for line in r:
            # c+=1;
            # if (c<2):
            # continue;

            inp = re.split('\t| ', line[0])

            print line

            input.append(float(inp[0]))

            output.append(float(inp[1]))

            # freq.append(float(inp[2]));

    return input, output


def apply_regression(filename):

    reply_message = ""

    # read filename containing data from commandline argument
    # filename = sys.argv[1]
    input, output = load_all(filename)

    input = array(input)
    output = array(output)
    # freq = array(freq);

    # normalize degrees and ranks between [0,1]
    MaxInput = max(input)
    MaxOutput = max(output)
    MinInput = min(input)
    MinOutput = min(output)

    input = input - MinInput
    output = output - MinOutput

    input = input / float(MaxInput - MinInput)
    output = output / float(MaxOutput - MinOutput)

    if pri > 2 :
        printV(zip(input, output))

    print input.shape, output.shape

    N = len(input)

    # Shuffle input and output array together
    x = np.arange(1, len(input))
    np.random.shuffle(x)
    shuf = x[:]

    comb = zip(x, input)
    comb = sorted(comb)

    input = [x[1] for x in comb]

    comb = zip(shuf, output)
    comb = sorted(comb)

    output = [x[1] for x in comb]

    input = array(input)
    output = array(output)

    input = input.reshape(-1, 1)
    # output = output.reshape(-1,1);



    # split data into training and testing instances
    splitRatio = 0.8  # splitRatio determines how many instances are used for training and testing. eg: 0.2 means 20% train, 80% test
    spl = int(splitRatio * N)  # split location for train-test
    print "Train : ", int(splitRatio * N), "\t Test: ", int((1.0 - splitRatio) * N)
    reply_message += '\n'+"Train : " + str(int(splitRatio * N))+"\t Test: "+str(int((1.0 - splitRatio) * N))

    trI = array(input[:spl])
    trL = array(output[:spl])  # trI - training instances, trL - training labels
    teI = array(input[spl:])
    teL = array(output[spl:])  # teI - testing instances, teL - testing labels

    trI = trI.astype('float')
    teI = teI.astype('float')

    # set parameters of neural network regression model
    nn = MLPRegressor(hidden_layer_sizes=(100, 50), activation='relu', solver='lbfgs', alpha=0.0001, batch_size='auto',
                      learning_rate='adaptive', learning_rate_init=0.001, max_iter=200, shuffle=True, random_state=None,
                      tol=0.00001, verbose=False, momentum=0.5, early_stopping=True, validation_fraction=0.15)

    print trI.shape, trL.shape

    # train NN regression model
    nn.fit(trI, trL)

    # test model to get accuracy
    res = nn.score(teI, teL)

    # 'res' represents how well regression model is learned.
    # It is defined as (1 - u/v), where u is the residual sum of squares ((y_true - y_pred) ** 2).sum()
    # and v is the total sum of squares ((y_true - y_true.mean()) ** 2).sum()

    print 'Accuracy measure: ', res
    reply_message += '\n'+'Accuracy measure: ' + str(res)

    # predict label/output for test instances/degrees for calculating error
    yres = nn.predict(teI)

    R = []  # output
    Dev = []  # deviation from true output

    sum = 0
    if pri > 1:
        print 'Predicted', '\t', 'Actual'
    # calculate deviation from true output for each test instance
    for e in sorted(zip(yres, teL, teI)):

        prank = (e[0] * (MaxOutput - MinOutput)) + MinOutput  # predicted output
        trank = (e[1] * (MaxOutput - MinOutput)) + MinOutput  # true output
        if (pri > 1):
            print (e[2] * (MaxInput - MinInput)) + MinInput, "\t", int(prank), "\t", trank

        sum += abs(prank - trank)

        R.append(e[1])
        Dev.append(abs(prank - trank))

    print 'Avg error: ', (sum / len(yres))
    reply_message += '\n'+'Avg error: '+str(sum / len(yres))

    # ===============================================================================
    #
    # # save plot image of input vs output on log scale
    # plt.plot(input,output,'o',ms=1.5)
    #
    # savefig(filename+".png");
    #
    # plt.clf();
    # #plt.plot(R,Dev,'o',ms=1.5)
    # #plt.show()
    # ===============================================================================

    # correct predicted output < 1 to 1(e^0)
    # yres = [ max(0,x) for x in yres ]

    # show plot of predicted output(dotted line) and actual output (continuous line).
    # NOTE : x-axis is input. Both input(x-axis) and output(y-axis) are on log scale and normalized
    # if pri > 1 :
    #     z = array(sorted(zip(teI, teL, yres)));
    #     plt.plot(z[:, 0], z[:, 2], 'o', ms=4)
    #     plt.plot(z[:, 0], z[:, 1], '-', ms=2)
    #     plt.show()

    return reply_message

# apply_regression("testfile.txt")
# apply_regression("dp_data.txt")