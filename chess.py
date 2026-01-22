import pygame
from pygame import *
from random import *
from copy import *
from stockfish import Stockfish
dir = r".\stockfish\stockfish-windows-x86-64-avx2.exe"
stockfish = Stockfish(path = dir)
stockfish.set_position([])
best_move_ever = ''
# classes
class chesspiece:
    name = 'king'
    color = 'white'
    col0 = 0
    row0 = 0
    row1 = -1
    def __init__(self, name,color,col0,row0):
        self.name = name
        self.color = color
        self.col0 = col0
        self.row0 = row0
    def spawn_figure(self, dict):
        figure=self.name
        cl=self.color
        x=self.col0
        y=self.row0
        if cl == 'black':
            figure='b'+figure
        screen.blit(dict[figure], (x*(step+s_b)+step, (step+s_b)*y+step))
    #def possible_moves(self,list):

class child_position:
    positionlist = []
    move = ''
    def __init__(self, positionlist, move):
        self.positionlist = positionlist
        self.move = move

#functions
def new_pos(listr,col_move):
    global list
    newpos = []
    list = listr
    for piece in listr:
        if piece.color==col_move:
            vyd = vyd_kl(piece.col0, piece.row0, piece, True)
            del vyd[0]
            for move in vyd:
                copy4 = list.copy()
                for f in copy4:
                    if f.col0 == move[0] and f.row0 == move[1]:
                        del copy4[copy4.index(f)]
                        break
                p_index=copy4.index(piece)
                newpiece = copy(copy4[p_index])
                copy4[p_index] = newpiece
                fig_move = chr(97 + 7 - newpiece.col0) + str(newpiece.row0 + 1) + chr(97 + 7 - move[0]) + str(move[1] + 1)
                copy4[p_index].col0,copy4[p_index].row0=move[0],move[1]
                copy1 = child_position(copy4,fig_move)
                newpos.append(copy1)
    return newpos
def prov_kl_m(piece1,x,y):
    for piece in list:
        if x>7 or y>7 or x<0 or y<0:
            return False, ""
        if piece.col0==x and (piece.row0==y or (piece1.name=='pawn' and piece.row1==y)):
            if piece.color==piece1.color:
                return False, ""
            else:
                return True, "color"
    return True, ""
def score(listW):
    count_white =0
    count_black = 0
    for piece in listW:
        if piece.color=='white':
            if piece.name == 'pawn':
                if (piece.col0 == 3 or piece.col0 == 4 ) and piece.row0>=3:
                    count_white+=0.2
                elif (piece.col0 == 3 or piece.col0 == 4) and piece.row0==2:
                    count_white+=0.15
                elif (piece.col0 == 2 or piece.col0 == 5) and piece.row0>=3:
                    count_white+=0.1
                elif (piece.col0 == 2 or piece.col0 == 5) and piece.row0==2:
                    count_white+=0.05
                count_white+=1
            elif piece.name == 'bishop' or piece.name== 'knight':
                count_white+=3
            elif piece.name == 'rook':
                count_white+=5
            if piece.name == 'queen':
                count_white+=9
            #if check_check("black",True) and check_checkmate("black"):
                #count_white+=1000
        else:
            if piece.name == 'pawn':
                if (piece.col0 == 3 or piece.col0 == 4) and piece.row0<=4:
                    count_black+=0.2
                elif (piece.col0 == 3 or piece.col0 == 4) and piece.row0==5:
                    count_black+=0.15
                elif (piece.col0 == 2 or piece.col0 == 5) and piece.row0<=4:
                    count_black+=0.1
                elif (piece.col0 == 2 or piece.col0 == 5) and piece.row0==5:
                    count_black+=0.05
                count_black+=1
            elif piece.name == 'bishop' or piece.name== 'knight':
                count_black+=3
            elif piece.name == 'rook':
                count_black+=5
            if piece.name == 'queen':
                count_black+=9
            #if check_check("white",True) and check_checkmate("black"):
                #count_black+=1000
    return(count_white-count_black)

def prov_kl(x,y,maincolor):
    for piece in list:
            if piece.col0==x and (piece.row0==y or (piece.name=='pawn' and piece.row1==y)) and (not maincolor or piece.color==col_move):
                return piece,x,y
    return None,x,y
def prov_kl_l0(x,y):
    for piece in list0:
        if (piece.col0==x or piece.col0+1==x ) and (piece.row0 == y or piece.row0+1 == y or piece.row0+2 == y):
            return piece,x,y
    return None,x,y
def prov_kl_l2(x,y,maincolor):
    for piece in list2:
            if piece.col0==x and (piece.row0==y or (piece.name=='pawn' and piece.row1==y)) and (not maincolor or piece.color==col_move):
                return piece,x,y
    return None,x,y
def st_move(m,dictletters):
    p1 = prov_kl(int(dictletters[m[0]]),int(m[1])-1,False)[0]
    p2,xf,yf = prov_kl(int(dictletters[m[2]]),int(m[3])-1,False)
    return p1,p2,xf,yf
def check_check(color,userecursion):
    if not userecursion:
        return False
    x,y=0,0
    for piece1 in list:
            if piece1.name=='king' and piece1.color==color:
                x,y = piece1.col0,piece1.row0
    for piece in list:
        if piece.color!=color:
            vyd_loc = vyd_kl(piece.col0, piece.row0, piece, False)
            if vyd_loc != None:
                 del vyd_loc[0]
                 if [x, y] in vyd_loc and len([True for f in list if f.col0==piece.col0 and f.row0==piece.row0])==1:
                    return True

def get_best_move(col_move):
    global list
    if col_move == 'white':
        col_move = True
    else:
        col_move = False
    list_copy = list
    minimax(list, 3, -10000, 10000, col_move)
    list = list_copy
    print('best move: ', best_move_ever)
    return best_move_ever
def make_moves_from_current_position(move):
    print("make_moves_from_current_position")



def minimax(positionList, depth, alpha, beta, maximizingPlayer):
    global  best_move_ever
    if depth == 0:
        return score(positionList)
    if maximizingPlayer:
        maxEval = -10000
        child_list = new_pos(positionList,'white')
        for child in child_list:
            Eval = minimax(child.positionlist,depth-1,alpha,beta,False)
#            print('debug ', str(maximizingPlayer), child.move, str(Eval))
            if Eval > maxEval and depth == 3:
                best_move_ever = child.move
            maxEval = max(maxEval,Eval)
            alpha = max(alpha,Eval)
            if beta<= alpha:
                break
        return maxEval
    else:
        minEval = 10000
        child_list = new_pos(positionList,'black')
        for child in child_list:
            Eval = minimax(child.positionlist, depth - 1, alpha, beta, True)
#            print('debug ', str(maximizingPlayer), child.move, str(Eval))
            if Eval < minEval and depth == 3:
                best_move_ever = child.move
            minEval = min(minEval, Eval)
            beta = min(beta, Eval)
            if beta <= alpha:
                break
        return minEval

def menu():
    screen.fill(D_BLUE)
    text1 = f1.render('Chess', 1, (0, 255, 0))
    text2 = f2.render('Choose gamemode', 1, (0, 255, 0))
    text3 = f2.render('Pl vs Pl', 1, WHITE)
    text4 = f2.render('PL vs EC', 1, WHITE)
    text5 = f2.render('Pl vs HC', 1, RED)
    screen2.blit(text1, (380, 20))
    screen2.blit(text2, (300, 90))
    screen2.blit(text3, (130, 480))
    screen2.blit(text4, (380, 480))
    screen2.blit(text5, (660, 480))
    for piece in list0:
        piece.spawn_figure(dictmodes)
def check_checkmate(color):
    vyd = 0
    for piece in list:
        if piece.color==color:
            vyd_loc = vyd_kl(piece.col0, piece.row0, piece, True)
            if len(vyd_loc) >1:
                 vyd+=1
    if vyd == 0:
        return True
    return False
def spawnall(list,dictImages,vyd,promoting,list2):
    global b_m
    global b_mode
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
    if vyd != None:
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
        if figure.name!='pawnd':
            piece.spawn_figure(dictImages)
    if promoting and (not b_mode or not b_m):
        draw.rect(screen, 'blue', (130, 246, s_b * 5 + 60, s_b * 2 + 60))
        draw.rect(screen, 'white', (134, 250, s_b * 5 + 52, s_b * 2 + 52))
        for piece in list2:
            piece.spawn_figure(dictImages)

def vyd_kl(col1,row1,figure,userecursion):
        vyd = []
        vyd.append([col1,row1])
        if figure.name == 'knight':
            if col1-1>=0 and row1+2<=7 and prov_kl_m(figure,col1-1,row1+2)[0]:
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1 - 1, row1 + 2
                if not check_check(figure.color, userecursion):
                    vyd.append([col1 - 1, row1 + 2])
                figure.col0, figure.row0 = ka, b
            if col1+1<=7 and row1+2<=7 and prov_kl_m(figure,col1+1,row1+2)[0]:
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1 + 1, row1 + 2
                if not check_check(figure.color, userecursion):
                    vyd.append([col1 + 1, row1 + 2])
                figure.col0, figure.row0 = ka, b
            if col1-1>=0 and row1-2>=0 and prov_kl_m(figure,col1-1,row1-2)[0]:
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1 - 1, row1 - 2
                if not check_check(figure.color, userecursion):
                    vyd.append([col1 - 1, row1 -2])
                figure.col0, figure.row0 = ka, b
            if col1+1<=7 and row1-2>=0 and prov_kl_m(figure,col1+1,row1-2)[0]:
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1 + 1, row1 - 2
                if not check_check(figure.color, userecursion):
                    vyd.append([col1 +1, row1 -2])
                figure.col0, figure.row0 = ka, b
            if row1-1>=0 and col1+2<=7 and prov_kl_m(figure,col1+2,row1-1)[0]:
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1 + 2, row1 - 1
                if not check_check(figure.color, userecursion):
                    vyd.append([col1 + 2, row1 - 1])
                figure.col0, figure.row0 = ka, b
            if row1+1<=7 and col1+2<=7 and prov_kl_m(figure,col1+2,row1+1)[0]:
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1 + 2, row1 + 1
                if not check_check(figure.color, userecursion):
                    vyd.append([col1 + 2, row1 + 1])
                figure.col0, figure.row0 = ka, b
            if row1-1>=0 and col1-2>=0 and prov_kl_m(figure,col1-2,row1-1)[0]:
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1 - 2, row1 - 1
                if not check_check(figure.color, userecursion):
                    vyd.append([col1 - 2, row1 - 1])
                figure.col0, figure.row0 = ka, b
            if row1+1<=7 and col1-2>=0 and prov_kl_m(figure,col1-2,row1+1)[0]:
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1-2, row1+1
                if not check_check(figure.color, userecursion):
                    vyd.append([col1 - 2, row1 + 1])
                figure.col0, figure.row0 = ka, b
        if figure.name == 'rook':
            a = col1
            b = row1
            col1+=1
            while col1<8:
                if prov_kl_m(figure,col1,row1)[0]:
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
                    if prov_kl_m(figure,col1,row1)[1]=='color':
                        break
                else:
                    break
                col1 += 1
            col1 = a
            col1 -= 1
            while col1 > -1:
                if prov_kl_m(figure, col1, row1)[0]:
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
                    if prov_kl_m(figure,col1,row1)[1]=='color':
                        break
                else:
                    break
                col1 -= 1
            col1 = a
            row1 += 1
            while row1<8:
                if prov_kl_m(figure,col1,row1)[0]:
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
                    if prov_kl_m(figure,col1,row1)[1]=='color':
                        break
                else:
                    break
                row1 += 1
            row1 = b
            row1 -= 1
            while row1 > -1:
                if prov_kl_m(figure, col1, row1)[0]:
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
                    if prov_kl_m(figure,col1,row1)[1]=='color':
                        break
                else:
                    break
                col1 += 1
            col1 = a
            col1 -= 1
            while col1 > -1:
                if prov_kl_m(figure, col1, row1)[0]:
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
                    if prov_kl_m(figure,col1,row1)[1]=='color':
                        break
                else:
                    break
                col1 -= 1
            col1 = a
            row1 += 1
            while row1<8:
                if prov_kl_m(figure,col1,row1)[0]:
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
                    if prov_kl_m(figure,col1,row1)[1]=='color':
                        break
                else:
                    break
                row1 += 1
            row1 = b
            row1 -= 1
            while row1 > -1:
                if prov_kl_m(figure, col1, row1)[0]:
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1])
                    figure.col0, figure.row0 = ka, b
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
            kl = prov_kl(col1 + a, row1 + a, False)[0]
            if figure.color == 'white':
                if row1 == 1:
                    f = True
                a = 1
            else:
                if row1 == 6:
                    f = True
                a = -1
            if prov_kl_m(figure, col1, row1+a)[0] and prov_kl_m(figure, col1, row1+a)[1]=='':
                ka,b = figure.col0,figure.row0
                figure.col0,figure.row0 =  col1, row1+a
                if not check_check(figure.color,userecursion):
                    vyd.append([col1, row1+a])
                figure.col0, figure.row0 =  ka,b
                if f and prov_kl_m(figure, col1 , row1 +2*a)[0] and prov_kl_m(figure, col1, row1 + 2*a)[1] == '':
                    ka, b = figure.col0, figure.row0
                    figure.col0, figure.row0 = col1, row1 + 2*a
                    if not check_check(figure.color, userecursion):
                        vyd.append([col1, row1 + 2*a])
                    figure.col0, figure.row0 = ka, b
            if prov_kl_m(figure, col1 + a, row1 + a)[0] and prov_kl_m(figure, col1+a, row1 + a)[1] == 'color' :
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1+a, row1 + a
                if not check_check(figure.color, userecursion):
                    vyd.append([col1+a, row1 + a])
                figure.col0, figure.row0 = ka, b
            if prov_kl_m(figure, col1 - a, row1 + a)[0] and prov_kl_m(figure, col1-a, row1 + a)[1] == 'color':
                ka, b = figure.col0, figure.row0
                figure.col0, figure.row0 = col1-a, row1 + a
                if not check_check(figure.color, userecursion):
                    vyd.append([col1-a, row1 + a])
                figure.col0, figure.row0 = ka, b
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

    a = prov_kl(x, y,False)[0]
    #print(a)
    if a != None and a in list:
        list.remove(a)
    x1, y1 = 0, 0
    for piece1 in list:
        if piece1.name == 'king' and piece1.color == color:
            x1, y1 = piece1.col0, piece1.row0
    k1 = prov_kl(x1, y1, False)[0]
    if k1 != None and k1 in list:
        list.remove(k1)
    k_dop = True
    a_dop = True
    newking = chesspiece("king", color, x, y)
    list.append(newking)
    for piece in list:
        if piece.color!=color:
            vyd_loc = vyd_kl(piece.col0, piece.row0, piece, False)
            if vyd_loc != None:
                 del vyd_loc[0]
                 if [x, y] in vyd_loc:
                    list.remove(newking)
                    if a != None:
                        list.append(a)
                        a_dop = False
                    if k1 != None:
                        list.append(k1)
                        k_dop = False
                    return True
    list.remove(newking)
    if a != None and a_dop:
        list.append(a)
    if k1 != None and k_dop:
        list.append(k1)
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

col_move = 'white'
display.set_caption('Chess')
f1 = font.SysFont('comicsans', 55)
f2 = font.SysFont('comicsans', 45)
screen = display.set_mode((wids, lens))
screen2 = display.set_mode((wids * 1.25, lens))
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
p_v_p = transform.scale(brook, (200, 200))
p_v_ec = transform.scale(bishop, (200, 200))
p_v_hc = transform.scale(queen, (200, 200))
fg1= chesspiece("pawn","white",0,6)


dictImages = {}
col_move = 'white'
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

dictmodes = {}
dictmodes['brook'] = p_v_p
dictmodes['bishop'] = p_v_ec
dictmodes['queen'] = p_v_hc

dictletters = {}
dictletters['a'] = 7
dictletters['b'] = 6
dictletters['c'] = 5
dictletters['d'] = 4
dictletters['e'] = 3
dictletters['f'] = 2
dictletters['g'] = 1
dictletters['h'] = 0






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

list0 = []
list0.append(chesspiece("rook","black",1,3))
list0.append(chesspiece("bishop","white",4,3))
list0.append(chesspiece("queen","white",7,3))

wrook1m = False
wrook2m = False
wkingm = False
brook1m = False
brook2m = False
bkingm = False
rok = ''
move = False
g_vyd = []
maincl = True
list2 = []
promoting = False
main_menu = True
#save_lastf = chesspiece("pawn","white",0,1)
#save_figure = chesspiece("pawn","black",0,6)
wr1 = list[8]
wr2 = list[9]
br1 = list[24]
br2 = list[25]
a=1
s_mode = False
b_mode = False
s_m = False
b_m = False
running = True
mouse_use=True
#spawnall(list, dictImages, g_vyd, promoting, list2)
while running:
    do_handle_mouse_down = False
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            running = False
        elif ev.type == MOUSEBUTTONDOWN:
            do_handle_mouse_down = True
    if s_m and s_mode or b_m and b_mode:
        do_handle_mouse_down = True
    if do_handle_mouse_down:
        if s_m:
            move1 = stockfish.get_best_move()
            #print('best',move1)
            if move1 == 'e8g8' or move1 == "e1g1":
                rok = 'short'
            elif move1 == 'e8c8' or move1 == "e1c1":
                rok = 'long'
            lastf, figure, xf, yf = st_move(move1, dictletters)
            #if lastf == None:
               # print('warning')
        #if s_m:
            #score(list)
            #lfl = lastf
            #fl = figure
        if b_m:
            move2 = get_best_move(col_move)
            print(move2)
            # print('best',move1)
            if move2 == 'e8g8' or move2 == "e1g1":
                rok = 'short'
            elif move2 == 'e8c8' or move2 == "e1c1":
                rok = 'long'
            lastf, figure, xf, yf = st_move(move2, dictletters)
            # if lastf == None:
            # print('warning')
        if b_m or s_m:
            score(list)
            lfl = lastf
            fl = figure
        if promoting:
            if not s_mode or s_m:
                x_mouse, y_mouse = mouse.get_pos()
                col1 = x_mouse // (step + s_b)
                row1 = y_mouse // (step + s_b)
                figure, x, y = prov_kl_l2(col1, row1, maincl)
                if figure in list2:
                    prom = figure
                    promoting = False
                    fg1.name = prom.name
                    list2 = []
                    draw.rect(screen, BROWN, (130, 246, s_b * 5 + 60, s_b * 2 + 60))
                    spawnall(list, dictImages, g_vyd, promoting, list2)
                else:
                    continue
        elif main_menu:
            x_mouse, y_mouse = mouse.get_pos()
            col1 = x_mouse // (step + s_b)
            row1 = y_mouse // (step + s_b)
            figure, x, y = prov_kl_l0(col1, row1)
            if figure.name == "rook":
                main_menu = False
                screen.fill(BROWN)
            elif figure.name == "queen":
                s_mode = True
                main_menu = False
                screen.fill(BROWN)
                if randint(0, 1) == 0:
                    s_m = True
                else:
                    s_m = False
            elif figure.name == "bishop":
                b_mode = True
                main_menu = False
                screen.fill(BROWN)
                if randint(0, 1) == 0:
                    b_m = True
                else:
                    b_m = False
            else:
                continue
            text1 = f1.render('Move:', 1, (255, 255, 0))
            text2 = f2.render(col_move, 1, (255, 255, 0))
            screen2.blit(text1, (730, 30))
            screen2.blit(text2, (740, 90))
            spawnall(list, dictImages, g_vyd, promoting, list2)
        elif mouse_use:
            maincl = True
            coll = 0
            rowl = 0
            last = g_vyd
            lastf = figure
            # save_lastf = lastf
            x_mouse, y_mouse = mouse.get_pos()
            if not s_m and not b_m:
                col1 = x_mouse // (step + s_b)
                row1 = y_mouse // (step + s_b)
            else:
                col1 = xf
                row1 = yf
            if a == 1:
                maincl = True
            elif a == 0 and [col1, row1] in last[1:]:
                maincl = False
            figure, x, y = prov_kl(col1, row1, maincl)
            #             if figure != None:
            #                coll = figure.col0
            #                rowl = figure.row0
            #             else:
            coll = x
            rowl = y
            if s_m or b_m:
                lastf = lfl
                figure = fl
            if (last != None and [coll, rowl] in last[1:] and lastf != None) or s_m or b_m:
                if not s_m and s_mode:
                    move1 = chr(97 + 7-lastf.col0) + str(lastf.row0 + 1) + chr(97 +7- x) + str(y + 1)
                elif not b_m and b_mode:
                    move2 = chr(97 + 7 - lastf.col0) + str(lastf.row0 + 1) + chr(97 + 7 - x) + str(y + 1)
                if s_mode:
                    stockfish.make_moves_from_current_position([move1])
                elif b_mode:
                    make_moves_from_current_position(move2)
                save = list
                saveV = g_vyd
                if lastf.row0 - rowl == 2:
                    lastf.row1 = rowl + 1
                elif lastf.row0 - rowl == -2:
                    lastf.row1 = rowl - 1
                if figure in list:
                    if figure != lastf:
                        list.remove(figure)
                figure = lastf
                if ((figure.row0 == 6 and figure.color == 'white') or (
                        figure.row0 == 1 and figure.color == 'black')) and figure.name == 'pawn':
                    promoting = True
                    fg1 = figure
                if lastf.name == 'king':
                    if lastf.col0 - coll == 2:
                        rok = 'short'
                    if coll - lastf.col0 == 2:
                        rok = 'long'
                if rok == 'short':
                    if lastf.color == 'white':
                        wr1.col0 = coll + 1
                        rok = ''
                    else:
                        br1.col0 = coll + 1
                        rok = ''
                elif rok == 'long':
                    if lastf.color == 'white':
                        wr2.col0 = coll - 1
                        rok = ''
                    else:
                        br2.col0 = coll - 1
                        rok = ''

                lastf.col0 = coll
                lastf.row0 = rowl
                move = True
                g_vyd = []
                spawnall(list, dictImages, None, promoting, list2)
                if lastf.name == 'king':
                    if lastf.color == 'white':
                        wkingm = True
                    else:
                        bkingm = True
                if lastf.name == 'rook':
                    if lastf.color == 'white':
                        if x == 0 and y == 0:
                            wrook1m = True
                        else:
                            wrook2m = True
                    else:
                        if x == 0 and y == 7:
                            brook1m = True
                        else:
                            brook2m = True
                if s_mode and not s_m:
                    s_m = True
                elif s_mode:
                    s_m = False
                elif b_mode and b_m:
                    b_m = False
                elif b_mode:
                    b_m = True
            if figure != None:
                if move:
                    a = 1
                    col1 = col_move
                    if col_move == 'white':
                        col_move = 'black'
                    else:
                        col_move = 'white'
                    for piece in list:
                        if piece.color == col_move:
                            piece.row1 = -1
                    screen2.blit(f2.render('', 1, (255, 255, 0)), (740, 90))
                    text2 = f2.render(col_move, 1, (255, 255, 0))
                    draw.rect(screen2, BROWN, (740, 100, 200, 60))
                    screen2.blit(text2, (740, 90))
                    move = False
                    if b_mode and not b_m:
                        print(str(b_mode) + '+' + str(b_m))
                        promoting = False
                        fg1.name = 'queen'
                        spawnall(list, dictImages, g_vyd, promoting, list2)
                    if promoting:
                        list2.append(chesspiece("queen", col1, 2, 3))
                        list2.append(chesspiece("rook", col1, 2, 4))
                        list2.append(chesspiece("bishop", col1, 5, 3))
                        list2.append(chesspiece("knight", col1, 5, 4))
                        spawnall(list, dictImages, g_vyd, promoting, list2)
                    if check_checkmate(col_move) and check_check(col_move, True):
                        if col_move == 'white':
                            col_move = 'black'
                        else:
                            col_move = 'white'
                        draw.rect(screen2, BROWN, (730, 40, 200, 160))
                        text3 = f2.render(col_move, 1, (0, 255, 0))
                        text4 = f1.render('Winner', 1, (0, 255, 0))
                        screen2.blit(text4, (720, 30))
                        screen2.blit(text3, (740, 90))
                        mouse_use = False
                    elif check_checkmate(col_move):
                        draw.rect(screen2, BROWN, (730, 40, 200, 160))
                        text5 = f1.render('Draw', 1, (0, 255, 0))
                        screen2.blit(text5, (720, 30))
                        mouse_use = False

                else:
                    move = False
                    a = 0
                    g_vyd = vyd_kl(col1, row1, figure, True)
                    spawnall(list, dictImages, g_vyd, promoting, list2)

    if main_menu:
        menu()
    if running:
        display.update()
