import csv
import time
import multiprocessing 
import gc
import networkx as nx
import matplotlib.pyplot as plt
import math
from networkx.readwrite import json_graph
import sys

G = nx.MultiGraph() #Criador do grafo principal
P = nx.MultiGraph() #escrita do grafo principal num arquivo de texto

def leituraArestas(pos,valor):
   M = nx.Graph() #Metricas Atemporais
   save = [] 
   i = 1
   with open("Teste.txt", "r") as f:               #Abre o primeiro CSV
      if(i == 1):
         t = open("Measures"+str(valor)+".txt","a")
         f.seek(pos)
         linha = f.readline()
         TimeSkip = float(linha.split(" ")[0])
      z = open("Teste.txt")                         #Abre o segundo CSV
      c = csv.reader(z,delimiter = " ")
      while(linha):              #Comeca a ler do primeiro CSV o valor
         if(i == (2972)):     #TEM Q ESTAR DIVIDO PELA QNTD DE THREADS           tempo 1kk linha -> 673.6     
            break
         pos = f.tell()
         z.seek(pos)
         if(TimeSkip < float(linha.split(" ")[0])):
            if(M.number_of_nodes() != 0):
               TimeSkip = float(linha.split(" ")[0])
               Gmed = (2*M.number_of_edges())/M.number_of_nodes()
               Var = (TimeSkip,round(nx.density(M),4),round(nx.degree_assortativity_coefficient(M),4),round(nx.average_clustering(M),4),round(Gmed,4))
               t.write("Tempo do dia: "+str(Var[0])+" Densidade: "+str(Var[1])+" Assortatividade: "+str(Var[2])+ " Clusterizacao: "+str(Var[3])+ " Grau medio: "+str(Var[4])+" Numero de arestas: "+str(M.number_of_edges())+" Numero de vertices: "+str(M.number_of_nodes())+"\n")
               t.close()
               t = open("GrauClust"+str(valor)+".txt","a")
               for x in M.nodes:
                  t.write("Tempo do dia: "+str(Var[0])+" Vertice: "+str(x)+" Grau dele: "+str(M.degree[x])+" Clusterizacao: "+str(nx.clustering(M,x))+"\n")
                  # print("Vertice: ",x," Grau dele: ",G.degree[x]," Clusterização: ",nx.clustering(G,x))
               t.close()
               t = open("Bridges"+str(valor)+".txt","a")
               t.write("Tempo do dia: "+str(Var[0])+" Quantidade de Pontes: "+str(len(list(nx.bridges(M))))+"\n")
               t.close()
               Gmed = 0
               Var = []               
               M.clear()
         if((0+i)%100 == 0):
            print("linha: ",(0+i))
         i += 1
         for ok in c:                   #Comeca a ler do segundo CSV ate passar do tempo do CSV anterior
            if(float(ok[0]) > float(linha.split(" ")[0])):
               break
            if(linha.split(" ")[0] == ok[0] and linha.split(" ")[1] != ok[1]): #Se os 2 CSVS estao no mesmo tempo e sao vertices diferentes
               if(G.has_edge(linha.split(" ")[1],ok[1])):        #Se ja existe aresta entre esses 2 pontos
                  if(euclidiana(float(linha.split(" ")[2]),float(linha.split(" ")[3]),float(ok[2]),float(ok[3])) < 100):  # Verificador de distancia (<100metros)
                     for x in G.edges.data("tempo"):  
                        True     # Le todas as arestas ja salvas
                     save.append(linha.split(" ")[1])
                     save.append(ok[1])
                     save.append(linha.split(" ")[0])
                     G.remove_edge(linha.split(" ")[1],ok[1])  #Remove a aresta antiga
                     G.add_edge(save[0],save[1],tempo =(x[2][0],save[2])) # E atualiza com o novo valor
                     save = [] #Limpa o vetor de salvacao das arestas
               elif((not(G.has_edge(linha.split(" ")[1],ok[1]))) or (G.has_edge(linha.split(" ")[1],ok[1]))):         #Caso as arestas ainda nao existem
                  if(linha.split(" ")[2] != ok[2] and linha.split(" ")[3] != ok[3]):
                     if(euclidiana(float(linha.split(" ")[2]),float(linha.split(" ")[3]),float(ok[2]),float(ok[3])) < 100):# Verificador de distancia (<100metros)
                        G.add_edge(linha.split(" ")[1],ok[1],tempo = ((linha.split(" ")[0]),(ok[0]))) #Cria a aresta pela primeira vez
                        M.add_edge(linha.split(" ")[1],ok[1],tempo = ((linha.split(" ")[0]),(ok[0])))
         linha = f.readline()
         z.seek(0) 
         save = []   

def printVertices(): #Metodo para printar o grafo
   nx.draw(G,with_labels = True)
   plt.show() 

def euclidiana(x1,y1,x2,y2):#Euclidiana ou manhatan??

   soma = (x1-x2)**2 + (y1-y2)**2
   final = math.sqrt(soma)
   return final

if __name__ == "__main__":
   pos = int(sys.argv[1])
   if(int(sys.argv[1]) == 0):
      valor = 0
   if(int(sys.argv[1]) == 171700):
      valor = 1
   if(int(sys.argv[1]) == 344463):
      valor = 2
   if(int(sys.argv[1]) == 517631):
      valor = 3
   #print(pos)
   cont = 1
   start = time.time()
   leituraArestas(pos,valor)
   for x in G.edges.data("tempo"):
      if(float(x[2][0]) - float(x[2][1]) != 0):
         P.add_edge(x[0],x[1],tempo = (x[2][0],x[2][1]))
   #printVertices()
   print(str(valor))
   t = open("Arestas_Salvas"+str(valor)+".txt","a")
   for x in P.edges.data("tempo"):
      if(float(x[2][1]) - float(x[2][0]) > 1):
         t.write(x[0]+" - "+x[1]+ " - "+x[2][0]+ " - "+x[2][1]+"\n")
   t.close()
   end = time.time()
   print("Final tempo: ",end-start)