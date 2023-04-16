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

PosAtualDoMouse = Ponto()
nPontoAtual = 0
mouseClicked = False
arrastaCurva = False
bloqueiaSubida = False

#**********************************************************************
# Lista de mensagens
#**********************************************************************
Mensagens = [
    "Clique o primeiro ponto.",
    "Clique o segundo ponto.",
    "Clique o terceiro ponto."
]

MouseState = [
    "Mouse down",
    "Mouse up"
]

angulo = 0.0
desenha = True


# **********************************************************************
# Imprime o texto S na posicao (x,y), com a cor 'cor'
# **********************************************************************
def PrintString(S: str, x: int, y: int, cor: tuple):
    defineCor(cor) 
    glRasterPos3f(x, y, 0) # define posicao na tela
    
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
    PrintString(Mensagens[nPontoAtual], -14, 13, White)

    if nPontoAtual > 0:
        PrintString("Ultimo ponto clicado: ", -14, 11, Red)
        ImprimePonto(PontosClicados[nPontoAtual-1], -14, 9, Red)
    
    PrintString("Mouse pos: ", 5, 11, White)
    ImprimePonto(PosAtualDoMouse, 5, 9, White)
    
    
    PrintString("Mouse: ", 5, 13, White)
    PrintString("Up", 10, 13, White) if mouseClicked else PrintString("Down", 10, 13, White)
    


# **********************************************************************
def animate():
    glutPostRedisplay()
     

# ***********************************************************************************
def reshape(w,h):
    global Min, Max

    # Reseta sistema de coordenadas antes de modifica-lo
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Define a area a ser ocupada pela area OpenGL dentro da Janela
    glViewport(0, 0, w, h)
    
    # Define os limites logicos da area OpenGL dentro da Janela
    glOrtho(Min.x, Max.x, Min.y, Max.y, -10, 10)

    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# **************************************************************
def DesenhaEixos():
    global Min, Max

    Meio = Ponto(); 
    Meio.x = (Max.x+Min.x)/2
    Meio.y = (Max.y+Min.y)/2
    Meio.z = (Max.z+Min.z)/2

    glBegin(GL_LINES)
    #  eixo horizontal
    glVertex2f(Min.x,Meio.y)
    glVertex2f(Max.x,Meio.y)
    #  eixo vertical
    glVertex2f(Meio.x,Min.y)
    glVertex2f(Meio.x,Max.y)
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
    if(arrastaCurva == True):
        Curvas[len(Curvas)-1] = C
    else:
        Curvas.append(C)


# ***********************************************************************************
def init():
    global Min, Max
    # Define a cor do fundo da tela (PRETO)
    glClearColor(0,0,0,0)

    CarregaModelos()

    d:float = 15
    Min = Ponto(-d,-d)
    Max = Ponto(d,d)

# ***********************************************************************************
def DesenhaLinha (P1: Ponto, P2: Ponto):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ***********************************************************************************
def DesenhaCurvas():
    for I in Curvas:
        defineCor(Yellow)
        I.Traca()
        defineCor(Brown)
        I.TracaPoligonoDeControle()

# **********************************************************************
def DesenhaPontos():
    defineCor(Red)
    glPointSize(4)
    glBegin(GL_POINTS)

    for Ponto in PontosClicados:
        glVertex2f(Ponto.x, Ponto.y)
    glEnd()
    glPointSize(1)

# **********************************************************************
def DesenhaMenu():
    glPushMatrix()
    glTranslated(11,13,0) # veja o arquivo MeiaSeta.txt
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

    if(nPontoAtual):
        DesenhaLinha(PontosClicados[nPontoAtual-1], PosAtualDoMouse)

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
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        glutFullScreen()
        
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        glutPositionWindow(50, 50)
        glutReshapeWindow(700, 500)
        
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        pass
        
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        pass

    glutPostRedisplay()

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
    
    curvaCriada = False;
    
    print(PontosClicados)
    
    if(arrastaCurva == True or len(PontosClicados) == 3):
        PontosClicados.clear()
    
    if(button == GLUT_RIGHT_BUTTON):
        if(state == GLUT_DOWN):
            print("Mouse down")
            mouseClicked = True;
            
        if((state == GLUT_UP and len(PontosClicados) != 3) or (state == GLUT_DOWN and len(PontosClicados) == 2)):
            print("Mouse up")

            if(not(state == GLUT_UP and bloqueiaSubida == True)):
                PontosClicados.append(ConvertePonto(Ponto(x, y)))
                PosAtualDoMouse = PontosClicados[len(PontosClicados)-1];
            
            if(state == GLUT_UP):
                mouseClicked = False
                bloqueiaSubida = False
            else:
                bloqueiaSubida = True
            # nPontoAtual += 1
            # print(f"Pontos clicados: {nPontoAtual}")
            
            # PosAtualDoMouse = PontosClicados[nPontoAtual-1]

    if(button == GLUT_LEFT_BUTTON):
        if(state == GLUT_DOWN):
            print("Mouse down")
            mouseClicked = True;
            if(len(PontosClicados) == 2):
                bloqueiaSubida = True
            PontosClicados.append(ConvertePonto(Ponto(x, y)))
            PosAtualDoMouse = PontosClicados[len(PontosClicados)-1];
            
        if(state == GLUT_UP):
            print("Mouse up")
            mouseClicked = False;
                   
            if(bloqueiaSubida == False):
                PontosClicados.append(ConvertePonto(Ponto(x, y)))
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
        
    if(state == GLUT_DOWN and len(PontosClicados) == 2):
        return
    if(button == GLUT_RIGHT_BUTTON):
        return

    PontoConvertido = ConvertePonto(Ponto(x, y))

    print(f"Mouse clicado na janela: ({x}, {y})")
    print(f"Mouse clicado no mundo: ({PontoConvertido.x}, {PontoConvertido.y})")

    glutPostRedisplay()

# **********************************************************************
# Captura as coordenadas do mouse do mouse sobre a area de
# desenho, enquanto um dos botoes esta sendo pressionado
# **********************************************************************
def Motion(x: int, y: int):
    global PosAtualDoMouse
    global arrastaCurva
    
    P = Ponto(x, y)
    PosAtualDoMouse = ConvertePonto(P)
    
    if(len(PontosClicados) == 3 and curvaCriada == True):
        arrastaCurva = True;
        PontosClicados[2] = PosAtualDoMouse;
        CriaCurvas();
    PosAtualDoMouse.imprime("Mouse:")
    print('')

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

print("Programa OpenGL")

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH | GLUT_RGB)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(500, 500)
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
