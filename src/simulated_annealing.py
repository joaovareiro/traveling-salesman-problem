from sys import argv
import random

import helper


FILE_PATH = argv[1]
TEMPERATURE_MAX = int(argv[2])
COOLING_RATE = float(argv[3])
NUMBER_OF_ITERATIONS = int(argv[4])
TEMPERATURE_MIN = int(argv[5])


def main():
    coordinates = helper.read_data(FILE_PATH)
    solution, value = simulated_annealing(coordinates)

    print(f"Melhor caminho encontrado para {FILE_PATH}: {solution}")
    print(f"Melhor avaliação encontrada para {FILE_PATH}: {value}")
    print()


def simulated_annealing(coordinates):
    temperature = TEMPERATURE_MAX

    best_solution = list(coordinates.keys())
    random.shuffle(best_solution)
    best_value = helper.evaluate_solution(best_solution, coordinates)

    while temperature > TEMPERATURE_MIN:
        current_iteration = 0

        while current_iteration != NUMBER_OF_ITERATIONS:
            vertex1 = random.randint(0, len(best_solution) - 1)
            vertex2 = random.randint(0, len(best_solution) - 1)
            new_solution = helper.get_neighbour(best_solution, min(vertex1, vertex2), max(vertex1, vertex2))
            new_value = helper.evaluate_solution(new_solution, coordinates)

            if new_value < best_value:
                best_solution, best_value = new_solution, new_value
            else:
                if random.random() < helper.probability_of_accepting_inferior_answer(temperature, best_value, new_value):
                    best_solution, best_value = new_solution.copy(), new_value

            current_iteration += 1
            
        temperature = COOLING_RATE * temperature
    
    return best_solution, best_value


if __name__ == "__main__":
    main()