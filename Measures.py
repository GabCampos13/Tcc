import csv
import time
import gc
import networkx as nx
import matplotlib.pyplot as plt
import math, pickle
from networkx.readwrite import json_graph
import sys

G = nx.Graph()
M = nx.Graph()

def leituraArestas(pos):
   save = [] 
   #Atemporal Metrics
   grauVert = []
   densityGraph = []
   Centrality = []
   Assortativity = []
   Clusterizacao = []
   GrauMedio = [] #NumberOfEdges *2 / NumberOfNodes
   i = 1
   with open("Teste.txt", "r") as f:               #Abre o primeiro CSV
      t = open("Measures.txt","a")
      if(i == 1):
         f.seek(pos)
         linha = f.readline()
         TimeSkip = float(linha.split(" ")[0])

      z = open("Teste.txt")                         #Abre o segundo CSV
      c = csv.reader(z,delimiter = " ")
      while(linha):              #Comeca a ler do primeiro CSV o valor
         pos = f.tell()
         z.seek(pos)
         if(TimeSkip < float(linha.split(" ")[0])):
            if(M.number_of_nodes() != 0):
               TimeSkip = float(linha.split(" ")[0])
               Gmed = (2*M.number_of_edges())/M.number_of_nodes()
               Var = (TimeSkip-1,round(nx.density(M),4),round(nx.degree_assortativity_coefficient(M),4),round(nx.average_clustering(M),4),round(Gmed,4))
               t.write("Tempo do dia: "+str(Var[0])+" Densidade: "+str(Var[1])+" Assortatividade: "+str(Var[2])+ " Clusterizacao: "+str(Var[3])+ " Grau medio: "+str(Var[4])+" Numero de arestas: "+M.number_of_edges\n")
               t = open("GrauClust.txt","a")
               for x in M.nodes:
                  t.write("Vertice: "+str(x)+" Grau dele: "+str(M.degree[x])+" Clusterização: "+str(nx.clustering(M,x))+"\n")
                  # print("Vertice: ",x," Grau dele: ",G.degree[x]," Clusterização: ",nx.clustering(G,x))
               t.close()
               t = open("Bridges.txt","a")
               for bridge in list(nx.bridges(G)):
                  t.write(str(bridge)+"\n")
               t.close()
               t = open("Pearlson.txt","a")
               t.write("Coeficiente de Pearson: "+str(nx.degree_pearson_correlation_coefficient(G)))
               t.close()
               M.clear()
               Gmed = 0
               Var = []
            #print(TimeSkip)
         if(i == (24000)):     #TEM Q ESTAR DIVIDO PELA QNTD DE THREADS   46167992/8        tempo 1kk linha -> 673.6 
            print(densityGraph)    
         break
         if((0+i)%100 == 0):
            print("linha: ",(0+i))
         i += 1
         for ok in c:                   #Comeca a ler do segundo CSV ate passar do tempo do CSV anterior
            if(float(ok[0]) > float(linha.split(" ")[0])):
               break
            if(linha.split(" ")[2] != ok[2] and linha.split(" ")[3] != ok[3]):
                if(euclidiana(float(linha.split(" ")[2]),float(linha.split(" ")[3]),float(ok[2]),float(ok[3])) < 100):# Verificador de distancia (<100metros)
                    G.add_edge(linha.split(" ")[1],ok[1],tempo = ((linha.split(" ")[0]),(ok[0]))) #Cria a aresta pela primeira vez
         linha = f.readline()
         z.seek(0)

      #for x in G.nodes:
         #print("Vertice: ",x," Grau dele: ",G.degree[x]," Clusterização: ",nx.clustering(G,x))
      print("Quantidade de componentes: ",nx.number_connected_components(G))
      #print("Diametro: ",nx.diameter(G)) Grafo nao é conectad, logo é impossivel
      i = 1
      max = 0
      print("Coeficiente de Pearson: ",nx.degree_pearson_correlation_coefficient(G))
      #for g in nx.connected_component_subgraphs(G):
         #print("Distancia dos componentes",i,": ",nx.average_shortest_path_length(g))
         #i+=1
      #print(nx.has_bridges(G))
      #print("Pontes no grafo: ",list(nx.bridges(G)))
      #largest_components=sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
      #for index,component in enumerate(largest_components):
         #nx.draw(component)
         #plt.show()


def euclidiana(x1,y1,x2,y2):#Euclidiana

   soma = (x1-x2)**2 + (y1-y2)**2
   final = math.sqrt(soma)
   return final

def Posicoes():
   G = nx.Graph()
   i = 0
   with open("Teste.txt", "r") as f:               #Abre o primeiro CSV
      linha = f.readline()
      z = open("Teste.txt")                         #Abre o segundo CSV
      c = csv.reader(z,delimiter = " ")
      f.seek(pos)
      while(linha):              #Comeca a ler do primeiro CSV o valor
         #print(float(linha.split(" ")[0]))
         if((float(linha.split(" ")[0]) - 28200) == 600):
           # print("entrei")
            print(f.tell())
            break
         #if(i%100 == 0):
            #print("linha: ",i)   
         #i = i + 1
         linha = f.readline()


def printVertices(): #Metodo para printar o grafo
   nx.draw(G,with_labels = True)
   plt.show() 


if __name__ == "__main__":
   pos = 0
   leituraArestas(pos)
   #Posicoes()
   #printVertices()
