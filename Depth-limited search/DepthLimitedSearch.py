from WeightedGraph import *
import math

def depth_limited_search(graph, threshold, initialNode):
    returnSet = set()
    nodeStack = []

    def recur(currentNode, currentWeight):
        nodeStack.append(currentNode)
        for i in range(graph.num_nodes):
            if (i not in nodeStack) and (graph.adj_matrix[currentNode][i] != 0) and (graph.adj_matrix[currentNode][i] + currentWeight <= threshold):
                returnSet.add(i)
                recur(i, currentWeight + graph.adj_matrix[currentNode][i])
        nodeStack.pop
        pass
    
    recur(initialNode, 0)
    
    return returnSet