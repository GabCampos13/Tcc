import csv
from time import clock
import gc
import networkx as nx
import matplotlib.pyplot as plt
import math, pickle
from networkx.readwrite import json_graph

G = nx.MultiGraph() #Criador do grafo
P = nx.MultiGraph() 

#23:13 - 7:46 2600000

#def leituraInicial():
  #existentes = [] #Quais vertices ja foram adicionados no grafo
  #with open("koln-pruned.tr", "r") as f:
    #reader = csv.reader(f,delimiter=" ")
    #for line in reader:
      #if(line[1] not in existentes):
        #G.add_node(line[1]) # vai criando os vertices
        #existentes.append(line[1])
        #print(line[0],"---",line[1])


def leituraTempo(pos):
  with open("Teste.txt", "r") as f:               #Abre o primeiro CSV
    i = 0
    #f.seek(1557548688)
    #linha = f.readline()
    #print(float(linha.split(" ")[0]))
    linha = f.readline()
    i += 1
    while(linha):
      if(i%2972 == 0):
        print(f.tell())
      linha = f.readline()
      i+=1
    #print("Quantidade de linhas: ",i)
    
def leituraArestas(pos):
  save = [] 
  i = 1

  with open("1kkTeste.txt", "r") as f:               #Abre o primeiro CSV
    if(i == 1):
      f.seek(pos)
      linha = f.readline()
      print(linha)
    z = open("1kkTeste.txt")                         #Abre o segundo CSV
    c = csv.reader(z,delimiter = " ")
    while(linha):              #Comeca a ler do primeiro CSV o valor
      if(i == 1000000): #Time 1kk -> 1697sec
        print(pos)
        break
      pos = f.tell()
      z.seek(pos)
      if(i%100 == 0):
        print("linha: ",i)
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

def save_graph(graph, filename):
  pickle.dump(graph, open(filename , 'wb'))

if __name__ == "__main__":
  #leituraInicial()
  pos = 0
  cont = 1
  start = clock()
  #pos = leituraArestas(pos)
  leituraTempo(pos)
  #print(G.edges.data("tempo"))
  #for x in G.edges.data("tempo"):
    #if(float(x[2][0]) - float(x[2][1]) != 0):
      #P.add_edge(x[0],x[1],tempo = (x[2][0],x[2][1]))
   #print("O vertice: ",x[0]," junto com o vertice: ",x[1], "passaram a menos de 200 metros comecando no instante: ",x[2][0], "e terminaram no instante: ",x[2][1])
  #printVertices()
  #for x in P.edges.data("tempo"):
    #print("O vertice: ",x[0]," junto com o vertice: ",x[1], "passaram a menos de 100 metros comecando no instante: ",x[2][0], "e terminaram no instante: ",x[2][1])
  #save_graph(P.edges.data("tempo"),"Cologne")
  end = clock()
  print("Final tempo: ",end-start)

