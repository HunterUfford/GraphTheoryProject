from WeightedGraph import *
import math
import numpy

def generateGraph(pointSet, threshold):
    outputGraph = WeightedGraph(len(pointSet))
    for i in range(len(pointSet)):
        for j in range(len(pointSet)):
            if (i != j) and (math.sqrt(numpy.sum(numpy.square(numpy.subtract(pointSet[i], pointSet[j])))) <= threshold):
                outputGraph.adj_matrix[i][j] = math.sqrt(numpy.sum(numpy.square(numpy.subtract(pointSet[i], pointSet[j]))))
    return outputGraph