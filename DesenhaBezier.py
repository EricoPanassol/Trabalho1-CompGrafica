# ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa cria um conjunto de INSTANCIAS
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from Poligonos import *
from InstanciaBZ import *
from Bezier import *
from ListaDeCoresRGB import *
import math
# ***********************************************************************************

# Modelos de Objetos
MeiaSeta = Polygon()
Mastro = Polygon()

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# lista de instancias do Personagens
Personagens = []

# ***********************************************************************************
# Lista de curvas Bezier
Curvas = []

# Variaveis de controle da curva Bezier
Curvas = []
PontosClicados = []
PoligonoDeControle = None
desenhaPoligonoControle = True

Linha = []
LinhaDerviada = []
Poligonos = []

PosAtualDoMouse = Ponto()
nPontoAtual = 0
mouseClicked = False
arrastaCurva = False
bloqueiaSubida = False
removerPoli = False
movePonto = True
movendoPonto = False
movendoPontoDerivada = False
casoPontoDerivada = 0

# **********************************************************************
# Lista de mensagens
# **********************************************************************
Mensagens = [
    "Clique o 2° ponto.",
    "Clique o 3° ponto.",
    "Clique o 1° ponto.",
]

MouseState = [
    "Mouse down",
    "Mouse up"
]

angulo = 0.0
desenha = True

mode = 0
pontoAuxiliar = Ponto()
pontoAuxiliar2 = Ponto()
aux = True
primeiraExecucaoModo1 = True
id = 0
PontosDerivadas = []
pontosAntecedentes = 0

# **********************************************************************
# Imprime o texto S na posicao (x,y), com a cor 'cor'
# **********************************************************************


def PrintString(S: str, x: int, y: int, cor: tuple):
    defineCor(cor)
    glRasterPos3f(x, y, 0)  # define posicao na tela

    for c in S:
        # GLUT_BITMAP_HELVETICA_10
        # GLUT_BITMAP_TIMES_ROMAN_24
        # GLUT_BITMAP_HELVETICA_18
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))


# **********************************************************************
# Imprime as coordenadas do ponto P na posicao (x,y), com a cor 'cor'
# **********************************************************************
def ImprimePonto(P: Ponto, x: int, y: int, cor: tuple):
    S = f'({P.x:.2f}, {P.y:.2f})'
    PrintString(S, x, y, cor)

# **********************************************************************
#  Imprime as mensagens do programa.
#  Funcao chamada na 'display'
# **********************************************************************


def ImprimeMensagens():
    #PrintString(Mensagens[len(PontosClicados)-1], -14, 13, White)
   
    # if(len(PontosClicados) == 0):
    #     PrintString("Clique no 1° ponto", -14, 13, White)
    # elif(len(PontosClicados) == 1):
    #     PrintString("Clique no 2° ponto", -14, 13, White)
    # else:
    #     PrintString("Clique no 3° ponto", -14, 13, White)
   
    # if nPontoAtual > 0:
    #     PrintString("Ultimo ponto clicado: ", -14, 11, Red)
    #     ImprimePonto(PontosClicados[nPontoAtual-1], -14, 9, Red)

    PrintString("Mouse pos: ", -14, 11, White)
    ImprimePonto(PosAtualDoMouse, -11, 11, White)

    PrintString("Mouse: ", -14, 9, White)
    PrintString("Down", -12, 9,White) if mouseClicked else PrintString("Up", -12, 9, White)
   
    PrintString("N° Curvas: ", -14, 7, White)
    PrintString(str(len(Curvas)), -11, 7, White)
   
    PrintString("Mode: ", -14, 5, White)
    PrintString(str(mode), -12, 5, White)


# **********************************************************************
def animate():
    glutPostRedisplay()


# ***********************************************************************************
def reshape(w, h):
    global Min, Max

    # Reseta sistema de coordenadas antes de modifica-lo
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Define a area a ser ocupada pela area OpenGL dentro da Janela
    glViewport(0, 0, w, h)

    # Define os limites logicos da area OpenGL dentro da Janela
    glOrtho(Min.x, Max.x, Min.y, Max.y, -10, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# **************************************************************


def DesenhaEixos():
    global Min, Max

    Meio = Ponto()
    Meio.x = (Max.x+Min.x)/2
    Meio.y = (Max.y+Min.y)/2
    Meio.z = (Max.z+Min.z)/2

    glBegin(GL_LINES)
    #  eixo horizontal
    glVertex2f(Min.x, Meio.y)
    glVertex2f(Max.x, Meio.y)
    #  eixo vertical
    glVertex2f(Meio.x, Min.y)
    glVertex2f(Meio.x, Max.y)
    glEnd()

# **************************************************************


def CarregaModelos():
    global MeiaSeta, Mastro
    MeiaSeta.LePontosDeArquivo("MeiaSeta.txt")
    Mastro.LePontosDeArquivo("Mastro.txt")

# **************************************************************


def CriaCurvas():
    global Curvas
    global primeiraExecucaoModo1
    global id
    global mode
    
    if(mode == 0):
        C = Bezier(PontosClicados[0], PontosClicados[1], PontosClicados[2])
        C.setTipo(0)
        C.setId(id)
    elif(mode == 1):
        C = Bezier(PontosClicados[0], PontosClicados[1], PontosClicados[2])
        C.setTipo(1)
        C.setId(id)
    else:
        C = Bezier(PontosClicados[0], PontosClicados[1], PontosClicados[2])
        C.setTipo(2)
        C.setId(id)
        
    if (arrastaCurva == True):
        Curvas[len(Curvas)-1] = C
    else:
        Curvas.append(C)
    primeiraExecucaoModo1 = False

# ***********************************************************************************
def init():
    global Min, Max
    # Define a cor do fundo da tela (PRETO)
    glClearColor(0, 0, 0, 0)

    CarregaModelos()

    d: float = 15
    Min = Ponto(-d, -d)
    Max = Ponto(d, d)

# ***********************************************************************************


def DesenhaLinha(P1: Ponto, P2: Ponto):
    glBegin(GL_LINES)
    glVertex3f(P1.x, P1.y, P1.z)
    glVertex3f(P2.x, P2.y, P2.z)
    glEnd()

# ***********************************************************************************


def DesenhaCurvas():
    global desenhaPoligonoControle
   
    # desenhaPoligonoControle = True
   
    for I in Curvas:
        defineCor(Aquamarine)
        I.Traca()
        if(desenhaPoligonoControle):
            defineCor(IndianRed)
            I.TracaPoligonoDeControle()

# **********************************************************************


def DesenhaPontos():
    defineCor(BlueViolet)
    glPointSize(7)
    glBegin(GL_POINTS)

    for Ponto in PontosClicados:
        glVertex2f(Ponto.x, Ponto.y)
    glEnd()
    glPointSize(1)

# **********************************************************************


def DesenhaMenu():
    glPushMatrix()
    glTranslated(11, 13, 0)  # veja o arquivo MeiaSeta.txt
    MeiaSeta.desenhaPoligono()
    glPopMatrix()

# ***********************************************************************************


def display():

    # Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Define os limites lógicos da área OpenGL dentro da Janela
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # Coloque aqui as chamadas das rotinas que desenham os objetos
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    glLineWidth(1)
    defineCor(White)

    DesenhaMenu()
    DesenhaEixos()

    nPontoAtual = len(PontosClicados)

    if (nPontoAtual):
        DesenhaLinha(PontosClicados[nPontoAtual-1], PosAtualDoMouse)

    if (len(Linha) > 1 and desenhaPoligonoControle):
        DesenhaLinha(Linha[0], Linha[1])

    glLineWidth(3)
    defineCor(Red)
    DesenhaPontos()
    DesenhaCurvas()
    ImprimeMensagens()

    glutSwapBuffers()


# ***********************************************************************************
# The function called whenever a key is pressed.
# Note the use of Python tuples to pass in: (key, x, y)
# ESCAPE = '\033'
# ***********************************************************************************
ESCAPE = b'\x1b'


def keyboard(*args):
    global desenha

    # If escape is pressed, kill everything.
    if args[0] == b' ':
        desenha = not desenha
    if args[0] == ESCAPE:
        os._exit(0)
    # Forca o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )
# **********************************************************************


def arrow_keys(a_keys: int, x: int, y: int):
    global desenhaPoligonoControle, mode, primeiraExecucaoModo1, id
   
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        glutFullScreen()

    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        desenhaPoligonoControle = not desenhaPoligonoControle
       
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        if(mode <= 0):
            mode = 0
            clear()
        else:
            primeiraExecucaoModo1 = True
            mode -= 1
            id = id + 1
            clear()
       
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        if(mode >= 2):
            mode = 2
            clear()
        else:
            primeiraExecucaoModo1 = True
            mode += 1
            id = id + 1
            clear()
           
    print("mode =", mode)

    glutPostRedisplay()


def clear():
    global nPontoAtual
    PontosClicados.clear()
    LinhaDerviada.clear()
    Linha.clear()
    nPontoAtual = 0
   
def dist(x1, y1, x2, y2, x3, y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    norm = px*px + py*py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    dist = (dx*dx + dy*dy)**.5

    return dist

# **********************************************************************
# Converte as coordenadas do ponto P de coordenadas de tela para
# coordenadas de universo (sistema de referencia definido na glOrtho
# (ver funcao reshape)
# Este codigo e baseado em http://hamala.se/forums/viewtopic.php?t=20
# **********************************************************************


def ConvertePonto(P: Ponto) -> Ponto:
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    wx, wy, wz = P.x, P.y, 0.0
    P.y = viewport[3] - P.y
    wy = P.y
    wz = glReadPixels(P.x, P.y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    ox, oy, oz = gluUnProject(wx, wy, wz, modelview, projection, viewport)

    return Ponto(ox, oy, oz)

# ***********************************************************************************
# Captura o clique do botao esquerdo do mouse sobre a area de desenho
# ***********************************************************************************


def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    global PosAtualDoMouse
    global mouseClicked
    global nPontoAtual
    global curvaCriada
    global arrastaCurva
    global bloqueiaSubida
    global Linha
    global mode
    global primeiraExecucaoModo1
    global desenhaPoligonoControle
    global pontoAuxiliar
    global pontoAuxiliar2
    global aux
    global pontosPoli
    global removerPoli
    global movePonto
    global pontoMovendo
    global movendoPonto
    global movendoPontoDerivada
    global casoPontoDerivada
    global PontosDerivadas
    global pontosAntecedentes
    global id
    pontosAntecedentes = 1
    curvaCriada = False
    movendoPonto = False
    movendoPontoDerivada = False
    PontosDerivadas.clear()
    # mode = 2

    # **********************************************************************************
    # ********************** MODE 0 - SEM CONTINUIDADE  ********************************
    # **********************************************************************************
   
    if (mode == 0):
        if (arrastaCurva == True or len(PontosClicados) == 3):
            PontosClicados.clear()

        if (button == GLUT_RIGHT_BUTTON):
            if (state == GLUT_DOWN):
                if(removerPoli == True):
                    PontoAtual = ConvertePonto(Ponto(x, y))
                    count = 0
                    for curva in Curvas:
                        pontosPoli = curva.GetPontos()
                        print(PontoAtual.GetX(), PontoAtual.GetY())
                        a = dist(pontosPoli[0].GetX(), pontosPoli[0].GetY(), pontosPoli[1].GetX(), pontosPoli[1].GetY(), PontoAtual.GetX(), PontoAtual.GetY())
                        b = dist(pontosPoli[0].GetX(), pontosPoli[0].GetY(), pontosPoli[2].GetX(), pontosPoli[2].GetY(), PontoAtual.GetX(), PontoAtual.GetY())
                        c = dist(pontosPoli[1].GetX(), pontosPoli[1].GetY(), pontosPoli[2].GetX(), pontosPoli[2].GetY(), PontoAtual.GetX(), PontoAtual.GetY())
                        print(a, b, c)
                        if((a < 0.2 and a > -0.2) or (b < 0.2 and b > -0.2) or (c < 0.2 and c > -0.2)):
                            Curvas.pop(count)
                            primeiraExecucaoModo1 = True
                            break
                        count = count + 1
                elif(movePonto == True):
                    PontoAtual = ConvertePonto(Ponto(x, y))
                    count = 0
                    for curva in Curvas:
                        pontosPoli = curva.GetPontos()
                        idTemp = curva.getId()
                        print(curva.getTipo())
                        if(curva.getTipo() != 2):
                            print(PontoAtual.GetX(), PontoAtual.GetY())
                            a = math.dist([pontosPoli[0].GetX(), pontosPoli[0].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            b = math.dist([pontosPoli[1].GetX(), pontosPoli[1].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            c = math.dist([pontosPoli[2].GetX(), pontosPoli[2].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            if(a > -0.4 and a < 0.4):
                                pontoMovendo = pontosPoli[0]
                                movendoPonto = True
                                break
                            elif(b > -0.4 and b < 0.4):
                                pontoMovendo = pontosPoli[1]
                                movendoPonto = True
                                break
                            elif(c > -0.4 and c < 0.4):
                                pontoMovendo = pontosPoli[2]
                                movendoPonto = True
                                break
                        else:
                            a = math.dist([pontosPoli[0].GetX(), pontosPoli[0].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            b = math.dist([pontosPoli[1].GetX(), pontosPoli[1].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            c = math.dist([pontosPoli[2].GetX(), pontosPoli[2].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            if(a > -0.4 and a < 0.4):
                                pontoMovendo = pontosPoli[0]
                                movendoPonto = True
                                break
                            elif(b > -0.4 and b < 0.4):
                                pontoMovendo = pontosPoli[1]
                                if(count != 0):
                                    if(count != len(Curvas)-1):
                                        if((Curvas[count-1].getId() != idTemp) and (Curvas[count+1].getId() != idTemp)):
                                            movendoPonto = True
                                            break
                                        else:
                                            movendoPontoDerivada = True
                                            casoPontoDerivada = 1
                                    else:
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 1
                                elif(count != len(Curvas)-1):
                                    if(Curvas[count+1].getId() == idTemp):
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 1
                                    else:
                                        movendoPonto = True
                                        break  
                                else:
                                    movendoPonto = True
                                    break
                                PontosDerivadas.append(pontosPoli[0])
                                PontosDerivadas.append(pontosPoli[1])
                                PontosDerivadas.append(pontosPoli[2]) 
                                if(count != 0):
                                    countAux1 = count - 1
                                    while(True):
                                        if(Curvas[countAux1].getId() == idTemp):
                                            PontosDerivadas.insert(0, Curvas[countAux1].GetPontos()[1])
                                            PontosDerivadas.insert(0, Curvas[countAux1].GetPontos()[0])
                                            pontosAntecedentes = pontosAntecedentes + 2
                                        else:
                                            break
                                        countAux1 = countAux1 - 1
                                        if(countAux1 < 0):
                                            break
                                        
                                if(count != len(Curvas)-1):
                                    countAux2 = count + 1
                                    while(True):
                                        if(Curvas[countAux2].getId() == idTemp):
                                            PontosDerivadas.append(Curvas[countAux2].GetPontos()[1])
                                            PontosDerivadas.append(Curvas[countAux2].GetPontos()[2])
                                        else:
                                            break
                                        countAux2 = countAux2 + 1
                                        if(countAux2 == len(Curvas)):
                                            break              
                            elif(c > -0.4 and c < 0.4):
                                pontoMovendo = pontosPoli[2]
                                if((count != 0) and (count != len(Curvas)-1)):
                                    if((Curvas[count-1].getId() != idTemp) and (Curvas[count+1].getId() != idTemp)):
                                        movendoPonto = True
                                        break
                                    else:
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 2
                                elif(count == 0 and (count != len(Curvas)-1)):
                                    if(Curvas[count+1].getId() == idTemp):
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 2
                                    else:
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 2
                                else:
                                    movendoPonto = True
                                    break
                                PontosDerivadas.append(pontosPoli[1])
                                PontosDerivadas.append(pontosPoli[2])
                                if(not(count >= len(Curvas)-1)):
                                    while(Curvas[count+1].getId() == idTemp):
                                        PontosDerivadas.append(Curvas[count+1].GetPontos()[1]) 
                                        PontosDerivadas.append(Curvas[count+1].GetPontos()[2]) 
                                        count = count + 1
                                        if(count >= len(Curvas)-1):
                                            break
                                break
                        count = count + 1

        if (button == GLUT_LEFT_BUTTON):
            if (state == GLUT_DOWN):
                # print("Mouse down")
                mouseClicked = True
                if (len(PontosClicados) == 2):
                    bloqueiaSubida = True
                PontosClicados.append(ConvertePonto(Ponto(x, y)))
                Linha.append(ConvertePonto(Ponto(x, y)))
                PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]

            if (state == GLUT_UP):
                # print("Mouse up")
                mouseClicked = False

                if (bloqueiaSubida == False):
                    PontosClicados.append(ConvertePonto(Ponto(x, y)))
                    Linha.append(ConvertePonto(Ponto(x, y)))
                    PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]

                bloqueiaSubida = False

        if (arrastaCurva == True):
            arrastaCurva = False

        if len(PontosClicados) == 3:
            CriaCurvas()
            curvaCriada = True
            Linha.clear()

        if (state == GLUT_DOWN and len(PontosClicados) == 2):
            return
        if (button == GLUT_RIGHT_BUTTON):
            return

    # **********************************************************************************
    # ********************** MODE 1 - CONTINUIDADE DE POSIÇÃO **************************
    # **********************************************************************************

    elif (mode == 1):
        if(arrastaCurva == True or len(PontosClicados) == 3):
            pontoAuxiliar = PontosClicados[2]
            PontosClicados.clear()
   
        if(button == GLUT_RIGHT_BUTTON):
            if (state == GLUT_DOWN):
                if(removerPoli == True):
                    PontoAtual = ConvertePonto(Ponto(x, y))
                    count = 0
                    for curva in Curvas:
                        pontosPoli = curva.GetPontos()
                        print(PontoAtual.GetX(), PontoAtual.GetY())
                        a = dist(pontosPoli[0].GetX(), pontosPoli[0].GetY(), pontosPoli[1].GetX(), pontosPoli[1].GetY(), PontoAtual.GetX(), PontoAtual.GetY())
                        b = dist(pontosPoli[0].GetX(), pontosPoli[0].GetY(), pontosPoli[2].GetX(), pontosPoli[2].GetY(), PontoAtual.GetX(), PontoAtual.GetY())
                        c = dist(pontosPoli[1].GetX(), pontosPoli[1].GetY(), pontosPoli[2].GetX(), pontosPoli[2].GetY(), PontoAtual.GetX(), PontoAtual.GetY())
                        print(a, b, c)
                        if((a < 0.2 and a > -0.2) or (b < 0.2 and b > -0.2) or (c < 0.2 and c > -0.2)):
                            Curvas.pop(count)
                            primeiraExecucaoModo1 = True
                            break
                        count = count + 1
                elif(movePonto == True):
                    PontoAtual = ConvertePonto(Ponto(x, y))
                    count = 0
                    for curva in Curvas:
                        pontosPoli = curva.GetPontos()
                        idTemp = curva.getId()
                        print(curva.getTipo())
                        if(curva.getTipo() != 2):
                            print(PontoAtual.GetX(), PontoAtual.GetY())
                            a = math.dist([pontosPoli[0].GetX(), pontosPoli[0].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            b = math.dist([pontosPoli[1].GetX(), pontosPoli[1].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            c = math.dist([pontosPoli[2].GetX(), pontosPoli[2].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            if(a > -0.4 and a < 0.4):
                                pontoMovendo = pontosPoli[0]
                                movendoPonto = True
                                break
                            elif(b > -0.4 and b < 0.4):
                                pontoMovendo = pontosPoli[1]
                                movendoPonto = True
                                break
                            elif(c > -0.4 and c < 0.4):
                                pontoMovendo = pontosPoli[2]
                                movendoPonto = True
                                break
                        else:
                            a = math.dist([pontosPoli[0].GetX(), pontosPoli[0].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            b = math.dist([pontosPoli[1].GetX(), pontosPoli[1].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            c = math.dist([pontosPoli[2].GetX(), pontosPoli[2].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            if(a > -0.4 and a < 0.4):
                                pontoMovendo = pontosPoli[0]
                                movendoPonto = True
                                break
                            elif(b > -0.4 and b < 0.4):
                                pontoMovendo = pontosPoli[1]
                                if(count != 0):
                                    if(count != len(Curvas)-1):
                                        if((Curvas[count-1].getId() != idTemp) and (Curvas[count+1].getId() != idTemp)):
                                            movendoPonto = True
                                            break
                                        else:
                                            movendoPontoDerivada = True
                                            casoPontoDerivada = 1
                                    else:
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 1
                                elif(count != len(Curvas)-1):
                                    if(Curvas[count+1].getId() == idTemp):
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 1
                                    else:
                                        movendoPonto = True
                                        break  
                                else:
                                    movendoPonto = True
                                    break
                                PontosDerivadas.append(pontosPoli[0])
                                PontosDerivadas.append(pontosPoli[1])
                                PontosDerivadas.append(pontosPoli[2]) 
                                if(count != 0):
                                    countAux1 = count - 1
                                    while(True):
                                        if(Curvas[countAux1].getId() == idTemp):
                                            PontosDerivadas.insert(0, Curvas[countAux1].GetPontos()[1])
                                            PontosDerivadas.insert(0, Curvas[countAux1].GetPontos()[0])
                                            pontosAntecedentes = pontosAntecedentes + 2
                                        else:
                                            break
                                        countAux1 = countAux1 - 1
                                        if(countAux1 < 0):
                                            break
                                        
                                if(count != len(Curvas)-1):
                                    countAux2 = count + 1
                                    while(True):
                                        if(Curvas[countAux2].getId() == idTemp):
                                            PontosDerivadas.append(Curvas[countAux2].GetPontos()[1])
                                            PontosDerivadas.append(Curvas[countAux2].GetPontos()[2])
                                        else:
                                            break
                                        countAux2 = countAux2 + 1
                                        if(countAux2 == len(Curvas)):
                                            break              
                            elif(c > -0.4 and c < 0.4):
                                pontoMovendo = pontosPoli[2]
                                if((count != 0) and (count != len(Curvas)-1)):
                                    if((Curvas[count-1].getId() != idTemp) and (Curvas[count+1].getId() != idTemp)):
                                        movendoPonto = True
                                        break
                                    else:
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 2
                                elif(count == 0 and (count != len(Curvas)-1)):
                                    if(Curvas[count+1].getId() == idTemp):
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 2
                                    else:
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 2
                                else:
                                    movendoPonto = True
                                    break
                                PontosDerivadas.append(pontosPoli[1])
                                PontosDerivadas.append(pontosPoli[2])
                                if(not(count >= len(Curvas)-1)):
                                    while(Curvas[count+1].getId() == idTemp):
                                        PontosDerivadas.append(Curvas[count+1].GetPontos()[1]) 
                                        PontosDerivadas.append(Curvas[count+1].GetPontos()[2]) 
                                        count = count + 1
                                        if(count >= len(Curvas)-1):
                                            break
                                break
                        count = count + 1
               
        if(button == GLUT_LEFT_BUTTON):
            if(state == GLUT_DOWN):
                print("Mouse down")
                mouseClicked = True;
                if(len(PontosClicados) == 2):
                    bloqueiaSubida = True
                if(primeiraExecucaoModo1 == False):
                    PontosClicados.append(pontoAuxiliar)
                if(primeiraExecucaoModo1 == True):
                    PontosClicados.append(ConvertePonto(Ponto(x, y)))
                    Linha.append(ConvertePonto(Ponto(x,y)))
                    PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
               
               
               
               
            if(state == GLUT_UP):
                print("Mouse up")
                mouseClicked = False;
                   
                if(bloqueiaSubida == False):
                    PontosClicados.append(ConvertePonto(Ponto(x, y)))
                    Linha.append(ConvertePonto(Ponto(x,y)))
                    PosAtualDoMouse = PontosClicados[len(PontosClicados)-1];
                   
                bloqueiaSubida = False
                # nPontoAtual += 1
                # print(f"Pontos clicados: {nPontoAtual}")
               
                # PosAtualDoMouse = PontosClicados[nPontoAtual-1]
       
        if(arrastaCurva == True):
            arrastaCurva = False
       
       
        if len(PontosClicados) == 3:
            CriaCurvas()
            curvaCriada = True;
            Linha.clear()
           
           
        if(state == GLUT_DOWN and len(PontosClicados) == 2):
            return
        if(button == GLUT_RIGHT_BUTTON):
            return
       
    # **********************************************************************************
    # ********************** MODE 2 - CONTINUIDADE DE DERIVADA *************************
    # **********************************************************************************
   
    elif(mode == 2):
        if (button == GLUT_RIGHT_BUTTON):
            clear()
            id = id + 1
            
            if (state == GLUT_DOWN):
                if(removerPoli == True):
                    PontoAtual = ConvertePonto(Ponto(x, y))
                    count = 0
                    for curva in Curvas:
                        pontosPoli = curva.GetPontos()
                        print(PontoAtual.GetX(), PontoAtual.GetY())
                        a = dist(pontosPoli[0].GetX(), pontosPoli[0].GetY(), pontosPoli[1].GetX(), pontosPoli[1].GetY(), PontoAtual.GetX(), PontoAtual.GetY())
                        b = dist(pontosPoli[0].GetX(), pontosPoli[0].GetY(), pontosPoli[2].GetX(), pontosPoli[2].GetY(), PontoAtual.GetX(), PontoAtual.GetY())
                        c = dist(pontosPoli[1].GetX(), pontosPoli[1].GetY(), pontosPoli[2].GetX(), pontosPoli[2].GetY(), PontoAtual.GetX(), PontoAtual.GetY())
                        print(a, b, c)
                        if((a < 0.2 and a > -0.2) or (b < 0.2 and b > -0.2) or (c < 0.2 and c > -0.2)):
                            Curvas.pop(count)
                            primeiraExecucaoModo1 = True
                            break
                        count = count + 1
                elif(movePonto == True):
                    PontoAtual = ConvertePonto(Ponto(x, y))
                    count = 0
                    for curva in Curvas:
                        pontosPoli = curva.GetPontos()
                        idTemp = curva.getId()
                        print(curva.getTipo())
                        if(curva.getTipo() != 2):
                            print(PontoAtual.GetX(), PontoAtual.GetY())
                            a = math.dist([pontosPoli[0].GetX(), pontosPoli[0].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            b = math.dist([pontosPoli[1].GetX(), pontosPoli[1].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            c = math.dist([pontosPoli[2].GetX(), pontosPoli[2].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            if(a > -0.4 and a < 0.4):
                                pontoMovendo = pontosPoli[0]
                                movendoPonto = True
                                break
                            elif(b > -0.4 and b < 0.4):
                                pontoMovendo = pontosPoli[1]
                                movendoPonto = True
                                break
                            elif(c > -0.4 and c < 0.4):
                                pontoMovendo = pontosPoli[2]
                                movendoPonto = True
                                break
                        else:
                            a = math.dist([pontosPoli[0].GetX(), pontosPoli[0].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            b = math.dist([pontosPoli[1].GetX(), pontosPoli[1].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            c = math.dist([pontosPoli[2].GetX(), pontosPoli[2].GetY()], [PontoAtual.GetX(), PontoAtual.GetY()])
                            if(a > -0.4 and a < 0.4):
                                pontoMovendo = pontosPoli[0]
                                movendoPonto = True
                                break
                            elif(b > -0.4 and b < 0.4):
                                pontoMovendo = pontosPoli[1]
                                if(count != 0):
                                    if(count != len(Curvas)-1):
                                        if((Curvas[count-1].getId() != idTemp) and (Curvas[count+1].getId() != idTemp)):
                                            movendoPonto = True
                                            break
                                        else:
                                            movendoPontoDerivada = True
                                            casoPontoDerivada = 1
                                    else:
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 1
                                elif(count != len(Curvas)-1):
                                    if(Curvas[count+1].getId() == idTemp):
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 1
                                    else:
                                        movendoPonto = True
                                        break  
                                else:
                                    movendoPonto = True
                                    break
                                PontosDerivadas.append(pontosPoli[0])
                                PontosDerivadas.append(pontosPoli[1])
                                PontosDerivadas.append(pontosPoli[2]) 
                                if(count != 0):
                                    countAux1 = count - 1
                                    while(True):
                                        if(Curvas[countAux1].getId() == idTemp):
                                            PontosDerivadas.insert(0, Curvas[countAux1].GetPontos()[1])
                                            PontosDerivadas.insert(0, Curvas[countAux1].GetPontos()[0])
                                            pontosAntecedentes = pontosAntecedentes + 2
                                        else:
                                            break
                                        countAux1 = countAux1 - 1
                                        if(countAux1 < 0):
                                            break
                                        
                                if(count != len(Curvas)-1):
                                    countAux2 = count + 1
                                    while(True):
                                        if(Curvas[countAux2].getId() == idTemp):
                                            PontosDerivadas.append(Curvas[countAux2].GetPontos()[1])
                                            PontosDerivadas.append(Curvas[countAux2].GetPontos()[2])
                                        else:
                                            break
                                        countAux2 = countAux2 + 1
                                        if(countAux2 == len(Curvas)):
                                            break              
                            elif(c > -0.4 and c < 0.4):
                                pontoMovendo = pontosPoli[2]
                                if((count != 0) and (count != len(Curvas)-1)):
                                    if((Curvas[count-1].getId() != idTemp) and (Curvas[count+1].getId() != idTemp)):
                                        movendoPonto = True
                                        break
                                    else:
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 2
                                elif(count == 0 and (count != len(Curvas)-1)):
                                    if(Curvas[count+1].getId() == idTemp):
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 2
                                    else:
                                        movendoPontoDerivada = True
                                        casoPontoDerivada = 2
                                else:
                                    movendoPonto = True
                                    break
                                PontosDerivadas.append(pontosPoli[1])
                                PontosDerivadas.append(pontosPoli[2])
                                if(not(count >= len(Curvas)-1)):
                                    while(Curvas[count+1].getId() == idTemp):
                                        PontosDerivadas.append(Curvas[count+1].GetPontos()[1]) 
                                        PontosDerivadas.append(Curvas[count+1].GetPontos()[2]) 
                                        count = count + 1
                                        if(count >= len(Curvas)-1):
                                            break
                                break
                        count = count + 1

        if (arrastaCurva == True or nPontoAtual == 3):
           
            pontoAuxiliar = PontosClicados[2]  
            pontoAuxiliar2 = PontosClicados[1]
           
            LinhaDerviada.append(pontoAuxiliar)
            LinhaDerviada.append(pontoAuxiliar2)
           
            # ************************************
            # LinhaDerivada[0] = PontosClicados[2]
            # LinhaDerivada[1] = PontosClicados[1]
            # ************************************
           
            vetBC = LinhaDerviada[0].__sub__(LinhaDerviada[1])
            vetBC.imprime("Dist entre LD[0] - LD[1], vetBC =")
           
            d = LinhaDerviada[0].__add__(vetBC)
            d.imprime("Ponto D =")
           
            PontosClicados.clear()
            PontosClicados.append(pontoAuxiliar)
            PontosClicados.append(d)
           
            Linha.clear()
            LinhaDerviada.clear()
            Linha.append(pontoAuxiliar)
           
            nPontoAtual = 2
            # aux = False
           
           
        if (button == GLUT_LEFT_BUTTON):
            if (state == GLUT_DOWN):
                mouseClicked = True
               
                if (len(PontosClicados) == 2):
                    bloqueiaSubida = True
           
                if (primeiraExecucaoModo1 == True):
                    PontosClicados.append(ConvertePonto(Ponto(x, y)))
                    PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
                    Linha.append(ConvertePonto(Ponto(x, y)))
                else:
                    if(len(PontosClicados) == 2):
                        PontosClicados.append(ConvertePonto(Ponto(x, y)))
                        PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]

            if (state == GLUT_UP):
                mouseClicked = False
                if (bloqueiaSubida == False):
                    PontosClicados.append(ConvertePonto(Ponto(x, y)))
                    Linha.append(ConvertePonto(Ponto(x, y)))
                    nPontoAtual += 1
                    PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
                   
                bloqueiaSubida = False
       
        if (arrastaCurva == True):
            arrastaCurva = False

        if len(PontosClicados) == 3:
            CriaCurvas()
            curvaCriada = True
            primeiraExecucaoModo1 = False
           

        if (state == GLUT_DOWN and len(PontosClicados) == 2):
            return
        if (button == GLUT_RIGHT_BUTTON):
            return   

        print("Pontos =", len(PontosClicados))

    # PontoConvertido = ConvertePonto(Ponto(x, y))
    # print(f"Mouse clicado na janela: ({x}, {y})")
    # print(f"Mouse clicado no mundo: ({PontoConvertido.x}, {PontoConvertido.y})")

    glutPostRedisplay()

# **********************************************************************
# Captura as coordenadas do mouse do mouse sobre a area de
# desenho, enquanto um dos botoes esta sendo pressionado
# **********************************************************************


def Motion(x: int, y: int):
    global PosAtualDoMouse
    global arrastaCurva
    global pontoMovendo
    global pontosAntecedentes

    P = Ponto(x, y)
    PosAtualDoMouse = ConvertePonto(P)

    if(movendoPonto == True):
        pontoMovendo.set(PosAtualDoMouse.GetX(), PosAtualDoMouse.GetY())
    elif(movendoPontoDerivada == True):
        pontoMovendo.set(PosAtualDoMouse.GetX(), PosAtualDoMouse.GetY())
        if(casoPontoDerivada == 2):
            count = 1
            for ponto in PontosDerivadas:
                if(count%2 != 0 and count < len(PontosDerivadas)-1):
                    vetAux = PontosDerivadas[count].__sub__(ponto)
                    novoPonto = PontosDerivadas[count].__add__(vetAux)
                    PontosDerivadas[1+count].set(novoPonto.GetX(), novoPonto.GetY())
                count = count + 1
                if(count == len(PontosDerivadas)-1):
                    break
        else:
            aux = pontosAntecedentes
            while(aux > 2):
                if(aux%2 != 0):
                    vetAux = PontosDerivadas[aux].__sub__(PontosDerivadas[aux-1])
                    novoPonto = PontosDerivadas[aux-1].__sub__(vetAux)
                    PontosDerivadas[aux-2].set(novoPonto.GetX(), novoPonto.GetY())
                aux = aux -1
            aux2 = pontosAntecedentes
            while(aux2 < len(PontosDerivadas)-2):
                if(aux2%2 !=0):
                    print("AUX: ", aux2)
                    vetAux = PontosDerivadas[aux2+1].__sub__(PontosDerivadas[aux2])
                    novoPonto = PontosDerivadas[aux2+1].__add__(vetAux)
                    PontosDerivadas[aux2+2].set(novoPonto.GetX(), novoPonto.GetY())
                aux2 = aux2 + 1
                if(aux2 == len(PontosDerivadas)-2):
                    break
    else:
        if (len(PontosClicados) == 3 and curvaCriada == True):
            arrastaCurva = True
            PontosClicados[2] = PosAtualDoMouse
            CriaCurvas()
    # PosAtualDoMouse.imprime("Mouse:")
    # print('')

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************


print("Programa OpenGL")
print("Mode =", mode)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH | GLUT_RGB)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(1400, 700)
glutInitWindowPosition(100, 100)

# Cria a janela na tela, definindo o nome da
# que aparecera na barra de título da janela
wind = glutCreateWindow("Animacao com Bezier")

# executa algumas inicializações
init()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# sera chamada automaticamente quando
# for necessario redesenhar a janela
glutDisplayFunc(display)

# Define que o tratador de evento para
# o invalidacao da tela. A funcao "display"
# sera chamada automaticamente sempre que a
# maquina estiver ociosa (idle)
glutIdleFunc(animate)

# Define que o tratador de evento para
# o redimensionamento da janela. A funcao "reshape"
# sera chamada automaticamente quando
# o usuario alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# sera chamada automaticamente sempre
# o usuario pressionar uma tecla comum
glutKeyboardFunc(keyboard)

# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" será chamada
# automaticamente sempre o usuário
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)
glutMouseFunc(mouse)
glutMotionFunc(Motion)

try:
    glutMainLoop()
except SystemExit:
    pass