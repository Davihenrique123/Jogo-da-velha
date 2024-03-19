import random

jogadas_possiveis = ['0:0', '0:1', '0:2',
                     '1:0', '1:1', '1:2',
                     '2:0', '2:1', '2:2']
player_1 = '1'
player_2 = '2'
vitoria1 = ['X', 'X', 'X']
vitoria2 = ['O', 'O', 'O']
caracter = '*'
player1 = 'X'
player2 = 'O'
tabuleiro = [[caracter, caracter, caracter],
             [caracter, caracter, caracter],
             [caracter, caracter ,caracter]]

def zerar_tudo():
    global tabuleiro
    global jogadas_possiveis

    tabuleiro = [[caracter, caracter, caracter],
                 [caracter, caracter, caracter],
                 [caracter, caracter ,caracter]]
    
    jogadas_possiveis = ['0:0', '0:1', '0:2',
                         '1:0', '1:1', '1:2',
                         '2:0', '2:1', '2:2']

def jogadaPL(player, coordenada):
    (linha, coluna) = coordenada.split(':')
    if coordenada in jogadas_possiveis:
        tabuleiro[int(linha)][int(coluna)] = player
        jogadas_possiveis.remove(coordenada)
        for linha in tabuleiro:
            print(linha)
        print("")
        return True
    else:
        return False
        
def jogadaCPU(player):
    coordenada = random.choice(jogadas_possiveis)
    (linha , coluna) = coordenada.split(':')
    if tabuleiro[int(linha)][int(coluna)] == caracter:
        tabuleiro[int(linha)][int(coluna)] = player
        jogadas_possiveis.remove(coordenada)
        for linha in tabuleiro:
            print(linha)
        print("")
        return coordenada
            
def verificação():
    for i in range(3):
        valores_linha = tabuleiro[i] 
        if (valores_linha == vitoria1):
            return player_1
        elif (valores_linha == vitoria2):
            return player_2

    for i in range(3):
        valores_coluna = [linha[i] for linha in tabuleiro] 
        if (valores_coluna == vitoria1): 
            return player_1
        elif (valores_coluna == vitoria2):
            return player_2
        
    if (tabuleiro[int(0)][int(0)] == 'X' and tabuleiro[int(1)][int(1)] == 'X' and tabuleiro[int(2)][int(2)] == 'X') or (tabuleiro[int(0)][int(2)] == 'X' and tabuleiro[int(1)][int(1)] == 'X' and tabuleiro[int(2)][int(0)] == 'X'): 
        return player_1
    
    if (tabuleiro[int(0)][int(0)] == 'O' and tabuleiro[int(1)][int(1)] == 'O' and tabuleiro[int(2)][int(2)] == 'O') or (tabuleiro[int(0)][int(2)] == 'O' and tabuleiro[int(1)][int(1)] == 'O' and tabuleiro[int(2)][int(0)] == 'O'):
        return player_2