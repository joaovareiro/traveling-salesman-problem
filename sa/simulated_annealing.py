import math
from sys import argv
import random

# TODO: rename variables, functions, etc to snake_case

TEMPERATURE_MAX = 10
COOLING_RATE = 0.95
NUMBER_OF_ITERATIONS = 20
TEMPERATURE_MIN = 5

def readData(filePath):
    vertexList = {}
    file = open(filePath, 'r')
    for line in file:
        data = line.rstrip().split()
        id = int(data[0]) - 1
        coordinates = (int(data[1]), int(data[2]))
        vertexList[id] = coordinates
    file.close()
    
    return vertexList


def generateNeighbour(solution, vertex1Index, vertex2Index):
    neighbour = solution.copy()

    for i in range(0, vertex1Index - 1):
        neighbour[i] = solution[i]
    for i in range(vertex1Index, vertex2Index + 1):
        neighbour[i] = solution[vertex2Index - i + vertex1Index]
    for i in range(vertex2Index + 1, len(solution)):
        neighbour[i] = solution[i]
    
    return neighbour


def calculateDistance(currentVertex, nextVertex):
    x1, y1 = currentVertex
    x2, y2 = nextVertex
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def evaluateSolution(solution, coordinates):
    totalDistance = 0
    for vertexIndex in range(len(solution) - 1):
        currentVertex = solution[vertexIndex]
        nextVertex = solution[vertexIndex + 1]
        totalDistance += calculateDistance(coordinates[currentVertex], coordinates[nextVertex])
    return totalDistance


def probability(temperature, currentValue, newValue):
    eulerNumber = math.e
    result = eulerNumber * ((currentValue - newValue)/temperature)
    return result


# get input file path from argv
filePath = argv[1]
# read data from file
coordinates = readData(filePath)
bestSolution = list(coordinates.keys())
random.shuffle(bestSolution)
# evaluate initial solution
bestValue = evaluateSolution(bestSolution, coordinates)

# define initial temperature to a high value
temperature = TEMPERATURE_MAX

while temperature > TEMPERATURE_MIN:
    currentIteration = 0
    while currentIteration != NUMBER_OF_ITERATIONS:
        vertex1 = random.randint(0, len(bestSolution) - 1)
        vertex2 = random.randint(0, len(bestSolution) - 1)
        newSolution = generateNeighbour(bestSolution, min(vertex1, vertex2), max(vertex1, vertex2))
        newValue = evaluateSolution(newSolution, coordinates)
        if newValue < bestValue:
            bestSolution, bestValue = newSolution.copy(), newValue
        else:
           if random.random() < probability(temperature, bestValue, newValue):
               bestSolution, bestValue = newSolution.copy(), newValue
        currentIteration += 1
    temperature = COOLING_RATE * temperature

# TODO: write to file, in order to keep a history

for i in range(len(bestSolution)):
    print(bestSolution[i], end=" ")
print(bestValue)