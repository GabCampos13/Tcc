import csv
import networkx as nx
import matplotlib.pyplot as plt
import math, pickle
from networkx.readwrite import json_graph

G = nx.MultiGraph() 

def printVertices(): #Metodo para printar o grafo
  nx.draw(G,with_labels = True)
  plt.show() 

if __name__ == "__main__":
  z = open("Arestas_Salvas.txt")                         #Abre o segundo CSV
  c = csv.reader(z,delimiter = "-")
  for linha in c:
    #print("O vertice: ",linha[0]," junto com o vertice: ",linha[1], "passaram a menos de 100 metros comecando no instante: ",linha[2], "e terminaram no instante: ",linha[3])
    G.add_edge(linha[0],linha[1],tempo=(linha[2],linha[3])) 
  #printVertices()
  for x in G.edges.data("tempo"):
    print("O vertice: ",x[0]," junto com o vertice: ",x[1], "passaram a menos de 100 metros comecando no instante: ",x[2][0], "e terminaram no instante: ",x[2][1])
