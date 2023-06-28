from sys import argv
import random

import helper

NUMBER_OF_ITERATIONS = int(argv[2])

def main():
    file_path = argv[1]
    coordinates = helper.read_data(file_path)
    solution, value = hill_climbing(coordinates)

    print(f"Melhor caminho encontrado para {file_path}: {solution}")
    print(f"Melhor avaliação encontrada para {file_path}: {value}")
    print()

def hill_climbing(coordinates):
    current_iteration = 0
    # define best solution as random order of vertices
    best_solution = list(coordinates.keys())
    random.shuffle(best_solution)
    # evaluate best solution
    best_value = helper.evaluate_solution(best_solution, coordinates)

    while current_iteration < NUMBER_OF_ITERATIONS:
        local_best = False
        # define local best solution as random order of vertices
        local_best_solution = list(coordinates.keys())
        random.shuffle(local_best_solution)
        # evaluate local best solution
        local_best_value = helper.evaluate_solution(local_best_solution, coordinates)

        while not local_best:
            # generate neighbours
            neighbours = helper.get_all_neighbours(local_best_solution)
            # get best neighbour
            best_neighbour, best_neighbour_value = helper.get_best_neighbour(neighbours, coordinates)

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

if __name__ == "__main__":
    main()