from WeightedGraph import *
import math
import numpy

def evaluate(pointArray, neighborsGraph, threshold):
    successCount = 0
    failCount = 0
    for i in range(len(pointArray) - 1):
        for j in range(i + 1, len(pointArray)):
            if math.sqrt(numpy.sum(numpy.square(numpy.subtract(pointArray[i], pointArray[j])))) <= threshold:
                if neighborsGraph.adj_matrix[i][j]: #works off of truthiness
                   successCount += 1
                else:
                    failCount += 1
    return (successCount, failCount)