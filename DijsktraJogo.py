import numpy as np
import math
import random
from collections import deque 

class Vertice:
  def __init__(self):
    self.adj = []
    self.d = math.inf
    self.pai = None
    self.tipo = 0
    '''
    Tipos:
    0 - Vazio
    1 - Obstáculo
    2 - Final
    '''
    
  def __str__(self):#Retorno de string para visualização dos tipos de quadros no terminal
    
    if self.tipo == 0:
      return "O"
    elif self.tipo == 1:
      return "X"
    elif self.tipo == 2:
      return "#"
       
    #return str(self.d)
    #return str(len(self.adj))
    
  def addArestas(self, vertice):
    if vertice not in self.adj:
      self.adj.append(vertice)
      if self not in vertice.adj:
        vertice.adj.append(self)
    
  def setTipo(self, n):#Define o tipo de um vértice
    match n:
      case 0:
        if self.tipo != 0:
          self.tipo = 0
      case 1:#Caso seja um quadrante de obstáculo, será retirado da lista de adjacência de seus vizinhos, e depois limpar a sua própria lista de adjacência
        if self.tipo != 1:
          self.tipo = 1
          for v in self.adj:
            v.adj.remove(self)
            
          self.adj.clear()
      case 2:
        if self.tipo != 2:
          self.tipo = 2
    

class Grafo:
  def __init__(self):
    self.grafo = np.empty((20, 10), dtype = Vertice)

  def criar_arestas(self):
    #Criação dos vértices 
    for i in range (20):
      for j in range (10):
        self.grafo[i][j] = Vertice()
        
        if i == 0:#Define a linha de chegada
          self.grafo[i][j].setTipo(2)

    #Criação das arestas
    for i in range (20):
      for j in range (10):
        v = self.grafo[i][j]
        if i > 0:
          v.addArestas(self.grafo[i-1][j])#Aresta acima
          
        if i < 19:
          v.addArestas(self.grafo[i+1][j])#Aresta abaixo
          
        if j > 0:
          v.addArestas(self.grafo[i][j-1])#Aresta da esquerda
          
        if j < 9:
          v.addArestas(self.grafo[i][j+1])#Aresta da direita
    
    self.definir_obstaculos()
          
          
  def definir_obstaculos(self):#Geração das linhas de obstáculos
    
    for i in range (20):
      lista = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]#lista onde as posições aleatórias dos espaços serão selecionados
      
      #Seleção dos dois espaços vazios
      a = random.choice(lista)
      lista.remove(a)
      b = random.choice(lista)
      for j in range (10):
        if i > 0 and i < 14 and i % 2 != 0:#cria linhas de obstáculos em todas as linhas pares a partir da sexta linha
          v = self.grafo[i][j]
          if j != a and j != b:
            self.grafo[i][j].setTipo(1)
          else:
            if v.tipo == 1:
              v.setTipo(0)#"restaura" o vertice, conectando-o com os vertices acima e abaixo
              v.addArestas(self.grafo[i+1][j])
              v.addArestas(self.grafo[i-1][j])

  def imprimir_grafo(self):
    print('Matriz: ')
    for i in range (20):
      for j in range (10):
        c = str(self.grafo[i][j])
        print (c, end=' ')
      print("\n")
      
  def relax(self, u,v):
    if v.d > u.d + 1:
      v.d = u.d + 1
      v.pai = u
  
  def resetar_vertices(self):
    for i in range(20):
      for j in range(10):
        v = self.grafo[i][j]
        v.d = math.inf
        v.pai = None
      
  def dijkstra(self, v):
    self.resetar_vertices()
    v.d = 0
    S = [] #Vértices já escolhidos
    Q = deque([v]) #Fila de vértices que terão suas arestas relaxadas
          
    while len(Q) != 0:
      u = Q.popleft()
      S.append(u)
      for s in u.adj:
        if s not in S:#Adiciona os vizinhos de u a lista caso nao tenham sido selecionados, e relaxa as arestas
          Q.append(s)
          self.relax(u, s)
          
  def spawn_tatu(self, x1, y1, x2, y2):#transforma cada tatu em um obstáculo
    self.grafo[x1][y1].setTipo(1)
    self.grafo[x2][y2].setTipo(1)
    
  def tatu_selecionado(self, x1, y1, x2, y2):
    v = self.grafo[x1][y1]
    u = self.grafo[x2][y2]
    self.grafo[x1][y1].setTipo(0)
    
    #Reabilita a aresta do tatu com exceção da parte de trás do tatu
    if x1 > 0:
      if self.grafo[x1-1][y1] != u:
        v.addArestas(self.grafo[x1-1][y1])#Aresta acima
      
    if x1 < 19:
      if self.grafo[x1+1][y1] != u:
        v.addArestas(self.grafo[x1+1][y1])#Aresta abaixo
      
    if y1 > 0:
      if self.grafo[x1][y1-1] != u:
        v.addArestas(self.grafo[x1][y1-1])#Aresta da esquerda
      
    if y1 < 9:
      if self.grafo[x1][y1+1] != u:
        v.addArestas(self.grafo[x1][y1+1])#Aresta da direita
        
  def tatu_deselecionado(self, x1, y1):
    self.grafo[x1][y1].setTipo(1)
    
  def tatu_liberado(self, x1, y1, x2, y2):
    v = self.grafo[x1][y1]
    u = self.grafo[x2][y2]
    
    v.setTipo(0)
    u.setTipo(0)
    
    if x1 > 0:
      if self.grafo[x1-1][y1] != u:
        v.addArestas(self.grafo[x1-1][y1])#Aresta acima
      
    if x1 < 19:
      if self.grafo[x1+1][y1] != u and self.grafo[x1+1][y1].tipo != 1:
        v.addArestas(self.grafo[x1+1][y1])#Aresta abaixo
      
    if y1 > 0:
      if self.grafo[x1][y1-1] != u and self.grafo[x1][y1-1].tipo != 1:
        v.addArestas(self.grafo[x1][y1-1])#Aresta da esquerda
      
    if y1 < 9:
      if self.grafo[x1][y1+1] != u and self.grafo[x1][y1+1].tipo != 1:
        v.addArestas(self.grafo[x1][y1+1])#Aresta da direita
        
    if x2 > 0:
      if self.grafo[x2-1][y2] != u and self.grafo[x2-1][y2].tipo != 1:
        v.addArestas(self.grafo[x2-1][y2])#Aresta acima
      
    if x2 < 19:
      if self.grafo[x2+1][y2] != u and self.grafo[x2+1][y2].tipo != 1:
        v.addArestas(self.grafo[x2+1][y2])#Aresta abaixo
      
    if y2 > 0:
      if self.grafo[x2][y2-1] != u and self.grafo[x2][y2-1].tipo != 1:
        v.addArestas(self.grafo[x2][y2-1])#Aresta da esquerda
      
    if y2 < 9:
      if self.grafo[x2][y2+1] != u:
        v.addArestas(self.grafo[x2][y2+1])#Aresta da direita

g = Grafo()

g.criar_arestas()

#g.dijkstra(g.grafo[18][5])

#g.imprimir_grafo()
