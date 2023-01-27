import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1 import AxesGrid
import re
from jjcli import * 
import math
#import sys 
#grep -Po '\bNx?\K[a-h][1-8]' /home/jotaalvim/Documents/bases_dados/outras/lichess_jotaalvim_2021-03-23.pgn | sort | uniq -c  | sort -n

#jogos = sys.argv[1]

#jogos = "/home/jotaalvim/Documents/bases_dados/outras/lichess_jotaalvim_2022-03-12.pgn"
#jogos2 = "/home/jotaalvim/Documents/bases_dados/outras/lichess_DiogoCipreste_2022-03-12.pgn"
##jogos = "/home/jotaalvim/Documents/bases_dados/outras/lichess_Lucena0202_2022-03-11.pgn"
##jogos = "/home/jotaalvim/Documents/bases_dados/outras/lichess_LordVeldergrath_2022-03-13.pgn" 
#jogos3 = "/home/jotaalvim/Documents/bases_dados/outras/lichess_Tigran-Harutyunyan_2022-03-15.pgn" 
#jogos4 = "/home/jotaalvim/Documents/bases_dados/outras/lichess_Portomas_2022-03-11.pgn"
#jogos5 = "/home/jotaalvim/Documents/bases_dados/outras/lichess_rp_o_02_2022-03-28.pgn"
#
#
##c = clfilter(opt="do:")     ## option values in c.opt dictionary
#for texto in c.text():



#username of the person in study 
#username = "DiogoCipreste"
#username2= "jotaalvim"
#username3 = "Tigran-Harutyunyan"
#username4 = "Portomas"
#username5 = "rp_o_02"


c = clfilter(opt="blu:f:t:p:")

# path option 
if '-p' in c.opt:
    jogos = c.opt['-p']

f = open(jogos, "r") 
texto = f.read() 

#Number of moves option, t stands for 'to' 
if '-t' in c.opt:
    end = int(c.opt['-t'])
else:
    end = 400

#Number of moves option, f stands for 'from' 
if '-f' in c.opt:
    i = int(c.opt['-f'])
else:
    i = 1

#Username option
if '-u' in c.opt:
    username = c.opt['-u']
#Logarithm scale option
if '-l' in c.opt:
    log = True
else:
    log = False
#Black color option
if '-b' in c.opt:
    color = 'black'
else:
    color = 'white'

def getGames(color,path, username):
    f = open(path, "r") 
    text = f.read() 
    if (color == 'white'):
        games = re.findall(fr'White "{username}"(?:.|\n)*?\n(1\..*)',text)
    if (color == 'black'):
        games = re.findall(fr'Black "{username}"(?:.|\n)*?\n(1\..*)',text)
    return games


def moveTable (color, path, username):
    games = getGames(color, path, username)
    dic = { 'N':{}, 'B':{}, 'Q':{}, 'K':{}, 'R':{}, 'P':{} } 

    for jogo in games:
        gameSlice = re.findall(fr'\b{i}\. (.*?)(?:{end+1}|1000)',jogo+'1000')
        gameSlice = ('' if gameSlice == [] else gameSlice[0])

        pretas = (r'\S+ ' if color == 'black' else '')

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


        # replace O-O with Rg1 and Tf1
        #white short castle
        if color == 'white':
            wsc= re.findall(r'\d+\. O-O',gameSlice)
            # n is at maximum 1
            n = len(wsc)
            if 'g1' in dic['K']:
                dic['K']['g1'] += n
            else:
                dic['K']['g1'] = n
            if 'f1' in dic['R']:
                dic['R']['f1'] += n
            else:
                dic['R']['f1'] = n
            #white long castle
            wlc= re.findall(r'\d+\. O-O-O',gameSlice)
            n = len(wlc)
            if 'c1' in dic['K']:
                dic['K']['c1'] += n
            else:
                dic['K']['c1'] = n
            if 'd1' in dic['R']:
                dic['R']['d1'] += n
            else:
                dic['R']['d1'] = n

        if color == 'black':
            #black short castle
            bsc= re.findall(r'\d+\. \w+ O-O',gameSlice)
            n = len(bsc)
            if 'g8' in dic['K']:
                dic['K']['g8'] += n
            else:
                dic['K']['g8'] = n

            if 'f8' in dic['R']:
                dic['R']['f8'] += n
            else:
                dic['R']['f8'] = n
            #black long castle
            blc= re.findall(r'\d+\. \w+ O-O-O',gameSlice)
            n = len(blc)
            if 'c8' in dic['K']:
                dic['K']['c8'] += n
            else:
                dic['K']['c8'] = n
            if 'd8' in dic['R']:
                dic['R']['d8'] += n
            else:
                dic['R']['d8'] = n

    # when there are no vallues put's them to 0
    fill0(dic)

    l = { 'N' : [], 'B' : [], 'Q' : [], 'R' : [], 'P' : [], 'K' : [] }

    for key in 'NBQRPK':
        for val in sorted(dic[key]):
            l[key].append(dic[key][val])



    # parte uma lista numa matriz de listas de tamanho 8
    n = 8

    dPlot = { 'N':None, 'Q':None, 'P':None, 'K':None, 'R':None, 'B':None}

    for key in 'NQPKRB':
        dPlot[key] = [l[key][i:i + n] for i in range(0, len(l[key]), n)] 

    # rotates the board to be in whites orientation
    for key in 'NQPKRB':
        for row in dPlot[key]:
            row.reverse()

    for key in 'NQPKRB':
        numpy_array = np.array(dPlot[key])
        transpose = numpy_array.T
        dPlot[key] = transpose.tolist()

    return dPlot


def fill0(dic):
    for pos in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']:
        for key in 'NQBPKR':
            if pos not in dic[key]:
                dic[key][pos] = 0


def countGames (color, path,username):
    return len(getGames(color,path, username))

def difTable (color, jogos, jogos2 ,username, username2):
    dPlot  = moveTable(color, jogos , username) 
    dPlot2 = moveTable(color, jogos2, username2) 
    
    ngames  = countGames(color, jogos, username)
    ngames2 = countGames(color, jogos2, username2)
    
    #delta = { 'N':[], 'Q':[[]], 'P':[[]], 'K':[[]], 'R':[[]], 'B':[[]]}
    delta = dPlot.copy()

    for key in 'NBRKPQ':
        for i in range(8):
            for j in range(8):
                # add 1 because log(-1) == -infininty
                delta[key][i][j] = math.log((dPlot2[key][i][j])/ngames2 +1) - math.log((dPlot[key][i][j])/ngames +1)

    return delta



def capturePieces (color,path, username):
    games = getGames(color, path, username)
    dic = { 'N' : {}, 'B' : {}, 'Q' : {}, 'R' : {}, 'P' : {}, 'K' : {} }
    if (color == 'black'):
        pretas = r'\S+ '
    else:
        pretas = ''

    for jogo in games:
        gameSlice = re.findall(fr'\b{i}\. (.*?)(?:{end+1}|1000)',jogo+'1000')
        if gameSlice == []:
            gameSlice = ''
        else:
            gameSlice  = gameSlice[0]

        for piece,pos in re.findall(fr'\b[0-9]+\. {pretas}([NQBRK])x([a-z][1-8])', gameSlice):
            if pos in dic[piece]:
                dic[piece][pos] += 1
            else:
                dic[piece][pos] =  1

        for pos in re.findall(fr'[0-9]+\. {pretas}[a-h]x([a-h][1-8])\+?',gameSlice):
            if pos in dic['P']:
                dic['P'][pos] += 1
            else:
                dic['P'][pos]  = 1


    fill0(dic)
    # cria uma lista com os valores
    l = { 'N' : [], 'B' : [], 'Q' : [], 'R' : [], 'P' : [], 'K' : [] }

    for key in 'NBQRPK':
        for val in sorted(dic[key]):
            l[key].append(dic[key][val])

    # parte uma lista numa matriz de listas de tamanho 8
    n = 8
    dPlot = { 'N':None, 'Q':None, 'P':None, 'K':None, 'R':None, 'B':None}
    for key in 'NQPKRB':
        dPlot[key] = [l[key][i:i + n] for i in range(0, len(l[key]), n)]
    for key in 'NQPKRB':
        for row in dPlot[key]:
            row.reverse()
    for key in 'NQPKRB':
        numpy_array = np.array(dPlot[key])
        transpose = numpy_array.T
        dPlot[key] = transpose.tolist()

    return dPlot


#dPlot = difTable (color, jogos2, jogos3, username2 , username3)

dPlot  = moveTable(color, jogos , username) 
#dPlot  = moveTable(color, jogos2 , username2) 
#dPlot  = moveTable(color, jogos3 , username3) 
#dPlot  = moveTable(color, jogos4 , username4) 
#dPlot  = moveTable(color, jogos5 , username5) 
#dPlot  = capturePieces(color, jogos3 , username3) 

fig, axes = plt.subplots(ncols=6, figsize=(80, 15))
ax1, ax2, ax3, ax4, ax5, ax6 = axes
if (log):
    #cmap = 'binary' cores a preto e branco
    im1 = ax1.matshow(dPlot['P'], norm=LogNorm())
    im2 = ax2.matshow(dPlot['N'], norm=LogNorm())
    im3 = ax3.matshow(dPlot['B'], norm=LogNorm())
    im4 = ax4.matshow(dPlot['R'], norm=LogNorm())
    im5 = ax5.matshow(dPlot['Q'], norm=LogNorm())
    im6 = ax6.matshow(dPlot['K'], norm=LogNorm())
else:
    im1 = ax1.matshow(dPlot['P'])
    im2 = ax2.matshow(dPlot['N'])
    im3 = ax3.matshow(dPlot['B'])
    im4 = ax4.matshow(dPlot['R'])
    im5 = ax5.matshow(dPlot['Q'])
    im6 = ax6.matshow(dPlot['K'])
#plt.title( "Knight heat map" )

plt.savefig('outputs/heatmap.png', dpi= 100)
plt.show()
