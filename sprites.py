#na primeira coluna o x=0 e y=0, na segunda coluna x=0, y=32, cada sprite valendo 32
import pygame
from constantes import *

class Tatu(pygame.sprite.Sprite):
    def __init__ (self, spritesheet_parado, spritesheet_andando):
        super(). __init__()
        # Variáveis de controle
        self.current_frame = 0
        self.current_row = 0 #fileira
        self.animation_speed = 200  # ms entre frames
        self.last_update = pygame.time.get_ticks()
        self.index_lista = 0
        
        self.sprites_andando = spritesheet_andando
        self.sprites_parado = spritesheet_parado
        # Posição do sprite na tela
        self.sprite_x = LARGURA // 2 - TATU_LARGURA // 2
        self.sprite_y = ALTURA // 2 - TATU_ALTURA // 2
    
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.carregar_sprites()
        
        self.estado = PARADO
        self.direcao = DIREITA
        self.image = self.sprites_parado[self.direcao][0]
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA // 2, ALTURA // 2)
        self.ocupando_posicao = []
        

        
    def carregar_sprites(self):
      sprite_sheet = pygame.image.load('tatu_sprites.png').convert_alpha()
      self.sprites_parado = [[], [], [], []]#direita esquerda cima baixo
      self.sprites_andando = [[], [], [], []]
      NOVO_LARGURA = TATU_LARGURA  
      NOVO_ALTURA = TATU_ALTURA 
      
      for row in range(4):
       # Recorta o sprite parado
       PARADO = sprite_sheet.subsurface((0, row * 40, 40, 40))
       # Redimensiona
       PARADO = pygame.transform.scale(PARADO, (NOVO_LARGURA, NOVO_ALTURA))
       # Adiciona à lista
       self.sprites_parado[row].append(PARADO)
       # Recorta e redimensiona os sprites andando
       for col in range(1, 5):
        andando = sprite_sheet.subsurface((col * 40, row * 40, 40, 40))
        andando = pygame.transform.scale(andando, (NOVO_LARGURA, NOVO_ALTURA))
        self.sprites_andando[row].append(andando)

    def atualizar_posicoes_ocupadas(self):
        self.ocupando_posicoes = []
        
        if self.direcao == DIREITA or self.direcao == ESQUERDA:
            # Tatu horizontal: ocupa 2 colunas na mesma linha
            col1 = self.coluna
            col2 = self.coluna + 1 if self.direcao == DIREITA else self.coluna - 1
            if 0 <= col2 < COLUNAS:
                self.ocupando_posicoes.append((self.linha, col1))
                self.ocupando_posicoes.append((self.linha, col2))
            else:
                self.ocupando_posicoes.append((self.linha, col1))
        else:
            # Tatu vertical: ocupa 2 linhas na mesma coluna
            linha1 = self.linha
            linha2 = self.linha + 1 if self.direcao == BAIXO else self.linha - 1
            if 0 <= linha2 < LINHAS:
                self.ocupando_posicoes.append((linha1, self.coluna))
                self.ocupando_posicoes.append((linha2, self.coluna))
            else:
                self.ocupando_posicoes.append((linha1, self.coluna))
        
        
    def update(self):
        # movimentação automática por caminho (lista de centros em pixels)
         if hasattr(self, 'path') and self.path:
            target_x, target_y = self.path[0]
            
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            speed = 4
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.direcao = DIREITA
                else:
                    self.direcao = ESQUERDA
            else:
                if dy < 0:
                    self.direcao = CIMA
                else:
                    self.direcao = BAIXO
            move_x = max(-speed, min(speed, dx))
            move_y = max(-speed, min(speed, dy))
            self.rect.centerx += int(move_x)
            self.rect.centery += int(move_y)
            # se alcançou o destino do passo
            if abs(dx) <= speed and abs(dy) <= speed:
                self.rect.center = (target_x, target_y)
                self.path.pop(0)
                
                self.linha = self.rect.centery // TAMANHO_CELULA
                self.coluna = self.rect.centerx // TAMANHO_CELULA
                self.linha = max(0, min(LINHAS - 1, self.linha))
                self.coluna = max(0, min(COLUNAS - 1, self.coluna))
                
                self.atualizar_posicoes_ocupadas()
                
                if not self.path:
                    self.estado = PARADO  # Para o tatu ao chegar
                    return
            # animação andando
            sprites_animacao = self.sprites_andando[self.direcao]
            self.index_lista = (self.index_lista + 0.25) % max(1, len(sprites_animacao))
            if sprites_animacao:
                self.image = sprites_animacao[int(self.index_lista)]
         else:
             self.image = self.sprites_parado[self.direcao][0]
        
    def mover(self, direção):
        self.estado = MOVIMENTO
        self.direcao = direção
        if direção == DIREITA:
            self.rect.x += 5
        elif direção == ESQUERDA:
            self.rect.x -= 5
        elif direção == CIMA:
            self.rect.y -= 5
        elif direção== BAIXO:
            self.rect.y += 5
    
    def parar(self):
        self.estado = PARADO
        
class Pedra(pygame.sprite.Sprite):
    def __init__(self, pos):
     super().__init__()
     self.image = pygame.image.load(os.path.join(diretorio_sprites, 'pedra1.png')).convert_alpha()
     self.image = pygame.transform.scale(self.image, (TAMANHO_CELULA, TAMANHO_CELULA))
     self.rect = self.image.get_rect()
     self.rect.topleft = pos
    
        
class Arbusto(pygame.sprite.Sprite):
    def __init__(self, pos):
     super().__init__()
     super().__init__()
     self.image = pygame.image.load(os.path.join(diretorio_sprites, 'arbusto1.png')).convert_alpha()
     self.image = pygame.transform.scale(self.image, (TAMANHO_CELULA, TAMANHO_CELULA))
     self.rect = self.image.get_rect()
     self.rect.topleft = pos
