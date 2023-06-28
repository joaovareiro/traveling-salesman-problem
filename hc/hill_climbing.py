import random
from sys import argv
import math

NUMBER_OF_ITERATIONS = int(argv[2])

def calculate_distance(current_vertex, next_vertex):
    x1, y1 = current_vertex
    x2, y2 = next_vertex
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def evaluateSolution(solution, coordinates):
    total_distance = 0
    for vertex_index in range(len(solution) - 1):
        current_vertex = solution[vertex_index]
        next_vertex = solution[vertex_index + 1]
        total_distance += calculate_distance(
            coordinates[current_vertex], coordinates[next_vertex]
        )
    return total_distance


def get_neighbour(solution, first_vertex_index, second_vertex_index):
    neighbour = solution.copy()

    for i in range(0, first_vertex_index - 1):
        neighbour[i] = solution[i]
    for i in range(first_vertex_index, second_vertex_index + 1):
        neighbour[i] = solution[second_vertex_index - i + first_vertex_index]
    for i in range(second_vertex_index + 1, len(solution)):
        neighbour[i] = solution[i]
    
    return neighbour


def generate_neighbours(solution):
    n = len(solution)
    neighbours = []

    for k in range(2, n-1):
        neighbours.append(get_neighbour(solution, 1, k))
    for i in range(2, n-1):
        for k in range(i+1, n):
            neighbours.append(get_neighbour(solution, i, k))

    return neighbours


def get_best_neighbour(neighbours, coordinates):
    best_neighbour = neighbours[0]
    best_neighbour_value = evaluateSolution(best_neighbour, coordinates)
    for neighbour in neighbours:
        neighbour_value = evaluateSolution(neighbour, coordinates)
        if neighbour_value < best_neighbour_value:
            best_neighbour, best_neighbour_value = neighbour, neighbour_value
    return best_neighbour, best_neighbour_value


def hill_climbing(vertices_keys, coordinates):
    current_iteration = 0
    # define best solution as random order of vertices
    best_solution = vertices_keys.copy()
    random.shuffle(best_solution)
    # evaluate best solution
    best_value = evaluateSolution(best_solution, coordinates)

    while current_iteration < NUMBER_OF_ITERATIONS:
        local_best = False
        # define local best solution as random order of vertices
        local_best_solution = vertices_keys.copy()
        random.shuffle(local_best_solution)
        # evaluate local best solution
        local_best_value = evaluateSolution(local_best_solution, coordinates)

        while not local_best:
            # generate neighbours
            neighbours = generate_neighbours(local_best_solution)
            # get best neighbour
            best_neighbour, best_neighbour_value = get_best_neighbour(neighbours, coordinates)

            # if neighbour is better than best, best = neighbour
            if best_neighbour_value < local_best_value:
                local_best_solution, local_best_value = best_neighbour, best_neighbour_value
            # else, local_best_solution is the local optimum
            else:
                local_best = True

        current_iteration += 1

        # if local_best is better than global_best, global_best = local_best
        if local_best_value < best_value:
            best_solution, best_value = local_best_solution, local_best_value

    return best_solution, best_value


def read_data(file_path):
    data = {}
    with open(file_path, "r") as file:
        for line in file:
            line_data = line.rstrip().split()
            id = int(line_data[0]) - 1
            coordinates = (int(line_data[1]), int(line_data[2]))
            data[id] = coordinates
    return data


file_path = argv[1]
coordinates = read_data(file_path)
vertices_keys = list(coordinates.keys())
solution, value = hill_climbing(
    vertices_keys, coordinates
)

print(f"Melhor caminho encontrado para {file_path}: {solution}")
print(f"Melhor avaliação encontrada para {file_path}: {value}")
print()
