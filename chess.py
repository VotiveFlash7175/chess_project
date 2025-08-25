import pygame
from pygame import *

# classes
class chesspiece:
    name = 'king'
    color = 'white'
    col0 = 0
    row0 = 0
    def __init__(self, name,color,col0,row0):
        self.name = name
        self.color = color
        self.col0 = col0
        self.row0 = row0
    def spawn_figure(self, dictImages):
        figure=self.name
        cl=self.color
        x=self.col0
        y=self.row0
        if cl == 'black':
            figure='b'+figure
        screen.blit(dictImages[figure], (x*(step+s_b)+step, (step+s_b)*y+step))
    #def possible_moves(self,list):

#functions
def prov_kl_m(piece1,x,y):
    for piece in list:
        if piece.col0==x and piece.row0==y:
            if piece.color==piece1.color:
                return False, ""
            else:
                return True, "color"
    return True, ""

def prov_kl(x,y):
    for piece in list:
        if piece.col0==x and piece.row0==y:
            return piece,x,y
    return None,x,y
def spawnall(list,dictImages,vyd):
    q = 0
    for col in range(8):
        for row in range(8):
            if q % 2==0:
                color = WHITE
            else:
                color = BLACK
            x = col * s_b + (col + 1) * step
            y = row * s_b + (row + 1) * step
            draw.rect(screen, color, (x, y, s_b, s_b))
            q+=1
        q+=1
    first = True
    for ab in vyd:
        a = ab[0]
        b = ab[1]
        if first:
            color = RED
        elif a%2==b%2:
            color = L_BLUE
        else:
            color = D_BLUE
        draw.rect(screen, color, (a*(step +s_b)+step, b*(step +s_b)+step, s_b, s_b))
        first = False
    for piece in list:
        piece.spawn_figure(dictImages)

def vyd_kl(col1,row1,figure,userecursion):
    vyd = []
    vyd.append([col1,row1])
    if figure.name == 'knight':
        if col1-1>=0 and row1+2<=7 and prov_kl_m(figure,col1-1,row1+2)[0]:
            vyd.append([col1-1,row1+2])
        if col1+1<=7 and row1+2<=7 and prov_kl_m(figure,col1+1,row1+2)[0]:
            vyd.append([col1+1,row1+2])
        if col1-1>=0 and row1-2>=0 and prov_kl_m(figure,col1-1,row1-2)[0]:
            vyd.append([col1-1,row1-2])
        if col1+1<=7 and row1-2>=0 and prov_kl_m(figure,col1+1,row1-2)[0]:
            vyd.append([col1+1,row1-2])
        if row1-1>=0 and col1+2<=7 and prov_kl_m(figure,col1+2,row1-1)[0]:
            vyd.append([col1+2,row1-1])
        if row1+1<=7 and col1+2<=7 and prov_kl_m(figure,col1+2,row1+1)[0]:
            vyd.append([col1+2,row1+1])
        if row1-1>=0 and col1-2>=0 and prov_kl_m(figure,col1-2,row1-1)[0]:
            vyd.append([col1-2,row1-1])
        if row1+1<=7 and col1-2>=0 and prov_kl_m(figure,col1-2,row1+1)[0]:
            vyd.append([col1-2,row1+1])
    if figure.name == 'rook':
        a = col1
        b = row1
        col1+=1
        while col1<8:
            if prov_kl_m(figure,col1,row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            col1 += 1
        col1 = a
        col1 -= 1
        while col1 > -1:
            if prov_kl_m(figure, col1, row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            col1 -= 1
        col1 = a
        row1 += 1
        while row1<8:
            if prov_kl_m(figure,col1,row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            row1 += 1
        row1 = b
        row1 -= 1
        while row1 > -1:
            if prov_kl_m(figure, col1, row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            row1 -= 1
        row1 = b
    if figure.name == 'bishop':
        a = col1
        b = row1
        col1+=1
        row1+=1
        while col1<8 and row1<8:
            if prov_kl_m(figure,col1,row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            col1 += 1
            row1 += 1
        col1 = a
        row1 = b
        col1 -= 1
        row1-=1
        while col1 > -1 and row1>-1:
            if prov_kl_m(figure, col1, row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            col1 -= 1
            row1 -= 1
        col1 = a
        row1 =b
        row1 += 1
        col1-=1
        while row1<8 and col1>-1:
            if prov_kl_m(figure,col1,row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            row1 += 1
            col1-=1
        row1 = b
        col1 = a
        row1 -= 1
        col1+=1
        while row1 > -1 and col1 >-1:
            if prov_kl_m(figure, col1, row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            row1 -= 1
            col1+=1
        row1 = b
        col1 = a
    if figure.name == 'queen':
        a = col1
        b = row1
        col1+=1
        while col1<8:
            if prov_kl_m(figure,col1,row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            col1 += 1
        col1 = a
        col1 -= 1
        while col1 > -1:
            if prov_kl_m(figure, col1, row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            col1 -= 1
        col1 = a
        row1 += 1
        while row1<8:
            if prov_kl_m(figure,col1,row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            row1 += 1
        row1 = b
        row1 -= 1
        while row1 > -1:
            if prov_kl_m(figure, col1, row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            row1 -= 1
        row1 = b
        col1+=1
        row1+=1
        while col1<8 and row1<8:
            if prov_kl_m(figure,col1,row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            col1 += 1
            row1 += 1
        col1 = a
        row1 = b
        col1 -= 1
        row1-=1
        while col1 > -1 and row1>-1:
            if prov_kl_m(figure, col1, row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            col1 -= 1
            row1 -= 1
        col1 = a
        row1 =b
        row1 += 1
        col1-=1
        while row1<8 and col1>-1:
            if prov_kl_m(figure,col1,row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            row1 += 1
            col1-=1
        row1 = b
        col1 = a
        row1 -= 1
        col1+=1
        while row1 > -1 and col1 >-1:
            if prov_kl_m(figure, col1, row1)[0]:
                vyd.append([col1, row1])
                if prov_kl_m(figure,col1,row1)[1]=='color':
                    break
            else:
                break
            row1 -= 1
            col1+=1
        row1 = b
        col1 = a
    if figure.name == 'pawn':
        a = 0
        f = False
        if figure.color == 'white':
            if row1 == 1:
                f = True
            a = 1
        else:
            if row1 == 6:
                f = True
            a = -1
        if prov_kl_m(figure, col1, row1+a)[0] and prov_kl_m(figure, col1, row1+a)[1]=='' :
            vyd.append([col1, row1+a])
        if f and prov_kl_m(figure, col1 , row1 +2*a)[0] and prov_kl_m(figure, col1, row1 + 2*a)[1] == '':
            vyd.append([col1, row1 + 2*a])
        if prov_kl_m(figure, col1 + a, row1 + a)[0] and prov_kl_m(figure, col1+a, row1 + a)[1] == 'color':
            vyd.append([col1 + a, row1 + a])
        if prov_kl_m(figure, col1 - a, row1 + a)[0] and prov_kl_m(figure, col1-a, row1 + a)[1] == 'color':
            vyd.append([col1 - a, row1 + a])
    if figure.name == 'king':
        if figure.color == 'white':
            rook1 = wrook1m
            rook2 = wrook2m
            king = wkingm
        else:
            rook1 = brook1m
            rook2 = brook2m
            king = bkingm
        if prov_kl_m(figure, col1, row1+1)[0] and not prov_vyd_king(col1, row1+1,figure.color, userecursion):
            vyd.append([col1, row1+1])
        if prov_kl_m(figure, col1, row1-1)[0] and not prov_vyd_king(col1, row1-1,figure.color, userecursion):
            vyd.append([col1, row1-1])
        if prov_kl_m(figure, col1+1, row1+1)[0] and not prov_vyd_king(col1+1, row1+1,figure.color, userecursion):
            vyd.append([col1+1, row1+1])
        if prov_kl_m(figure, col1-1, row1+1)[0] and not prov_vyd_king(col1-1, row1+1,figure.color, userecursion):
            vyd.append([col1-1, row1+1])
        if prov_kl_m(figure, col1+1, row1 - 1)[0] and not prov_vyd_king(col1+1, row1-1,figure.color, userecursion):
            vyd.append([col1+1, row1 - 1])
        if prov_kl_m(figure, col1-1, row1 - 1)[0] and not prov_vyd_king(col1-1, row1-1,figure.color, userecursion):
            vyd.append([col1-1, row1 - 1])
        if prov_kl_m(figure, col1 - 1, row1)[0] and not prov_vyd_king(col1-1, row1,figure.color, userecursion):
            vyd.append([col1 - 1, row1])
            if not rook1 and not king and prov_kl_m(figure, col1 - 2, row1)[0] and not prov_vyd_king(col1-2, row1,figure.color, userecursion) and not prov_vyd_king(col1, row1,figure.color, userecursion):
                vyd.append([col1 - 2, row1])
        if prov_kl_m(figure, col1+1, row1)[0] and not prov_vyd_king(col1+1, row1,figure.color, userecursion):
            vyd.append([col1 + 1, row1])
            if not rook2 and not king and prov_kl_m(figure, col1 + 2, row1)[0] and not prov_vyd_king(col1+2, row1,figure.color, userecursion) and not prov_vyd_king(col1, row1,figure.color, userecursion):
                vyd.append([col1 + 2, row1])
    return vyd
def prov_vyd_king(x,y,color, userecursion):
    if not userecursion:
        return False

    a = prov_kl(x, y)[0]
    if a != None and a in list:
        list.remove(a)

    newking = chesspiece("king", color, x, y)
    list.append(newking)
    for piece in list:
        if piece.color!=color:
            vyd_loc = vyd_kl(piece.col0, piece.row0, piece, False)
            del vyd_loc[0]
            if [x, y] in vyd_loc:
                list.remove(newking)
                if a != None:
                    list.append(a)
                return True
    list.remove(newking)
    if a != None:
        list.append(a)
    return False

s_b = 80
step = 10
wids = lens = s_b * 8 + step * 9
BLACK = (0, 0, 0)
BROWN = (117, 90, 87)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
L_BLUE= (173,216,230)
D_BLUE = (0,0,63)

init()

screen = display.set_mode((wids,lens))
display.set_caption('Chess')
screen.fill(BROWN)
knight = image.load('knight_transparent.png').convert_alpha()
knight = transform.scale(knight, (80, 80))
bknight = image.load('bknight.png').convert_alpha()
bknight = transform.scale(bknight, (80, 80))
rook = image.load('rook1.png').convert_alpha()
rook = transform.scale(rook, (80, 80))
brook = image.load('brook.png').convert_alpha()
brook = transform.scale(brook, (80, 80))
bishop = image.load('bishop1.png').convert_alpha()
bishop = transform.scale(bishop, (80, 80))
bbishop = image.load('bbishop.png').convert_alpha()
bbishop = transform.scale(bbishop, (80, 80))
queen = image.load('queen1.png').convert_alpha()
queen = transform.scale(queen, (80, 80))
bqueen = image.load('bqueen.png').convert_alpha()
bqueen = transform.scale(bqueen, (80, 80))
king = image.load('king1.png').convert_alpha()
king = transform.scale(king, (80, 80))
bking = image.load('bking.png').convert_alpha()
bking = transform.scale(bking, (80, 80))
pawn = image.load('pawn1.png').convert_alpha()
pawn = transform.scale(pawn, (80, 80))
bpawn = image.load('bpawn.png').convert_alpha()
bpawn = transform.scale(bpawn, (80, 80))
dictImages = {}
figure = chesspiece("pawn","white",0,1)
dictImages['king'] = king
dictImages['bking'] = bking
dictImages['queen'] = queen
dictImages['bqueen'] = bqueen
dictImages['pawn'] = pawn
dictImages['bpawn'] = bpawn
dictImages['rook'] = rook
dictImages['brook'] = brook
dictImages['bishop'] = bishop
dictImages['bbishop'] = bbishop
dictImages['knight'] = knight
dictImages['bknight'] = bknight



list = []
list.append(chesspiece("pawn","white",0,1))
list.append(chesspiece("pawn","white",1,1))
list.append(chesspiece("pawn","white",2,1))
list.append(chesspiece("pawn","white",3,1))
list.append(chesspiece("pawn","white",4,1))
list.append(chesspiece("pawn","white",5,1))
list.append(chesspiece("pawn","white",6,1))
list.append(chesspiece("pawn","white",7,1))
list.append(chesspiece("rook","white",0,0))
list.append(chesspiece("rook","white",7,0))
list.append(chesspiece("knight","white",1,0))
list.append(chesspiece("knight","white",6,0))
list.append(chesspiece("bishop","white",2,0))
list.append(chesspiece("bishop","white",5,0))
list.append(chesspiece("king","white",3,0))
list.append(chesspiece("queen","white",4,0))

list.append(chesspiece("pawn","black",0,6))
list.append(chesspiece("pawn","black",1,6))
list.append(chesspiece("pawn","black",2,6))
list.append(chesspiece("pawn","black",3,6))
list.append(chesspiece("pawn","black",4,6))
list.append(chesspiece("pawn","black",5,6))
list.append(chesspiece("pawn","black",6,6))
list.append(chesspiece("pawn","black",7,6))
list.append(chesspiece("rook","black",0,7))
list.append(chesspiece("rook","black",7,7))
list.append(chesspiece("knight","black",1,7))
list.append(chesspiece("knight","black",6,7))
list.append(chesspiece("bishop","black",2,7))
list.append(chesspiece("bishop","black",5,7))
list.append(chesspiece("king","black",3,7))
list.append(chesspiece("queen","black",4,7))
wrook1m = False
wrook2m = False
wkingm = False
brook1m = False
brook2m = False
bkingm = False
g_vyd = []
spawnall(list,dictImages,g_vyd)

running = True

while running:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            running = False
        elif ev.type == MOUSEBUTTONDOWN:
             coll = 0
             rowl = 0
             last = g_vyd
             lastf = figure
             x_mouse, y_mouse = mouse.get_pos()
             col1 = x_mouse // (step+ s_b)
             row1 = y_mouse // (step + s_b)
             figure = prov_kl(col1,row1)[0]
             x = prov_kl(col1,row1)[1]
             y = prov_kl(col1, row1)[2]
             if figure != None:
                coll = figure.col0
                rowl = figure.row0
             else:
                coll = x
                rowl = y
             if [coll, rowl] in last and lastf!=None:
                lastf.col0=coll
                lastf.row0=rowl
             if figure!= None:
                 g_vyd = vyd_kl(col1,row1,figure, True)
                 spawnall(list,dictImages,g_vyd)
    if running:
        display.update()
