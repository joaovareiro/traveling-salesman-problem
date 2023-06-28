import math
from sys import argv
import random

TEMPERATURE_MAX = int(argv[2])
COOLING_RATE = float(argv[3])
NUMBER_OF_ITERATIONS = int(argv[4])
TEMPERATURE_MIN = int(argv[5])

def read_data(file_path):
    data = {}
    file = open(file_path, 'r')
    for line in file:
        line_data = line.rstrip().split()
        id = int(line_data[0]) - 1
        coordinates = (int(line_data[1]), int(line_data[2]))
        data[id] = coordinates
    file.close()
    return data


def generate_neighbour(solution, first_vertex_index, second_vertex_index):
    neighbour = solution.copy()

    for i in range(0, first_vertex_index - 1):
        neighbour[i] = solution[i]
    for i in range(first_vertex_index, second_vertex_index + 1):
        neighbour[i] = solution[second_vertex_index - i + first_vertex_index]
    for i in range(second_vertex_index + 1, len(solution)):
        neighbour[i] = solution[i]
    
    return neighbour


def calculate_distance(current_vertex, next_vertex):
    x1, y1 = current_vertex
    x2, y2 = next_vertex
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def evaluate_solution(solution, coordinates):
    total_distance = 0
    for vertex_index in range(len(solution) - 1):
        current_vertex = solution[vertex_index]
        next_vertex = solution[vertex_index + 1]
        total_distance += calculate_distance(coordinates[current_vertex], coordinates[next_vertex])
    return total_distance


def probability(temperature, current_value, new_value):
    euler_number = math.e
    result = euler_number * ((current_value - new_value)/temperature)
    return result


# get input file path from argv
file_path = argv[1]
# read data from file
coordinates = read_data(file_path)
# define best solution as random order of vertices
best_solution = list(coordinates.keys())
random.shuffle(best_solution)
# evaluate initial solution
best_value = evaluate_solution(best_solution, coordinates)

# define initial temperature to a high value
temperature = TEMPERATURE_MAX

while temperature > TEMPERATURE_MIN:
    current_iteration = 0
    while current_iteration != NUMBER_OF_ITERATIONS:
        vertex1 = random.randint(0, len(best_solution) - 1)
        vertex2 = random.randint(0, len(best_solution) - 1)
        new_solution = generate_neighbour(best_solution, min(vertex1, vertex2), max(vertex1, vertex2))
        new_value = evaluate_solution(new_solution, coordinates)
        if new_value < best_value:
            best_solution, best_value = new_solution.copy(), new_value
        else:
           if random.random() < probability(temperature, best_value, new_value):
               best_solution, best_value = new_solution.copy(), new_value
        current_iteration += 1
    temperature = COOLING_RATE * temperature

# TODO: write to file, in order to keep a history

for i in range(len(best_solution)):
    print(best_solution[i], end=" ")
print(best_value)