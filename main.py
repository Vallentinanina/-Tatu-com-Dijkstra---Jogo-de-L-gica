import pygame
import constantes
import sprites
import os
from DijsktraJogo import Grafo
from niveis import *



class Jogo:
    def __init__(self):
        pygame.init()
        self.nivel_atual = 1
        self.tela = pygame.display.set_mode((constantes.LARGURA, constantes.ALTURA))
        pygame.display.set_caption("Hora do Tatu")
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.font = pygame.font.match_font('Times New Roman')
        self.tatu_selecionado = None
        self.carregar_arquivos()
        self.pontos = 0
        self.fonte_pixel = pygame.font.Font(os.path.join('sprites', 'NFPixels-Regular.ttf'), 20)
        self.spacebar = True
        
    
    def novo_jogo(self):
        #MR - Cria a mariz 20x10 e conecta os vértices vizinhos. O grafo vira o mapa lógico do nível
        # é nele que o Dijkstra calcula o caminho do tatu
        self.grafo = Grafo()
        self.grafo.criar_arestas()
        self.tatu_selecionado = None
        self.spacebar = True
        config = NIVEIS[self.nivel_atual]
        posicoes_tatus = config['spawn_tatu']
        direcoes = config['direcao']
        qt_tatus = config['tatus']
        
        coord_x1 = config['coord_tatu_f1']
        coord_y1 = config['coord_tatu_f2']
        coord_x2 = config['coord_tatu_t1']
        coord_y2 = config['coord_tatu_t2']
        
        self.todas_sprites = pygame.sprite.Group()
        self.tatus = []
        self.grupo_pedras = pygame.sprite.Group()
        self.grupo_arbusto = pygame.sprite.Group()

        for i in range(qt_tatus):
            pos = posicoes_tatus[i]
            direcao = direcoes[i]
            
            
            x1 = coord_x1[i]
            y1 = coord_y1[i]
            x2 = coord_x2[i]
            y2 = coord_y2[i]
            
            self.grafo.spawn_tatu(x1, y1, x2, y2)
            
            tatu = sprites.Tatu(self.surf_sprites_parado, self.surf_sprites_andando)
            tatu.rect.center = pos
            tatu.direcao = direcao
            
            tatu.x1 = x1
            tatu.y1 = y1
            tatu.x2 = x2
            tatu.y2 = y2
            
            tatu.linha = x1
            tatu.coluna = y1

         # Atualiza sprite inicial de acordo com a direção
            tatu.image = tatu.sprites_parado[direcao][0]
            tatu.chegou_final = False
            self.todas_sprites.add(tatu)
            self.tatus.append(tatu)

     
        for i in range(constantes.LINHAS):
            for j in range(constantes.COLUNAS):
             v =self.grafo.grafo[i][j]
             x = j * constantes.TAMANHO_CELULA
             y = i * constantes.TAMANHO_CELULA
             if v.tipo == 1:
                 if i in [13, 9, 5, 1]: #onde as pedras vao nascer
                     pedra = sprites.Pedra((x,y))
                     self.grupo_pedras.add(pedra)
                 elif i in [11,7,3]: #onde os arbustos vão nascer
                     arbusto = sprites.Arbusto((x,y))
                     self.grupo_arbusto.add(arbusto)
             elif v.tipo == 0:
                 pass   
             elif v.tipo == 2:
                 pass         


        
        self.rodar()
        
     
    def rodar(self):   
        #loop while
        self.jogando = True
        while self.jogando:
            self.relogio.tick(constantes.FPS) #taxa de frames
            self.eventos()
            self.atualizar()#atualiza as sprites
            self.desenhar()#desenhar as sprites
            
    def eventos(self):
        # Consumir todos os eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for tatu in self.tatus:
                    if tatu.rect.collidepoint(mouse):
                        self.tatu_selecionado = tatu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.spacebar:
                        self.grafo.imprimir_grafo()
                        if self.tatu_selecionado is None or self.tatu_selecionado.chegou_final == True:
                            print("Selecione um tatu!")
                            self.som_preso.play()
                            break
                        self.spacebar = False
                        # calcula caminho até a linha de chegada (linha 0), mesma coluna do tatu selecionado
                        caminho = self.calcular_caminho(self.tatu_selecionado.x1, self.tatu_selecionado.y1, self.tatu_selecionado.x2, self.tatu_selecionado.y2,)
                        if caminho and len(caminho) > 1:
                            caminho_valido = True
                            for i in range(1, len(caminho)):
                                pos = caminho[i]

                            if caminho_valido:
                                self.tatu_selecionado.path = [self.pixel_center_from_grid(r, c) for (r, c) in caminho]
                                self.tatu_selecionado.estado = constantes.MOVIMENTO
                            else: 
                                print("Caminho bloqueado por tatu")
                                self.som_preso.play()
                                self.spacebar = True
                    else:
                        print("Aguarde o tatu chegar ao final!")
                        self.som_preso.play()   
            '''''
            elif event.type == pygame.KEYUP:
                print("Digite o nível a ser acessado:")
                nivel = input()
                self.nivel_atual = int(nivel)
                self.jogando = False
                self.mostrar_tela_parabens()
              '''''
             
        # leitura contínua de teclas para movimento (fora do loop de eventos)
        teclas = pygame.key.get_pressed()
        tatu = self.tatu_selecionado
        
    def verificar_movimento_seguro(self, tatu, caminho):
       for i in range(1, len(caminho)):
          pos = caminho[i]
        
        # Verifica se há outro tatu nesta posição
       for other_t in self.tatus:
            if other_t is not tatu and not other_t.chegou_final:
                # Posição atual de outro tatu
                if (other_t.linha, other_t.coluna) == pos:
                    return False
                
                # Próxima posição de outro tatu em movimento
                if hasattr(other_t, 'path') and other_t.path:
                    next_other_pos = self.grid_from_pixel(other_t.path[0][0], other_t.path[0][1])
                    if next_other_pos == pos:
                        return False
       return True
    def atualizar_tatus(self):
   
     for t in self.tatus:
        if not t.chegou_final:
            t.linha, t.coluna = self.grid_from_pixel(t.rect.centerx, t.rect.centery)
            t.atualizar_posicoes_ocupadas() 
    
     self.ocupado_por_tatu = set()
     for t in self.tatus:
        if not t.chegou_final:
            for pos in t.ocupando_posicoes:
                self.ocupado_por_tatu.add(pos)
            
            if hasattr(t, 'path') and t.path:
                next_pos = self.grid_from_pixel(t.path[0][0], t.path[0][1])
                self.ocupado_por_tatu.add(next_pos)
        
        
    def atualizar(self):
        self.todas_sprites.update()


        #aplica caminhos calculados em background
        for tatu in self.tatus:
            if hasattr(tatu, 'caminho_pendente') and tatu.caminho_pendente is not None:
                caminho = tatu.caminho_pendente 
                if caminho:
                    tatu.caminho = [self.pixel_center_from_grid(r,c) for (r,c)in caminho]
                    tatu.estado = constantes.MOVIMENTO
                tatu.caminho_pendente = None
                tatu.calculando = False
                
        
            r, c = self.grid_from_pixel(tatu.rect.centerx, tatu.rect.centery)
            if r == 0 and not tatu.chegou_final: #tatu chegou no final
                tatu.chegou_final = True
                self.pontos += 50
                self.som_ponto.play()
                self.grafo.definir_obstaculos()#redefine os obstáculos
                self.spacebar = True
                self.grafo.tatu_liberado(tatu.x1, tatu.y1, tatu.x2, tatu.y2)
               
                self.tatu_selecionado = None
                
                #redefine os sprites
                for i in range(constantes.LINHAS):
                    for j in range(constantes.COLUNAS):
                        v =self.grafo.grafo[i][j]
                        x = j * constantes.TAMANHO_CELULA
                        y = i * constantes.TAMANHO_CELULA
                        if v.tipo == 1:
                            if i in [13, 9, 5, 1]: #sprites de pedras
                                pedra = sprites.Pedra((x,y))
                                if pedra not in self.grupo_pedras:
                                    self.grupo_pedras.add(pedra)
                            elif i in [11,7,3]: #sprites de arbustos
                                arbusto = sprites.Arbusto((x,y))
                                if arbusto not in self.grupo_arbusto:
                                    self.grupo_arbusto.add(arbusto)
                        elif v.tipo == 0:
                            if i in [13, 9, 5, 1]:  #limpa os sprites de pedra
                                for pedra in list(self.grupo_pedras):
                                    if pedra.rect.topleft == (x, y):
                                        self.grupo_pedras.remove(pedra)
                            elif i in [11, 7, 3]:  #limpa os sprites de arbusto
                                for arbusto in list(self.grupo_arbusto):
                                    if arbusto.rect.topleft == (x, y):
                                        self.grupo_arbusto.remove(arbusto)
                        elif v.tipo == 2:
                            pass         

                 
            #quando todos chegarem pula o nivel
            if len(self.tatus) > 0 and all(t.chegou_final for t in self.tatus): 
                 self.jogando = False
                 
              #se era o ultimo nivel acaba     
                 if self.nivel_atual == len(NIVEIS):     
                     self.mostrar_tela_fim_jogo()
                     self.rodando = False
                     return
            
                 self.mostrar_tela_parabens()
                 self.nivel_atual +=1
                 self.spacebar = True
                 return        
                 
        
    def desenhar(self):
        self.tela.blit(self.fundo, (0,0))
        
        #Fazer a grade
        for x in range(constantes.COLUNAS + 1):
            pygame.draw.line(
                self.tela, (200,200,200), #cinza claro
                (x * constantes.TAMANHO_CELULA, 0), (x * constantes.TAMANHO_CELULA, constantes.ALTURA)
            )
        for y in range(constantes.LINHAS + 1):
            pygame.draw.line(
                self.tela,
                (200,200,200),
                (0,y* constantes.TAMANHO_CELULA), (constantes.LARGURA, y * constantes. TAMANHO_CELULA)
            )
        self.todas_sprites.draw(self.tela)
        self.grupo_arbusto.draw(self.tela)
        self.grupo_pedras.draw(self.tela)
        pontos_texto = self.fonte_pixel.render(f"Pontos: {self.pontos}", True, (255, 255, 0))
        self.tela.blit(pontos_texto, (10, 10))
        pygame.display.flip()
        
    def carregar_arquivos(self):
        diretorio_imgs = os.path.join(os.getcwd(), 'sprites')

        # surfaces importantes (já escaladas quando necessário)
        self.surf_sprites_parado = pygame.image.load(os.path.join(diretorio_imgs,'sprites_parado.png')).convert_alpha()
        self.surf_sprites_andando = pygame.image.load(os.path.join(diretorio_imgs,'sprites_movimento.png')).convert_alpha()

        self.fundo = pygame.image.load(os.path.join(diretorio_imgs, 'fundo.png')).convert()
        self.fundo = pygame.transform.scale(self.fundo, (constantes.LARGURA, constantes.ALTURA))
        
        self.fundo_inicio = pygame.image.load(os.path.join(diretorio_imgs, 'fundo_inicio.png')).convert()
        self.fundo_inicio = pygame.transform.scale(self.fundo_inicio, (constantes.LARGURA, constantes.ALTURA))

        self.img_pedra1 = pygame.image.load(os.path.join(diretorio_imgs, 'pedra1.png')).convert_alpha()
        self.img_pedra1 = pygame.transform.scale(self.img_pedra1, (constantes.TAMANHO_CELULA, constantes.TAMANHO_CELULA))

        self.img_pedra2 = pygame.image.load(os.path.join(diretorio_imgs, 'pedra2.png')).convert_alpha()
        self.img_pedra2 = pygame.transform.scale(self.img_pedra2, (constantes.TAMANHO_CELULA, constantes.TAMANHO_CELULA))

        self.img_arbusto = pygame.image.load(os.path.join(diretorio_imgs, 'arbusto1.png')).convert_alpha()
        self.img_arbusto = pygame.transform.scale(self.img_arbusto, (constantes.TAMANHO_CELULA, constantes.TAMANHO_CELULA))
        
        self.nuvem = pygame.image.load(os.path.join(diretorio_imgs, 'nuvens.png')).convert()
        self.nuvem = pygame.transform.scale(self.nuvem, (constantes.LARGURA, constantes.ALTURA))

        self.som_ponto = pygame.mixer.Sound(os.path.join(diretorio_imgs, 'levelUp.wav'))
        self.som_preso = pygame.mixer.Sound(os.path.join(diretorio_imgs, 'somPreso.wav'))
        self.som_nivel = pygame.mixer.Sound(os.path.join(diretorio_imgs, 'telaParabensEFinal.wav'))
        self.som_final = pygame.mixer.Sound(os.path.join(diretorio_imgs, 'telaParabensEFinal.wav'))

    def mostrar_texto(self,texto, tamanho, cor, x, y):
        #exibe um texto na tela do jogo
        fonte = pygame.font.Font(self.font, tamanho)
        texto = fonte.render(texto, True, cor)
        texto_rect = texto.get_rect()
        texto_rect.midtop = (x,y)
        self.tela.blit(texto, texto_rect)
        
    def mostrar_tela_start(self):
        self.tela.blit(self.fundo_inicio, (0,0))
        nuvem1 = Nuvem()
        nuvem1.rect.center =(100,100)
        self.tela.blit(nuvem1.image, nuvem1.rect)
        nuvem2 = Nuvem()
        nuvem2.rect.center =(300,150)
        self.tela.blit(nuvem2.image, nuvem2.rect)
        self.mostrar_texto("Hora do Tatu", 60, (255, 255, 255), constantes.LARGURA / 2, constantes.ALTURA / 4)
        self.mostrar_texto("Pressione uma tecla para começar", 29, (0, 0, 139), constantes.LARGURA / 2, constantes.ALTURA / 2)
        self.mostrar_texto("Desenvolvido por: Luna, Maria Rita e Vallentina", 19, (255, 255, 255), constantes.LARGURA/2,5)
        pygame.display.flip()
        self.esperar_por_jogador()
        
    def mostrar_tela_parabens(self):
        self.som_nivel.play()
        esperando = True
        while esperando:
            self.relogio.tick(constantes.FPS)
            self.tela.blit(self.fundo_inicio, (0,0))
            self.mostrar_texto("PARABAINS!", 50 ,(255,255,0), constantes.LARGURA/2, constantes.ALTURA/4)
            self.mostrar_texto(f"Pontuação atual:{self.pontos}", 35, (255, 255, 255), constantes.LARGURA/2, constantes.ALTURA/3)
            self.mostrar_texto('Pressione qualquer tecla para o próximo nível', 19, (255,255,255),  constantes.LARGURA / 2, constantes.ALTURA / 2)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if event.type == pygame.KEYUP:
                    esperando = False
    
    def mostrar_tela_fim_jogo(self):
        self.som_final.play()
        esperando = True
        while esperando:
            self.relogio.tick(constantes.FPS)
            self.tela.fill((0,0,0))
            self.mostrar_texto("PARABAINS!", 50 ,(255,255,0), constantes.LARGURA/2, constantes.ALTURA/4)
            self.mostrar_texto("Pontuação Final:", 40, (255, 255, 255), constantes.LARGURA/2, constantes.ALTURA/1.6)
            self.mostrar_texto(str(self.pontos), 60, (255, 255,0), constantes.LARGURA/2, constantes.ALTURA/1.45)
            self.mostrar_texto("Fim de jogo", 50, (255,255,255), constantes.LARGURA/2, constantes.ALTURA/2)
            self.mostrar_texto("Pressione qualquer tecla para sair", 30, (200,200,200), constantes.LARGURA/2, constantes.ALTURA/1.3)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if event.type == pygame.KEYUP:
                    esperando = False
    
        
    def esperar_por_jogador(self):
        esperando = True
        while esperando:
            self.relogio.tick(constantes.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if event.type == pygame.KEYUP:
                    esperando = False
    
    #MR - Essa função converte coordenadas de pixel para coordenadas de grade do mapa do jogo
    def grid_from_pixel(self, x, y):
        #Divide x e y pelo tamanho da célula para descobrir em qual célula da grade e o ponto está
        col = x // constantes.TAMANHO_CELULA
        row = y // constantes.TAMANHO_CELULA
        #Usa max e min para garantir que o resultado não ultrapasse os limites da grade
        col = max(0, min(constantes.COLUNAS - 1, col))
        row = max(0, min(constantes.LINHAS - 1, row))
        #Retornar uma tupla representando a posição na matriz do grafo
        return (row, col)
    
    #MR - Essa função faz o inverso, recebe uma posição na grade e retorna as coordenadas de pixel do centro dessa célula
    def pixel_center_from_grid(self, row, col):
        #Multiplica a coluna e a linha pelo tamanho da célula e soma metade do tamanho da célula para obter o centro
        cx = col * constantes.TAMANHO_CELULA + constantes.TAMANHO_CELULA // 2
        cy = row * constantes.TAMANHO_CELULA + constantes.TAMANHO_CELULA // 2
        #Retorna, que são as coordenadas centrais em pixels
        return (cx, cy)
    
    def calcular_caminho(self, x1, y1, x2, y2):
        #Pega o vértice inical do grafo usando as coordenadas fornecidas
        start_v = self.grafo.grafo[x1][y1]
        #Reseta os vértices do grafo para limpar estados anteriores
        self.grafo.resetar_vertices()
        #Marca o tatu como selecionado no grafo
        self.grafo.tatu_selecionado(x1, y1, x2, y2)
        #Executa o algoritmo de Dijkstra a partir do vértice incial
        self.grafo.dijkstra(start_v)
        #Define o objetivo como o vértice na linha 0 (topo) e mesma coluna do tatu
        goal_v = self.grafo.grafo[0][y1]
        #Se não existe caminho, imprime mensagem de tatu preso
        if goal_v.pai is None:
            print("Tatu preso! (-25 pontos)")
            self.grafo.tatu_deselecionado(x1, y1)
            self.som_preso.play()
            self.pontos -= 25
            self.spacebar = True
            return None
        #Se existe reconstrói caminho do objetivo até o início
        #Percorrendo cada vértice, procura sua posição na matriz do grafo e adiciona o caminho
        #Inverte o caminho para que ele vá do incío ao objetivo
        #Retorna a lista de posições do caminho
        path = []
        v = goal_v
        # para obter índices, procura o vértice na matriz (20x10) — custo é pequeno
        while v is not None:
            found = False
            for i in range(constantes.LINHAS):
                for j in range(constantes.COLUNAS):
                    if self.grafo.grafo[i][j] is v:
                        path.append((i, j))
                        found = True
                        break
                if found:
                    break
            v = v.pai
        path.reverse()
        #self.grafo.imprimir_grafo
        return path

class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        diretorio_imgs = os.path.join(os.getcwd(), 'sprites')
        self.image = pygame.image.load(os.path.join(diretorio_imgs, 'nuvens.png')).convert()
        self.image = pygame.transform.scale(self.image,(150,150))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
           

g = Jogo()
g.mostrar_tela_start()

while g.rodando:
    g.novo_jogo()

