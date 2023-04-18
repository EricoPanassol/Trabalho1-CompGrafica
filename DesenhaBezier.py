# ***********************************************************************************
#   ExibePoligonos.py
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
from Poligonos import *
from InstanciaBZ import *
from Bezier import *
from ListaDeCoresRGB import *
import numpy as np
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

PosAtualDoMouse = Ponto()
nPontoAtual = 0
mouseClicked = False
arrastaCurva = False
bloqueiaSubida = False

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
firstCurve = True
aux = True

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
    PrintString(Mensagens[len(PontosClicados)-1], -14, 13, White)
    
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
    C = Bezier(PontosClicados[0], PontosClicados[1], PontosClicados[2])
    if (arrastaCurva == True):
        Curvas[len(Curvas)-1] = C
    else:
        Curvas.append(C)


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

    aux = PontosClicados
    for Ponto in aux:
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
    global desenhaPoligonoControle, mode, firstCurve
    
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        Curvas.clear()

    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        desenhaPoligonoControle = not desenhaPoligonoControle
        
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        if(mode <= 0):
            mode = 0
            clearScreen()
        else:
            firstCurve = True
            mode -= 1
            clearScreen()
        
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        if(mode >= 2):
            mode = 2
            clearScreen()
        else:
            firstCurve = True
            mode += 1
            clearScreen()
            
    print("mode =", mode)

    glutPostRedisplay()


def clearScreen():
    PontosClicados.clear()
    LinhaDerviada.clear()
    Linha.clear()

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
    # if(len(Curvas) > 0):
    #     curva = Curvas[0].getPontos()
                
                
    #     # cria os x e y dos pontos da curva
    #     pontosDaCurva = []
    #     p0 = [curva[0].x, curva[0].y]
    #     p1 = [curva[1].x, curva[1].y]
    #     p2 = [curva[2].x, curva[2].y]
        
        
    #     # cria os pontos da curva
    #     ponto0 = ConvertePonto(Ponto(p0[0], p0[1]))
    #     ponto1 = ConvertePonto(Ponto(p1[0], p0[1]))
    #     ponto2 = ConvertePonto(Ponto(p2[0], p0[1]))
    #     print("ponto0 =", ponto0)
                
                
    #     # adiciona os pontos da curva na lista
    #     pontosDaCurva.append(ponto0)
    #     pontosDaCurva.append(ponto1)
    #     pontosDaCurva.append(ponto2)
        
        
    #     # calcula a diff entre os pontos da curva para pegar as arestas
    #     arestasDaCurva = []
    #     a0 = ponto1.__sub__(ponto0)
    #     a1 = ponto2.__sub__(ponto1)
    #     a2 = ponto2.__sub__(ponto0)
                
        
    #     # adiciona essa diff na lista
    #     arestasDaCurva.append(a0)
    #     arestasDaCurva.append(a1)
    #     arestasDaCurva.append(a2)
    
    
    
    # on mouse move() -> verifica se a pos do mouse está perto de qualquer vértice do pol de controle e o mouse está down
    # arrasta o vertice
    # cuidar para nao arrastar o vértica de uma outra curva enquanto estiver arrastando alguma ja
        

    if (mode == 0):
       semContinuidade(button, state, x, y)


    elif (mode == 1):
        continuidadePosicao(button, state, x, y)

    
    elif(mode == 2):
        continuidadeDerivada(button, state, x, y)

    glutPostRedisplay()


# **********************************************************************
# Modos de criação de curva
# 
# **********************************************************************


def semContinuidade(button: int, state: int, x: int, y: int):
    global PontosClicados, PosAtualDoMouse, mouseClicked, nPontoAtual, curvaCriada, arrastaCurva, bloqueiaSubida, Linha, mode, pontoAuxiliar, firstCurve, pontoAuxiliar2, aux
    
    curvaCriada = False
    
    if (arrastaCurva == True or len(PontosClicados) == 3):
        PontosClicados.clear()

    if (button == GLUT_LEFT_BUTTON):
        if (state == GLUT_DOWN):
            mouseClicked = True
            if (len(PontosClicados) == 2):
                bloqueiaSubida = True
            PontosClicados.append(ConvertePonto(Ponto(x, y)))
            Linha.append(ConvertePonto(Ponto(x, y)))
            PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]

        if (state == GLUT_UP):
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


def continuidadePosicao(button: int, state: int, x: int, y: int):
    global PontosClicados, PosAtualDoMouse, mouseClicked, nPontoAtual, curvaCriada, arrastaCurva, bloqueiaSubida, Linha, mode, pontoAuxiliar, firstCurve, pontoAuxiliar2, aux
    
    curvaCriada = False
    
    if (arrastaCurva == True or nPontoAtual == 3):
            pontoAuxiliar = PontosClicados[2]        
            PontosClicados.clear()
            PontosClicados.append(pontoAuxiliar)
            nPontoAtual = 1
            Linha.clear()
            Linha.append(pontoAuxiliar)

    if (button == GLUT_LEFT_BUTTON):
        if (state == GLUT_DOWN):
            mouseClicked = True
            
            if (len(PontosClicados) == 2):
                bloqueiaSubida = True
            
            if (firstCurve == True): 
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
        
        firstCurve = False
    
    if (state == GLUT_DOWN and len(PontosClicados) == 2):
        return
    if (button == GLUT_RIGHT_BUTTON):
        return    


def continuidadeDerivada(button: int, state: int, x: int, y: int):
    global PontosClicados, PosAtualDoMouse, mouseClicked, nPontoAtual, curvaCriada, arrastaCurva, bloqueiaSubida, Linha, mode, pontoAuxiliar, firstCurve, pontoAuxiliar2, aux
    
    curvaCriada = False
    
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
        # vetBC.imprime("Dist entre LD[0] - LD[1], vetBC =")
        
        d = LinhaDerviada[0].__add__(vetBC)
        # d.imprime("Ponto D =")
        
        PontosClicados.clear()
        PontosClicados.append(pontoAuxiliar)
        PontosClicados.append(d)
        
        Linha.clear()
        LinhaDerviada.clear()
        Linha.append(pontoAuxiliar)
        
        nPontoAtual = 2        
        
    if (button == GLUT_LEFT_BUTTON):
        if (state == GLUT_DOWN):
            mouseClicked = True
            
            if (len(PontosClicados) == 2):
                bloqueiaSubida = True
        
            if (firstCurve == True): 
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
        firstCurve = False
        
    if (state == GLUT_DOWN and len(PontosClicados) == 2):
        return
    if (button == GLUT_RIGHT_BUTTON):
        return    


# **********************************************************************
# Captura as coordenadas do mouse do mouse sobre a area de
# desenho, enquanto um dos botoes esta sendo pressionado
# **********************************************************************


def Motion(x: int, y: int):
    global PosAtualDoMouse
    global arrastaCurva

    P = Ponto(x, y)
    PosAtualDoMouse = ConvertePonto(P)

    if (len(PontosClicados) == 3 and curvaCriada == True):
        arrastaCurva = True
        PontosClicados[2] = PosAtualDoMouse
        CriaCurvas()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************


print("Programa OpenGL")

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
