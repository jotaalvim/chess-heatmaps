import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1 import AxesGrid
import re
#import sys

#lances de cavalo
#grep -Po '\bNx?\K[a-h][1-8]' /home/jotaalvim/Documents/bases_dados/outras/lichess_jotaalvim_2021-03-23.pgn | sort | uniq -c  | sort -n

#jogos = sys.argv[1]
#jogos = "/home/jotaalvim/Documents/bases_dados/outras/lichess_jotaalvim_2022-03-12.pgn"
#jogos = "/home/jotaalvim/Downloads/lichess_DiogoCipreste_2022-03-12.pgn"
#jogos = "/home/jotaalvim/Downloads/lichess_Lucena0202_2022-03-11.pgn"
#jogos = "/home/jotaalvim/Downloads/lichess_Portomas_2022-03-11.pgn"
jogos = "/home/jotaalvim/Downloads/lichess_LordVeldergrath_2022-03-13.pgn" 
f = open(jogos, "r") 

texto = f.read() 

#username of the person in study, might be automated later?
#username = "jotaalvim"
#username = "Portomas"
username = "LordVeldergrath"

#Logarithm scale option
log = False
#log = True

#color of analysis  'black', 'white', 'both'
#color = 'white'
color = 'black'


def getGames(color):
    if (color == 'white'):
        games = re.findall(fr'White "{username}"(?:.|\n)*?\n(1\..*)',texto)
    if (color == 'black'):
        games = re.findall(fr'Black "{username}"(?:.|\n)*?\n(1\..*)',texto)
    return games

games = getGames(color)

dic = { 'N' : {}, 'B' : {}, 'Q' : {}, 'K' : {}, 'R' : {}, 'P' : {} } 

for jogo in games:
    i = 1
    fim = 200

    gameSlice = re.findall(fr'\b{i}\. (.*?)(?:{fim+1}|1000)',jogo+'1000')[0]

    if (color == 'black'):
        pretas = r'\S+ '
    else:
        pretas = ''

    for peca,pos in re.findall(fr'\b[0-9]+\. {pretas}([NQBRK])x?([a-z][1-8])', gameSlice):
        if pos in dic[peca]:
            dic[peca][pos] += 1
        else:
            dic[peca][pos]  = 1

    for pos in re.findall(fr'[0-9]+\. {pretas}(?:[a-h]x)?([a-z][1-8])',gameSlice):
        if pos in dic['P']:
            dic['P'][pos] += 1
        else:
            dic['P'][pos]  = 1


# quando não ha valores poe-nos a 0
for c in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']:
    for key in 'NQBPKR':
        if c not in dic[key]:
            dic[key][c] = 0


# cria uma lista com os valores
l = { 'N' : [], 'B' : [], 'Q' : [], 'R' : [], 'P' : [], 'K' : [] }

for key in 'NBQRPK':
    for val in sorted(dic[key]):
        l[key].append(dic[key][val])

#for val in sorted(dKing):
#    lK.append(dKing[val])


# parte uma lista numa matriz de listas de tamanho 8
n = 8

dPlot = { 'N':None, 'Q':None, 'P':None, 'K':None, 'R':None, 'B':None}
#    "plot Night"
for key in 'NQPKRB':
    dPlot[key] = [l[key][i:i + n] for i in range(0, len(l[key]), n)] 

#pK = [lK[i:i + n] for i in range(0, len(lK), n)] 

# trapalhada para por o tabuleiro com orientação das brancas

for key in 'NQPKRB':
    for row in dPlot[key]:
        row.reverse()
#for row in pK:
#    row.reverse()

for key in 'NQPKRB':
    numpy_array = np.array(dPlot[key])
    transpose = numpy_array.T
    dPlot[key] = transpose.tolist()

#numpy_array = np.array(pK)
#transpose = numpy_array.T
#pK = transpose.tolist()

#plt.title( "Knight heat map" )

fig, axes = plt.subplots(ncols=6, figsize=(80, 15))
#fig.set_figheight(80)
#fig.set_figwidth(15)

ax1, ax2, ax3, ax4, ax5, ax6 = axes

if (log):
    im1 = ax1.matshow(dPlot['P'], cmap = 'binary', norm=LogNorm())
    im2 = ax2.matshow(dPlot['N'], cmap = 'binary', norm=LogNorm())
    im3 = ax3.matshow(dPlot['B'], cmap = 'binary', norm=LogNorm())
    im4 = ax4.matshow(dPlot['R'], cmap = 'binary', norm=LogNorm())
    im5 = ax5.matshow(dPlot['Q'], cmap = 'binary', norm=LogNorm())
    im6 = ax6.matshow(dPlot['K'], cmap = 'binary', norm=LogNorm())
else:
    im1 = ax1.matshow(dPlot['P'])
    im2 = ax2.matshow(dPlot['N'])
    im3 = ax3.matshow(dPlot['B'])
    im4 = ax4.matshow(dPlot['R'])
    im5 = ax5.matshow(dPlot['Q'])
    im6 = ax6.matshow(dPlot['K'])

#plt.title( "Knight heat map" )
plt.savefig('assets/teste.svg', dpi= 100)
plt.savefig('assets/teste.png', dpi= 100)
plt.show()
