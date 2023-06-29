from sys import argv
import random

import helper


FILE_PATH = argv[1]
NUMBER_OF_ITERATIONS = int(argv[2])
OUTPUT_PATH = FILE_PATH.replace("input", "output/HC")

def main():
    coordinates = helper.read_data(FILE_PATH)
    solution, value = hill_climbing(coordinates)

    helper.hc_save_results(OUTPUT_PATH, solution, value, NUMBER_OF_ITERATIONS)


def hill_climbing(coordinates):
    current_iteration = 0
    best_solution = list(coordinates.keys())
    random.shuffle(best_solution)
    best_value = helper.evaluate_solution(best_solution, coordinates)

    while current_iteration < NUMBER_OF_ITERATIONS:
        is_local_best = False

        local_best_solution = list(coordinates.keys())
        random.shuffle(local_best_solution)
        local_best_value = helper.evaluate_solution(local_best_solution, coordinates)

        while not is_local_best:
            neighbors = helper.get_all_neighbors(local_best_solution)
            best_neighbor, best_neighbor_value = helper.get_best_neighbor(neighbors, coordinates)

            if best_neighbor_value < local_best_value:
                local_best_solution, local_best_value = best_neighbor, best_neighbor_value
            else:
                is_local_best = True

        current_iteration += 1

        if local_best_value < best_value:
            best_solution, best_value = local_best_solution, local_best_value

    return best_solution, best_value

if __name__ == "__main__":
    main()