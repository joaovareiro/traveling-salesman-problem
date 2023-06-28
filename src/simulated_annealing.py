from sys import argv
import random

import helper


FILE_PATH = argv[1]
TEMPERATURE_MAX = int(argv[2])
COOLING_RATE = float(argv[3])
NUMBER_OF_ITERATIONS = int(argv[4])
TEMPERATURE_MIN = int(argv[5])
OUTPUT_PATH = FILE_PATH.replace("input", "output/SA")


def main():
    coordinates = helper.read_data(FILE_PATH)
    solution, value = simulated_annealing(coordinates)

    helper.sa_save_results(OUTPUT_PATH, solution, value, TEMPERATURE_MAX, COOLING_RATE, NUMBER_OF_ITERATIONS, TEMPERATURE_MIN)


def simulated_annealing(coordinates):
    temperature = TEMPERATURE_MAX

    best_solution = list(coordinates.keys())
    random.shuffle(best_solution)
    best_value = helper.evaluate_solution(best_solution, coordinates)

    while temperature > TEMPERATURE_MIN:
        current_iteration = 0

        while current_iteration != NUMBER_OF_ITERATIONS:
            new_solution = helper.get_random_neighbour(best_solution)
            new_value = helper.evaluate_solution(new_solution, coordinates)

            if new_value < best_value:
                best_solution, best_value = new_solution, new_value
            else:
                if helper.will_accept_inferior_answer(best_value, new_value, temperature):
                    best_solution, best_value = new_solution.copy(), new_value

            current_iteration += 1
            
        temperature = COOLING_RATE * temperature
    
    return best_solution, best_value


if __name__ == "__main__":
    main()