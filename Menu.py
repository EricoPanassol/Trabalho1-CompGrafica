from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from ListaDeCoresRGB import *

def PrintString(S: str, x: int, y: int, cor: tuple):
    defineCor(cor)
    glRasterPos3f(x, y, 0)  # define posicao na tela

    for c in S:
        # GLUT_BITMAP_HELVETICA_10
        # GLUT_BITMAP_TIMES_ROMAN_24
        # GLUT_BITMAP_HELVETICA_18
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

def ImprimeMensagens():
    # PrintString(Mensagens[len(PontosClicados)-1], -14, 13, White)
   
    # if(len(PontosClicados) == 0):
    #     PrintString("Clique no 1° ponto", -14, 13, White)
    # elif(len(PontosClicados) == 1):
    #     PrintString("Clique no 2° ponto", -14, 13, White)
    # else:
    #     PrintString("Clique no 3° ponto", -14, 13, White)
   
    # if nPontoAtual > 0:
    #     PrintString("Ultimo ponto clicado: ", -14, 11, Red)
    #     ImprimePonto(PontosClicados[nPontoAtual-1], -14, 9, Red)

    # PrintString("Mouse pos: ", -14, 11, White)
    # ImprimePonto(PosAtualDoMouse, -11, 11, White)

    # PrintString("Mouse: ", -14, 9, White)
    # PrintString("Down", -12, 9,White) if mouseClicked else PrintString("Up", -12, 9, White)
   
    # PrintString("N° Curvas: ", -14, 7, White)
    # PrintString(str(len(Curvas)), -11, 7, White)
    # PrintString(str(mode), -1, 11, White)
    PrintString("", -11, 13, DarkBrown)
    desenhaQuadrado(-15,15,-5,10)
    PrintString("Modos ", -11, 13, OrangeRed)
   
    PrintString("Modo A", -14, 11, MandarinOrange)
    desenhaQuadrado(-14,11,-12,12)
    PrintString("Modo B", -11, 11, MandarinOrange)
    desenhaQuadrado(-11,11,-9,12)
    PrintString("Modo C", -8, 11, MandarinOrange)
    desenhaQuadrado(-8,11,-6,12)

    PrintString("", -11, 13, DarkBrown)
    desenhaQuadrado(-5,15,15,10)
    PrintString("Modos de edição de curva", 2, 13, OrangeRed)

    PrintString("Remove Curva",-4,11,MandarinOrange)
    desenhaQuadrado(-4,11,-0.6,12)
    PrintString("Movimenta Vértice",0,11,MandarinOrange)
    desenhaQuadrado(0,11,4.4,12)
    PrintString("Conecta curvas",5,11,MandarinOrange)
    desenhaQuadrado(5,11,8,12)
    PrintString("Atualiza continuidade entre curvas:",9,11,MandarinOrange)
    desenhaQuadrado(9,11,15,12)
    

def desenhaQuadrado(x1:int,y1:int,x2:int,y2:int):
    glBegin(GL_LINES)
    #  eixo horizontal
    glVertex2f(x1, y1-0.3)
    glVertex2f(x2, y1-0.3)
    glVertex2f(x1, y2)
    glVertex2f(x2, y2)
    #  eixo vertical
    glVertex2f(x1, y2)
    glVertex2f(x1, y1-0.3)
    glVertex2f(x2, y2)
    glVertex2f(x2, y1-0.3)
    glEnd()