import random
import math

def calcular_distancia(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def avaliacao(caminho, coordenadas):
    distancia_total = 0
    for i in range(len(caminho) - 1):
        cidade_atual = caminho[i]
        prox_cidade = caminho[i + 1]
        distancia_total += calcular_distancia(
            coordenadas[cidade_atual], coordenadas[prox_cidade]
        )
    return distancia_total


def gerar_vizinhos(caminho):
    vizinhos = []
    for i in range(len(caminho)):
        for j in range(i + 1, len(caminho)):
            vizinho = caminho[:]
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            vizinhos.append(vizinho)
    return vizinhos


def hill_climbing(caminho, coordenadas, dataset):
    MAX_ITERACOES = 1000
    t = 0
    melhor = caminho
    melhor_avaliacao = avaliacao(caminho, coordenadas)
    historico_avaliacoes = []

    while t < MAX_ITERACOES:
        local = "F"
        aval_caminho = avaliacao(caminho, coordenadas)

        vizinhos = gerar_vizinhos(caminho)

        encontrou_melhor = False
        for vizinho in vizinhos:
            aval_vizinho = avaliacao(vizinho, coordenadas)
            if aval_vizinho < aval_caminho:
                caminho = vizinho
                local = "V"
                encontrou_melhor = True
                break

        if not encontrou_melhor:
            break

        t += 1

        if avaliacao(caminho, coordenadas) < melhor_avaliacao:
            melhor = caminho
            melhor_avaliacao = avaliacao(caminho, coordenadas)

        historico_avaliacoes.append((t, melhor_avaliacao, melhor))

        print(f"Iteração {t}: Melhor Avaliação = {avaliacao(melhor, coordenadas)}")

    return melhor, melhor_avaliacao, historico_avaliacoes


def carregar_coordenadas(nome_arquivo):
    coordenadas = {}
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            cidade, x, y = linha.split()
            coordenadas[int(cidade) - 1] = (float(x), float(y))
    return coordenadas


def salvar_melhor_solucao(melhor_caminho, melhor_avaliacao, dataset):
    nome_arquivo = f"best_solution_{dataset}.txt"
    with open(nome_arquivo, "w") as arquivo:
        arquivo.write("Melhor Caminho\n")
        arquivo.write(f"{melhor_caminho}\n")
        arquivo.write("Melhor Avaliação\n")
        arquivo.write(f"{melhor_avaliacao}\n")


def salvar_historico_avaliacoes(historico_avaliacoes, dataset):
    nome_arquivo = f"iterations_{dataset}.txt"
    with open(nome_arquivo, "w") as arquivo:
        arquivo.write("Iteração\tMelhor Avaliação\tMelhor Caminho\n")
        for iteracao, avaliacao, caminho in historico_avaliacoes:
            arquivo.write(f"{iteracao}\t\t{avaliacao}\t\t{caminho}\n")


datasets = ["att48.tsp", "berlin52.tsp", "bier127.tsp", "eil76.tsp","kroA100.tsp", "kroE100.tsp", "pr76.tsp", "rat99.tsp", "st70.tsp"]
N_REPETICOES = 300

for dataset in datasets:
    melhor_global = None
    melhor_avaliacao_global = float("inf")
    historico_avaliacoes_global = []

    for _ in range(N_REPETICOES):
        nome_arquivo = dataset
        coordenadas = carregar_coordenadas(nome_arquivo)

        caminho = list(coordenadas.keys())
        random.shuffle(caminho)

        melhor_caminho, melhor_avaliacao, historico_avaliacoes = hill_climbing(
            caminho, coordenadas, dataset
        )

        if melhor_avaliacao < melhor_avaliacao_global:
            melhor_global = melhor_caminho
            melhor_avaliacao_global = melhor_avaliacao
            historico_avaliacoes_global = historico_avaliacoes

        print(f"Melhor caminho encontrado para {dataset}: {melhor_caminho}")
        print(f"Melhor avaliação encontrada para {dataset}: {melhor_avaliacao}")
        print()

    salvar_melhor_solucao(melhor_global, melhor_avaliacao_global, dataset)
    salvar_historico_avaliacoes(historico_avaliacoes_global, dataset)

    print(f"Melhor solução global para {dataset} salva no arquivo 'best_solution_{dataset}.txt'")
    print(f"Histórico das melhores avaliações para {dataset} salvo no arquivo 'iterations_{dataset}.txt'")
    print()
