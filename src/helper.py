import os
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


def get_best_neighbor(neighbors, coordinates):
    best_neighbor = neighbors[0]
    best_neighbor_value = evaluate_solution(best_neighbor, coordinates)

    for index in range(1, len(neighbors)):
        neighbor = neighbors[index]
        neighbor_value = evaluate_solution(neighbor, coordinates)

        if neighbor_value < best_neighbor_value:
            best_neighbor, best_neighbor_value = neighbor, neighbor_value

    return best_neighbor, best_neighbor_value


def get_neighbor(solution, first_vertex_index, second_vertex_index):
    neighbor = solution.copy()

    for i in range(0, first_vertex_index):
        neighbor[i] = solution[i]
    for i in range(first_vertex_index, second_vertex_index + 1):
        neighbor[i] = solution[second_vertex_index - i + first_vertex_index]
    for i in range(second_vertex_index + 1, len(solution)):
        neighbor[i] = solution[i]
    
    return neighbor


def get_all_neighbors(solution):
    neighbors = []

    for i in range(1, len(solution) - 1):
        neighbors.append(get_neighbor(solution, 0, i))

    for i in range(1, len(solution) - 1):
        for j in range(i + 1, len(solution)):
            neighbors.append(get_neighbor(solution, i, j))

    return neighbors


def get_random_neighbor(solution):
    vertex1 = random.randint(0, len(solution) - 1)
    vertex2 = random.randint(0, len(solution) - 1)
    new_solution = get_neighbor(solution, min(vertex1, vertex2), max(vertex1, vertex2))
    return new_solution


def probability_of_accepting_inferior_answer(temperature, current_value, new_value):
    euler_number = math.e
    result = euler_number * ((current_value - new_value)/temperature)
    return result


def will_accept_inferior_answer(temperature, best_value, new_value):
    return random.random() < probability_of_accepting_inferior_answer(temperature, best_value, new_value)


def write_solution_path(file, solution):
    for i in range(len(solution)):
            if i != len(solution) - 1:
                file.write(f"{solution[i] + 1} -> ")
            else:
                file.write(f"{solution[i] + 1}\n\n\n")


# Simulated Annealing
def sa_save_results(output_path, solution, value, temperature_max, cooling_rate, number_of_iterations, temperature_min):
    if not os.path.exists("output/SA"):
        os.makedirs("output/SA")

    with open(output_path, "a+") as file:
        file.write(f"""TEMPERATURE_MAX: {temperature_max}
COOLING_RATE: {cooling_rate}
NUMBER_OF_ITERATIONS: {number_of_iterations}
TEMPERATURE_MIN: {temperature_min}
""")
        file.write(f"\nVALUE: {value:.2f}\n")
        write_solution_path(file, solution)
                   

# Hill Climbing
def hc_save_results(output_path, solution, value, number_of_iterations):
    if not os.path.exists("output/HC"):
        os.makedirs("output/HC")

    with open(output_path, "a+") as file:
        file.write(f"NUMBER_OF_ITERATIONS: {number_of_iterations}\n")
        file.write(f"\nVALUE: {value:.2f}\n")
        write_solution_path(file, solution)