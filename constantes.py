import pygame
import os   

COLUNAS = 10
LINHAS = 20
TAMANHO_CELULA = 40
BLOCO_TAMANHO = TAMANHO_CELULA * 2

TATU_LARGURA = TAMANHO_CELULA * 2
TATU_ALTURA = TAMANHO_CELULA * 2

LARGURA = COLUNAS * TAMANHO_CELULA
ALTURA = LINHAS * TAMANHO_CELULA
FPS = 60

DIREITA = 0
ESQUERDA = 1
CIMA = 2
BAIXO = 3

SPRITE_LARGURA = 80
SPRITE_ALTURA = 80

PARADO = 0
MOVIMENTO = 1

diretorio_principal = os.path.dirname(__file__)
diretorio_sprites = os.path.join(diretorio_principal, 'sprites')