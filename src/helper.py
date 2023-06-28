import math
import random

def read_data(file_path):
    data = {}
    with open(file_path, "r") as file:
        for line in file:
            line_data = line.rstrip().split()
            id = int(line_data[0]) - 1
            coordinates = (int(line_data[1]), int(line_data[2]))
            data[id] = coordinates
    return data


def calculate_distance(current_vertex, next_vertex):
    current_vertex_x, current_vertex_y = current_vertex
    next_vertex_x, next_vertex_y = next_vertex
    distance = math.sqrt((next_vertex_x - current_vertex_x) ** 2 + (next_vertex_y - current_vertex_y) ** 2)
    return distance


def evaluate_solution(solution, coordinates):
    total_distance = 0
    for vertex_index in range(len(solution) - 1):
        current_vertex = solution[vertex_index]
        next_vertex = solution[vertex_index + 1]
        total_distance += calculate_distance(coordinates[current_vertex], coordinates[next_vertex])
    return total_distance


def get_best_neighbour(neighbours, coordinates):
    best_neighbour = neighbours[0]
    best_neighbour_value = evaluate_solution(best_neighbour, coordinates)

    for index in range(1, len(neighbours)):
        neighbour = neighbours[index]
        neighbour_value = evaluate_solution(neighbour, coordinates)

        if neighbour_value < best_neighbour_value:
            best_neighbour, best_neighbour_value = neighbour, neighbour_value

    return best_neighbour, best_neighbour_value


def get_neighbour(solution, first_vertex_index, second_vertex_index):
    neighbour = solution.copy()

    for i in range(0, first_vertex_index):
        neighbour[i] = solution[i]
    for i in range(first_vertex_index, second_vertex_index + 1):
        neighbour[i] = solution[second_vertex_index - i + first_vertex_index]
    for i in range(second_vertex_index + 1, len(solution)):
        neighbour[i] = solution[i]
    
    return neighbour


def get_all_neighbours(solution):
    neighbours = []

    for i in range(1, len(solution) - 1):
        neighbours.append(get_neighbour(solution, 0, i))

    for i in range(1, len(solution) - 1):
        for j in range(i + 1, len(solution)):
            neighbours.append(get_neighbour(solution, i, j))

    return neighbours


def get_random_neighbour(solution):
    neighbours = get_all_neighbours(solution)
    neighbour = neighbours[random.randint(0, len(solution)-1)]
    return neighbour


def probability_of_accepting_inferior_answer(temperature, current_value, new_value):
    euler_number = math.e
    result = euler_number * ((current_value - new_value)/temperature)
    return result


def will_accept_inferior_answer(temperature, best_value, new_value):
    return random.random() < probability_of_accepting_inferior_answer(temperature, best_value, new_value)
