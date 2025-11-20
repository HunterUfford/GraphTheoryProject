import random

def setSeed(seed):
    random.seed(seed)

def pointGen(dimension):
    output = []
    for i in range(dimension):
        output.append(random.random())
    return output

def pointSetGen(pointCount, dimension):
    output = []
    for i in range(pointCount):
        output.append(pointGen(dimension))
    return output