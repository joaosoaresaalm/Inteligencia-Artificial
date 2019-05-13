import networkx as nx
import matplotlib.pyplot as plt

def Grafo():
    
   cidades_csv = open('arestas.csv')
   G = nx.Graph()
   for j in cidades_csv:
       sep = j.split(',')
       sep[2] = sep[2].replace('\n', "")
       G.add_edge(sep[0], sep[1], weight=float(sep[2]))


   return G

def showGrafo(grafo):
    plt.figure(1, figsize=(12, 8))             #definindo o tamanho da figura
    pos=nx.fruchterman_reingold_layout(grafo)      #definindo o algoritmo do layout
    plt.axis('off')                            #retira as bordas
    nx.draw_networkx_nodes(grafo,pos,node_size=1000) #plota os nos
    nx.draw_networkx_edges(grafo,pos,alpha=0.8)    #plota as arestas
    plt.title('Cidades', size=16)     #Título
    plt.show()

def heuristicaDistancia():
    heuristica_csv = open('heuristicaDistancia.csv')
    matDistancia = []

    for j in heuristica_csv:
        sep = j.split(',')
        sep[len(sep) - 1] = sep[len(sep) - 1].replace('\n', '')
        sep.remove(sep[0])
        matDistancia.append(sep)

    ordenacaoCidades = matDistancia[0]
    matDistancia.remove(matDistancia[0])

    for i in range(len(matDistancia)):
        for j in range(len(matDistancia[i])):
            if j >= i:
                matDistancia[i][j] = float(matDistancia[i][j])
            else:
                matDistancia[i][j] = None

    return ordenacaoCidades, matDistancia


var = Grafo()
