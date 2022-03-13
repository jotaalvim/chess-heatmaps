import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1 import AxesGrid

import re
#import sys

#jogos = sys.argv[1]
#jogos = "/home/jotaalvim/Documents/bases_dados/outras/lichess_jotaalvim_2022-03-12.pgn"
#jogos = "/home/jotaalvim/Downloads/lichess_DiogoCipreste_2022-03-12.pgn"

#jogos = "/home/jotaalvim/Downloads/lichess_Lucena0202_2022-03-11.pgn"
#jogos = "/home/jotaalvim/Downloads/lichess_Portomas_2022-03-11.pgn"
jogos = "/home/jotaalvim/Downloads/lichess_LordVeldergrath_2022-03-13.pgn"




f = open(jogos, "r")
texto = f.read()

games = re.findall(r'\n1.*',texto)

dKnight = {}
dBishop = {}
dQueen  = {}
dRook   = {}
dPawn   = {}

#lances de cavalo
#grep -Po '\bNx?\K[a-h][1-8]' /home/jotaalvim/Documents/bases_dados/outras/lichess_jotaalvim_2021-03-23.pgn | sort | uniq -c  | sort -n

for jogo in games:
    #for pos in re.findall(r'Nx?([a-z][1-8])',jogo):
    for pos in re.findall(r'[0-9]+\. Nx?([a-z][1-8])',jogo):
    #for pos in re.findall(r'\b[1-9]\. Nx?([a-z][1-8])',jogo):
        if pos in dKnight:
            dKnight[pos] += 1
        else:
            dKnight[pos] = 1


    for pos in re.findall(r'[0-9]+\. Bx?([a-z][1-8])',jogo):
    #for pos in re.findall(r'\b[1-9]\. Nx?([a-z][1-8])',jogo):
        if pos in dBishop:
            dBishop[pos] += 1
        else:
            dBishop[pos] = 1

    for pos in re.findall(r'[0-9]+\. Qx?([a-z][1-8])',jogo):
    #for pos in re.findall(r'\b[1-9]\. Nx?([a-z][1-8])',jogo):
        if pos in dQueen:
            dQueen[pos] += 1
        else:
            dQueen[pos] = 1

    for pos in re.findall(r'[0-9]+\. Rx?([a-z][1-8])',jogo):
    #for pos in re.findall(r'\b[1-9]\. Nx?([a-z][1-8])',jogo):
        if pos in dRook:
            dRook[pos] += 1
        else:
            dRook[pos] = 1


    for pos in re.findall(r'[0-9]+\. (?:[a-h]x)?([a-z][1-8])',jogo):
    #for pos in re.findall(r'\b[1-9]\. Nx?([a-z][1-8])',jogo):
        if pos in dPawn:
            dPawn[pos] += 1
        else:
            dPawn[pos] = 1


# quando não ha valores poe-nos a 0
for c in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']:
    if c not in dKnight:
        dKnight[c] = 0
    if c not in dBishop:
        dBishop[c] = 0
    if c not in dQueen:
        dQueen[c] = 0
    if c not in dRook:
        dRook[c] = 0
    if c not in dPawn:
        dPawn[c] = 0


# cria uma lista com os valores
lN = []
lB = []
lQ = []
lR = []
lP = []

for val in sorted(dKnight):
    lN.append(dKnight[val])
for val in sorted(dBishop):
    lB.append(dBishop[val])
for val in sorted(dQueen):
    lQ.append(dQueen[val])
for val in sorted(dRook):
    lR.append(dRook[val])
for val in sorted(dPawn):
    lP.append(dPawn[val])


# parte uma lista numa matriz de listas de tamanho 8
n = 8
#    "plot Night"
pN = [lN[i:i + n] for i in range(0, len(lN), n)] 
pB = [lB[i:i + n] for i in range(0, len(lB), n)] 
pQ = [lQ[i:i + n] for i in range(0, len(lQ), n)] 
pR = [lR[i:i + n] for i in range(0, len(lR), n)] 
pP = [lP[i:i + n] for i in range(0, len(lP), n)] 

# trapalhada para por o tabuleiro com orientação das brancas
for row in pN:
    row.reverse()
for row in pB:
    row.reverse()
for row in pQ:
    row.reverse()
for row in pR:
    row.reverse()
for row in pP:
    row.reverse()

numpy_array = np.array(pN)
transpose = numpy_array.T
pN = transpose.tolist()

numpy_array = np.array(pB)
transpose = numpy_array.T
pB = transpose.tolist()

numpy_array = np.array(pQ)
transpose = numpy_array.T
pQ = transpose.tolist()

numpy_array = np.array(pR)
transpose = numpy_array.T
pR = transpose.tolist()

numpy_array = np.array(pP)
transpose = numpy_array.T
pP = transpose.tolist()
#plt.imshow( pN , cmap = 'binary')
#plt.imshow( pN , cmap = 'binary' , interpolation = 'nearest',  norm=LogNorm())
##plt.imshow( pN ,  norm=LogNorm())
#plt.title( "Knight heat map" )
#plt.show()


fig, axes = plt.subplots(ncols=5, figsize=(1, 8))

ax1, ax2, ax3, ax4, ax5 = axes

im1 = ax1.matshow(pN, cmap = 'binary')
im2 = ax2.matshow(pB, cmap = 'binary')
im3 = ax3.matshow(pQ, cmap = 'binary')
im4 = ax4.matshow(pR, cmap = 'binary')
im5 = ax5.matshow(pP, cmap = 'binary')

#plt.title( "Knight heat map" )
plt.show()



