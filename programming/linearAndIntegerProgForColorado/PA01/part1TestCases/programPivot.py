__author__ = 'zhushun0008'

import os
import pylab
import numpy as np
import math

def getSortedIndices(orignList, sortedList):
    sortedIndices = []
    for i in range(len(sortedList)):
        for j in range(len(orignList)):
            if sortedList[i] == orignList[j]:
                sortedIndices.append(j)
    return sortedIndices

def progamPivot(filename):
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

    # b[leavingIndex] /= abs(equationList[leavingIndex][enterIndex])
    # for j in range(numVars):
    #     equationList[enterIndex][j] /= abs(equationList[leavingIndex][enterIndex])
    #

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

#
# print progamPivot(
#     'F:\SkyDrive\Studying\coursera\linearAndIntegerProgramming'
#     '\LinearAndIntegerProgramming\programming\linearAndIntegerProgForColorado'
#     '\PA01\part1TestCases\unitTests\dict10')

print progamPivot(
    'F:\SkyDrive\Studying\coursera\linearAndIntegerProgramming'
    '\LinearAndIntegerProgramming\programming\linearAndIntegerProgForColorado'
    '\PA01\part1TestCases\AssignmentParts\part5.dict')
