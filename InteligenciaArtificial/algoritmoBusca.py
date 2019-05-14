from Grafo import*
import math
from termcolor import colored


# Busca em Profundidade
def algoritmo_dfs(grafo, estadoInicial, estadoFinal, caminhoVisitado = None):

    if caminhoVisitado is None:
        caminhoVisitado = [estadoInicial]

    if estadoInicial == estadoFinal:
        return caminhoVisitado

    for i in grafo[estadoInicial]:

        if i not in caminhoVisitado:
            if estadoFinal not in caminhoVisitado:
                caminhoVisitado = algoritmo_dfs(grafo, i, estadoFinal, caminhoVisitado + [i])

    return caminhoVisitado


# Busca em Largura
def bfs_algoritm(grafo, estadoInicial,estadoFinal):
    # Acompanha todos os nós visitados
    visitados = []
    # Acompanha os nós a serem verificados
    fila = [estadoInicial]

    # manter o loop até que haja nós ainda a serem verificados
    while fila:
       # remove primeiro no da fila
        node = fila.pop(0)

        # adicionar vizinhos do nó à fila
        if node not in visitados:
            visitados.append(node)
            vizinhos = grafo[node]
            for proximo in vizinhos:
                fila.append(proximo)

        if node == estadoFinal:

            return visitados

#Função Heurística para o o Pathfinder : F(n) = H(n) + G(n)
def heuristica(grafo, origem, objetivo, cidadesOrdem, matrizDistancia, cidadesVisitadas):

    min_heu = math.inf
    tempCidade = None

    for cidade in grafo[origem]:
        distancia_heu = None
        atual = None #armazena a posição(da cidade) na coluna do csv
        destino = None #armazena a posição(da cidade) na linha do csv

        #Calcula a distância em Linha reta da Cidade atual até o Destino. H(n)
        for i in range(len(cidadesOrdem)):
            print(cidade == cidadesOrdem[i])

            if cidade == cidadesOrdem[i]:
                atual = i

            if objetivo == cidadesOrdem[i]:
                destino = i

        if matrizDistancia[atual][destino] is None:
            distancia_heu = matrizDistancia[destino][atual]
        else:
            distancia_heu = matrizDistancia[atual][destino]


      #F(n) =          H(n): Custo para ir até o nó                   +         G(n): Custo para alcançar o nó
        f_n = grafo[origem][cidade]['weight'] + distancia_heu

        if f_n < min_heu and (cidade not in cidadesVisitadas):
            min_heu = f_n
            tempCidade = cidade

    return tempCidade


#Algoritmo de A*
def aEstrela(grafo, origem, objetivo, cidadesOrdem, matrizDistancia, cidadesVisitadas = None):
    if cidadesVisitadas is None:
        cidadesVisitadas = [estadoInicial]

    if origem == objetivo:
        return cidadesVisitadas

    proxCidade = heuristica(grafo,origem, objetivo, cidadesOrdem, matrizDistancia, cidadesVisitadas)

    return aEstrela(grafo, proxCidade, objetivo, cidadesOrdem, matrizDistancia, cidadesVisitadas + [proxCidade])

# Printa a Rota feita pelo algoritmo escolhido
def mostrarRota(busca):

    for i in range(len(busca)):
        if i == 0:
            print(colored(str(i + 1) + '- ' + busca[i], 'green'))
        elif i == len(busca) - 1:
            print(colored(str(i + 1) + '- ' + busca[i], 'red'))
        else:
            print(colored(str(i + 1) + '- ' + busca[i], 'yellow'))


def showGrafo(grafo, busca):
    pos = nx.fruchterman_reingold_layout(grafo)
    plt.axis('off')
    nx.draw_networkx_nodes(grafo, pos, node_size=180, node_color='violet')
    nx.draw_networkx_edges(grafo, pos, alpha=0.8)
    nx.draw_networkx_labels(grafo, pos, font_size=9)

    vertices = [(busca[n], busca[n + 1]) for n in range(len(busca) - 1)]
    nx.draw_networkx_edges(grafo, pos=pos, edgelist=vertices, edge_color='blue', width=4.0,
                           alpha=0.5)  #
    nx.draw_networkx_nodes(grafo, pos, nodelist=[busca[0]], node_size=80,
                           node_color='green')
    nx.draw_networkx_nodes(grafo, pos, nodelist=[busca[-1]], node_size=80, node_color='red')
    plt.show()


#Chamadas de funções do Grafo

grafo = Grafo()
ordenacaoCidades, matDistancia = heuristicaDistancia()


while True:

    escolhaBusca =int(input(colored("Escolha qual Algoritmo de Busca \n1- Busca em Profundidade\n2- Busca em Largura\n3-Pathfinder(A*)\n10- Finalizar\n", 'blue')))

    if escolhaBusca == 1:
        estadoInicial = input("Origem: \n")
        if estadoInicial not in var:
            print(colored('Cidade origem inválida', 'blue'))

        estadoFinal = input("Destino: \n")
        if estadoFinal not in var:
            print("Cidade destino inválida")
        busca = algoritmo_dfs(var,estadoInicial, estadoFinal)
        mostrarRota(busca)
        showGrafo(grafo,busca)

    elif escolhaBusca == 2:
        estadoInicial = input("Origem: \n")
        if estadoInicial not in var:
            print('Cidade origem inválida')

        estadoFinal = input("Destino: \n")
        if estadoFinal not in var:
            print("Cidade destino inválida")

        busca= bfs_algoritm(var, estadoInicial,estadoFinal)
        mostrarRota(busca)
        showGrafo(grafo, busca)
    if escolhaBusca == 3:
        estadoInicial = input("Origem: \n")
        if estadoInicial not in grafo:
            print('Cidade origem inválida')

        estadoFinal = input("Destino: \n")
        if estadoFinal not in grafo:
            print("Cidade destino inválida")

        busca = aEstrela(grafo, estadoInicial, estadoFinal,ordenacaoCidades, matDistancia)
        mostrarRota(busca)
        showGrafo(grafo, busca)
    elif escolhaBusca == 10:
        break


#Referências Bibliográficas

#https://www.python-course.eu/networkx.php
#https://www.programiz.com/dsa/graph-bfs
#https://networkx.github.io/documentation/stable/tutorial.html
#['Fagaras', 'Sibiu', 'Bucharest', 'Arad', 'Oradea', 'Rimnicu-Vilcea', 'Pitesti', 'Urziceni', 'Giurgiu', 'Zerind', 'Timisoara', 'Craiova']
#https://pythoninwonderland.wordpress.com/2017/03/18/how-to-implement-breadth-first-search-in-python/
