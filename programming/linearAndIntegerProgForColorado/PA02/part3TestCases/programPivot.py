__author__ = 'zhushun0008'

import os
import pylab
import numpy as np
import math

class SimplexDictionary(object):
    def __init__(self, basicIndices, nonBasicIndices, b, equationList,
                 costCoef, cost):
        self.basisIndices = basicIndices
        self.nonBasisIndices = nonBasicIndices
        self.b = b
        self.equationList = equationList
        self.costCoef = costCoef
        self.cost = cost
    def getBasisIndices(self):
        return self.basisIndices
    def getNonBasisIndices(self):
        return self.nonBasisIndices
    def getB(self):
        return self.b
    def getEquationList(self):
        return self.equationList
    def getCostCoef(self):
        return self.costCoef
    def getCost(self):
        return self.cost

def getSortedIndices(orignList, sortedList):
    sortedIndices = []
    for i in range(len(sortedList)):
        for j in range(len(orignList)):
            if sortedList[i] == orignList[j]:
                sortedIndices.append(j)
    return sortedIndices

def parseFile(filename):
    basicIndices = []
    nonBasicIndices = []
    b = []
    equationList = []
    costCoef = []

    fp = open(filename, 'r')

    line = fp.readline().split()
    (numEquations, numVars) = (int(line[0]), int(line[1]))

    # Get the Indices of Basic Variables
    basicLine = fp.readline().split()
    for x in basicLine:
        basicIndices.append(int(x))

    # Get the Indices of Non-Basic Variables
    nonBasicLine = fp.readline().split()
    for x in nonBasicLine:
       nonBasicIndices.append(int(x))

    # Get b
    bLine = fp.readline().split()
    for x in bLine:
        b.append(float(x))

    # Get Equation Matrix
    for i in range(numEquations):
        line = fp.readline().split()
        equationList.append([float(x) for x in line])

    # Get cost coefficients
    coefLine = fp.readline().split()
    cost = float(coefLine[0])
    for x in coefLine[1:]:
        costCoef.append(float(x))
    fp.close()
    initDict = SimplexDictionary(basicIndices, nonBasicIndices, b,
                                 equationList, costCoef, cost)

    return initDict

def progamPivot(initDict):

    basicIndices = initDict.getBasisIndices()
    nonBasicIndices = initDict.getNonBasisIndices()
    b = initDict.getB()
    equationList = initDict.getEquationList()
    costCoef = initDict.getCostCoef()
    cost = initDict.getCost()

    numEquations = len(basicIndices)
    numVars = len(nonBasicIndices)

    sortedBasic = sorted(basicIndices)
    sortedNonBasic = sorted(nonBasicIndices)
    sortedIndicesForBasic = getSortedIndices(basicIndices, sortedBasic)
    sortedIndicesForNonBasic = getSortedIndices(nonBasicIndices, sortedNonBasic)
    enterVar = None
    leavingVar = None
    ## 01 Entering Variable Analysis for Non-Basis
    for i in range(numVars):
        ii = sortedIndicesForNonBasic[i]
        if costCoef[ii] > 0:
            enterVar = nonBasicIndices[ii]

            ## 02 Leaving Variable Analysis
            minX = None
            enterIndex = nonBasicIndices.index(enterVar)
            for j in range(numEquations):
                jj = sortedIndicesForBasic[j]
                if equationList[jj][enterIndex] < 0:
                    tempMin = b[jj] / (-1 * equationList[jj][enterIndex])
                    if minX == None or tempMin < minX:
                        minX = tempMin
                        leavingVar = basicIndices[jj]
            if minX != None:
                break
            else:
                leavingVar = 'UNBOUNDED'
                return [enterVar, leavingVar, 'n/a']

    leavingIndex = basicIndices.index(leavingVar)

    ## Update Dictionary
    unitNum = (-1.0) * equationList[leavingIndex][enterIndex]
    for i in range(numEquations):
        if i != leavingIndex:
            equationList[i][enterIndex] /= unitNum
            b[i] += equationList[i][enterIndex] * b[leavingIndex] / unitNum
            for j in range(numVars):
                if j != enterIndex:
                    equationList[i][j] += equationList[i][enterIndex] * \
                                          equationList[leavingIndex][j] / unitNum
        else:
            b[i] /= unitNum

    for j in range(numVars):
        equationList[leavingIndex][j] /= unitNum


    basicIndices[leavingIndex] = enterVar
    nonBasicIndices[enterIndex] = leavingVar
    cost += b[leavingIndex] * costCoef[enterIndex]
    return [enterVar, leavingVar, cost]


def simplexWithoutInit(filename):
    [basicIndices, nonBasicIndices, b, equationList, costCoef, cost] = parseFile(filename)
    progamPivot(basicIndices, nonBasicIndices, b, equationList, costCoef, cost)