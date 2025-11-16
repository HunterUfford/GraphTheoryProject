from WeightedGraph import *
import math
import numpy

def generateGraph(pointSet, threshold):
    outputGraph = WeightedGraph(len(pointSet))
    for i in pointSet:
        for j in pointSet:
            if (i != j) and (math.sqrt(sum(numpy.square(numpy.subtract(i, j)))) <= threshold):
                WeightedGraph[i][j] = math.sqrt(sum(numpy.square(numpy.subtract(i, j))))
    return outputGraph