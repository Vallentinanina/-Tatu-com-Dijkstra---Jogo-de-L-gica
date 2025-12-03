from constantes import *
NIVEIS = {
    1: {
        'tatus': 16,
        'spawn_tatu':[(50,620),(100,640),(160,620), (220,640),(280, 620),(360, 620),(40, 660),(150, 660),(280,660),(340, 680),(200, 700),(60,720),(120, 700),(260, 720),(330, 740),(150,740)],
        
        #Cabeça - x1
        'coord_tatu_f1':[15,15,15,15,15,15,16,16,16,16,17,17,17,17,18,18],
        #y1
        'coord_tatu_f2':[1,2,3,5,6,9,0,3,7,8,3,1,5,6,3,8], 
        #Atrás - x2
        'coord_tatu_t1':[15,16,15,16,15,15,16,16,16,17,17,18,17,18,18,18],
        #y2
        'coord_tatu_t2':[0,2,4,5,7,8,1,4,6,8,2,1,4,6,4,7],
        
        'direcao': [DIREITA,CIMA,ESQUERDA,CIMA,ESQUERDA,DIREITA,ESQUERDA,ESQUERDA,DIREITA,CIMA,DIREITA,CIMA,DIREITA,CIMA,DIREITA,ESQUERDA],
    },
    2: {
        'tatus': 18,
        'spawn_tatu':[(60, 640), (120, 620), (180, 640), (250, 620),(320, 620), (40, 700), (100, 680), (160, 700),(220, 680),(280, 660), (270, 700),(340, 680), (80, 740), (140, 760), (200, 740), (260, 760), (300, 760), (350, 740)],
        'direcao':[CIMA, ESQUERDA, CIMA, DIREITA, DIREITA, DIREITA, CIMA, ESQUERDA, CIMA, DIREITA,ESQUERDA, CIMA, DIREITA, CIMA, DIREITA, CIMA, BAIXO, ESQUERDA],
         #Cabeça - x1
        'coord_tatu_f1':[15,15,15,15,15,17,16,17,16,16,17,16,18,18,18,18,19,18],
        #y1
        'coord_tatu_f2':[1,2,4,6,8,1,2,3,5,7,6,8,2,3,5,6,7,8],
        #Atrás - x2
        'coord_tatu_t1':[16,15,16,15,15,17,17,17,17,16,17,16,18,19,18,19,18,18],
        #y2
        'coord_tatu_t2':[1,3,4,5,7,0,2,4,5,6,7,8,1,3,4,6,7,9],
        },
    3: {
        'tatus': 18,
        'spawn_tatu':[(80, 620), (170, 620), (220, 640), (280, 620),(280,660),(340,640), (40, 660), (100, 680), (150, 660), (200, 700),(280,700),(360,700),(20, 720), (80, 740), (140, 760), (200, 740), (280,740),(340,760)],
     'direcao':[ESQUERDA, DIREITA, CIMA, DIREITA, ESQUERDA,CIMA, DIREITA, CIMA, ESQUERDA, DIREITA, ESQUERDA,DIREITA, CIMA, DIREITA, CIMA, ESQUERDA, ESQUERDA,BAIXO],
      #Cabeça - x1
        'coord_tatu_f1':[15,15,15,15,16,15,16,16,16,17,17,17,17,18,18,18,18,19],
        #y1
        'coord_tatu_f2':[1,4,5,7,6,8,1,2,3,5,6,9,0,2,3,4,6,8],
        #Atrás - x2
        'coord_tatu_t1':[15,15,16,15,16,16,16,17,16,17,17,17,18,18,19,18,18,18],
        #y2
        'coord_tatu_t2':[2,3,5,6,7,8,0,2,4,4,7,8,0,1,3,5,7,8],
    }
}