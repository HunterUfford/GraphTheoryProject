from WeightedGraph import *
import heapq
import math

def depth_limited_search(graph, threshold, initialNode):
    returnSet = set()
    
    def recur(currentNode, currentWeight):
        for i in range(graph.num_nodes):
            if (graph.adj_matrix[currentNode][i] != 0) and (graph.adj_matrix[currentNode][i] + currentWeight <= threshold):
                returnSet.add(i)
                recur(i, currentWeight + graph.adj_matrix[currentNode][i])
        pass
    
    recur(initialNode, 0)
    
    return returnSet