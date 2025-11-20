from pointGenerator import *
from PointSetToWeightedGraph import *
from DepthLimitedSearch import *
from DLSPerformanceEvaluation import *

DEBUGGING = True
if(DEBUGGING):
    import time
    START_TIME = time.time()

seed = 0
userCount = 1000
interestDimension = 8
associationThreshold = 1
searchThreshold = 2

setSeed(seed)
interestSpace = pointSetGen(userCount, interestDimension)
if(DEBUGGING):
    print("Interest space created.", time.time() - START_TIME)

associationGraph = generateGraph(interestSpace, associationThreshold)
if(DEBUGGING):
    print("Association graph created.", time.time() - START_TIME)
    
recommendations = []
for i in range(userCount):
    recommendations.append(depth_limited_search(associationGraph, searchThreshold, i))
if(DEBUGGING):
    print("Recommendations created.", time.time() - START_TIME)

recommendationGraph = WeightedGraph(userCount)
for i in range(len(recommendations)):
    for j in recommendations[i]:
        recommendationGraph.adj_matrix[i][j] = 1
if(DEBUGGING):
    print("Recommendation graph created.", time.time() - START_TIME)
    print()    
evaluation = evaluate(interestSpace, recommendationGraph, searchThreshold)

print(evaluation)
if(DEBUGGING):
    print(time.time() - START_TIME)