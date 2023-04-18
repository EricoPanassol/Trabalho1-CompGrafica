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
from Menu import *
# ***********************************************************************************
# Curves Menu
menu = Menu()

# Modelos de Objetos
MeiaSeta = Polygon()
Mastro = Polygon()

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# lista de instancias do Personagens
#Personagens = [] 

# ***********************************************************************************
# Lista de curvas Bezier
#Curvas = []

# Variaveis de controle da curva Bezier
Curvas = []
PontosClicados = []
PoligonoDeControle = None

PosAtualDoMouse = Ponto()
VerdadeiraPosMouse = Ponto()
PontoClicado = Ponto()
nPontoAtual = 0
mouseClicked = False
traca_pol_controle = True

Linha = []

#**********************************************************************
# Lista de mensagens
#**********************************************************************
Mensagens = [
    "  Clique o primeiro ponto.",
    "  Clique o segundo ponto.",
    "  Clique o terceiro ponto."
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
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c))


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
    PrintString(Mensagens[len(PontosClicados)], -15, -14, White)

    # if nPontoAtual > 0:
    #     PrintString("Ultimo ponto clicado: ", -14, 11, Red)
    #     ImprimePonto(PontosClicados[nPontoAtual-1], -14, 9, Red)
    PrintString(f"Mouse pos: {PosAtualDoMouse.to_string()}", -3, -14, White)
    #ImprimePonto(PosAtualDoMouse, -1, -14, White)
    
    PrintString(f"Mouse: {'Down' if  mouseClicked else 'Up'}", 11, -14, White)
    #PrintString("Down", 13, -14, White) if mouseClicked else PrintString("Up", 13, -14, White)

    PrintString(f"{len(Curvas)} Curvas", 7, -14, White)
    

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
    glVertex2f(Meio.x,Min.y+2)
    glVertex2f(Meio.x,Max.y-1)
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

    setup_menu_options()

# ***********************************************************************************
def DesenhaLinha (P1: Ponto, P2: Ponto):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ***********************************************************************************
def DesenhaCurvas():
    global traca_pol_controle
    
    for I in Curvas:
        defineCor(Aquamarine)
        I.Traca()
        defineCor(IndianRed)
        if(traca_pol_controle):
            I.TracaPoligonoDeControle()
            defineCor(BlueViolet)
            glPointSize(7)
            glBegin(GL_POINTS)
            for curva in Curvas:
                for ponto in curva.Coords:
                    glVertex2f(ponto.x, ponto.y)
            glEnd()
            glPointSize(1)

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
    glTranslated(11,13,0) # veja o arquivo MeiaSeta.txt
    MeiaSeta.desenhaPoligono()
    glPopMatrix()

# ***********************************************************************************

def removeCurve(button: int, state: int, x: int, y: int):
    if(len(Curvas) > 0):
        curvas = Curvas.copy()
        for curva in curvas:
            pontos = curva.getPontos()
            p0 = [pontos[0].x, pontos[0].y]
            p1 = [pontos[1].x, pontos[1].y]
            p2 = [pontos[2].x, pontos[2].y]

            if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
                point = ConvertePonto(Ponto(x, y))
                aresta0 = [p0, p1]   
                aresta1 = [p1, p2]
                aresta2 = [p0, p2]         

                canRemove = point_on_edge(point, aresta0) or point_on_edge(point, aresta1) or point_on_edge(point, aresta2)
                
                if canRemove and traca_pol_controle:
                    Curvas.remove(curva)
                    print("Curva removida")

# ***********************************************************************************
    
def point_on_edge(point, edge):
    TOLERANCE = 0.1
    
    # delimita os pontos para a aresta
    min_x = min(edge[0][0], edge[1][0])
    max_x = max(edge[0][0], edge[1][0])
    min_y = min(edge[0][1], edge[1][1])
    max_y = max(edge[0][1], edge[1][1])
    if point.x < min_x or point.x > max_x or point.y < min_y or point.y > max_y:
        return False
    
    # calcula a distância do ponto à reta que contém a aresta
    d0 = distance_point_to_line(point, edge)

    # calcula a distância do ponto aos extremos da aresta
    d1 = distance_point_to_line(point, [edge[0], [point.x, point.y]])
    d2 = distance_point_to_line(point, [edge[1], [point.x, point.y]])

    # verifica se o ponto está próximo o suficiente da aresta para considerá-lo como um clique na aresta
    if d0 < TOLERANCE and min(d1, d2) < math.dist(edge[0], edge[1]):
        return True
    else:
        return False
   
    
# ***********************************************************************************

def distance_point_to_line(point, aresta):    
    x0 = point.x
    y0 = point.y
    
    x1 = aresta[0][0]
    y1 = aresta[0][1]
    
    x2 = aresta[1][0]
    y2 = aresta[1][1]
    
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    if((A,B) == (0,0)):
        return 0
    
    d = abs(A * x0 + B * y0 + C) / math.sqrt(A**2 + B**2)
    return d

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

    #DesenhaMenu()
    DesenhaEixos()
    menu.desenha()
    
    glLineWidth(2)
    defineCor(White)
    desenha_rubberband()
    
    if(len(PontosClicados) == 2 and mouseClicked):
        temp_curve = Bezier(PontosClicados[0], PontosClicados[1], PosAtualDoMouse)
        defineCor(Aquamarine)
        temp_curve.Traca()
        defineCor(IndianRed)
        temp_curve.TracaPoligonoDeControle()
        #defineCor(IndianRed)
        
    # if(len(Linha) > 1):
    #     DesenhaLinha(Linha[0], Linha[1])

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

def desenha_rubberband():
    num_pontos_clicados = len(PontosClicados)
    if(num_pontos_clicados > 0):
        DesenhaLinha(PontosClicados[num_pontos_clicados-1], PosAtualDoMouse)

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
    global PontosClicados
    global PosAtualDoMouse
    global VerdadeiraPosMouse
    global mouseClicked
    global Linha
    
    # Se for o botão direito deixa criar curvas clicando em 3 pontos
    # se for o botão esquerdo ele cria a curva de bezier a partir do rubberbanding

    PontoClicado = ConvertePonto(Ponto(x,y))

    print(f"PontoClicado.x : {PontoClicado.x}")

    if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        mouseClicked = True
        if(VerdadeiraPosMouse.y > 14):
            print('called')
            menu.get_option_click(PontoClicado, state)
            
    elif(button == GLUT_RIGHT_BUTTON and state == GLUT_UP):
        mouseClicked = False

    clicked_inside_canvas = PontoClicado.y < 14 and PontoClicado.y >= -13

    if(clicked_inside_canvas):
        
        print("Click no canvas")
        print(f"len PontosClicados: {len(PontosClicados)}")
        
        # SEM CONTINUIDADE          
        if(menu.active_option == 0):
            semContinuidade(button, state, x, y)

        # CONTINUIDADE DE POSICAO          
        if(menu.active_option == 1):
            continuidadeDePosicao(button, state, x, y)
            
        # CONTINUIDADE DE DERIVADA          
        if(menu.active_option == 2):
            continuidadeDeDerivada(button, state, x, y)

        # EDITAR VERTICES
        if(menu.active_option == 3):
            # Editar Vertices
            pass
        
        # REMOVE CURVA
        if(menu.active_option == 4):
            removeCurve(button, state, x, y)

    glutPostRedisplay()

def semContinuidade(button: int, state: int, x: int, y: int):
    global PontoClicado
    global PontosClicados
    global PosAtualDoMouse
    global VerdadeiraPosMouse
    global mouseClicked
    global Linha
    
    if(state == GLUT_DOWN):
        if(len(PontosClicados) == 0):
            print("len == 0")
            PontosClicados.append(PontoClicado)
            PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
            print(f"len PontosClicados: {len(PontosClicados)}")
            
    if(state == GLUT_UP):
        PontosClicados.append(PontoClicado)
        PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]

    if(len(PontosClicados) == 3):
        print("We got a curve, ain't we?")
        CriaCurvas()
        ClearPontosClicados()


def continuidadeDePosicao(button: int, state: int, x: int, y: int):
    global PontoClicado
    global PontosClicados
    global PosAtualDoMouse
    global VerdadeiraPosMouse
    global mouseClicked
    global Linha
    
    if(state == GLUT_DOWN):
        if(len(PontosClicados) == 0):
            print("len == 0")
            PontosClicados.append(PontoClicado)
            PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
            print(f"len PontosClicados: {len(PontosClicados)}")
            
    if(state == GLUT_UP):
        PontosClicados.append(PontoClicado)
        PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]

    if(len(PontosClicados) == 3):
        print("We got a curve, ain't we?")
        checkpoint = PontosClicados[2] #hehe
        CriaCurvas()
        ClearPontosClicados()
        PontosClicados.append(checkpoint)
        PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]


def continuidadeDeDerivada(button: int, state: int, x: int, y: int):
    if(state == GLUT_DOWN):
        if(len(PontosClicados) == 0):
            print("len == 0")
            PontosClicados.append(PontoClicado)
            PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
            print(f"len PontosClicados: {len(PontosClicados)}")
            
    if(state == GLUT_UP):
        PontosClicados.append(PontoClicado)
        PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]

    if(len(PontosClicados) == 3):
        print("We got a curve, ain't we?")
        checkpoint_b = PontosClicados[1]
        checkpoint_c = PontosClicados[2]
        projected_point = checkpoint_c.__add__(checkpoint_c.__sub__(checkpoint_b))
        CriaCurvas()
        ClearPontosClicados()
        PontosClicados.append(checkpoint_c)
        PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
        PontosClicados.append(projected_point)
        PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]


def removeCurve(button: int, state: int, x: int, y: int):
    global PontoClicado
    global PontosClicados
    global PosAtualDoMouse
    global VerdadeiraPosMouse
    global mouseClicked
    global Linha
    
    if(len(Curvas) > 0 and traca_pol_controle):
        curvas = Curvas.copy()
        for curva in curvas:
            pontos = curva.getPontos()
            p0 = [pontos[0].x, pontos[0].y]
            p1 = [pontos[1].x, pontos[1].y]
            p2 = [pontos[2].x, pontos[2].y]

            if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
                point = ConvertePonto(Ponto(x, y))
                aresta0 = [p0, p1]   
                aresta1 = [p1, p2]
                aresta2 = [p0, p2]         

                canRemove = point_on_edge(point, aresta0) or point_on_edge(point, aresta1) or point_on_edge(point, aresta2)

                if canRemove:
                    Curvas.remove(curva)
                    print("Curva removida") 


def setup_menu_options():
        menu.add_option("Sem Continuidade", True, ClearPontosClicados)
        menu.add_option("Cont. de Posição", False, ClearPontosClicados)
        menu.add_option("Cont. de Derivada", False, ClearPontosClicados)
        menu.add_option("Editar Vertices", False, ClearPontosClicados)
        menu.add_option("Remover Curva", False, ClearPontosClicados)
        menu.add_option("Poligono de Controle", True, SwitchPoligonoControle)
        menu.add_option("Limpa Tela", False, LimpaTela)

def ClearPontosClicados():
    PontosClicados.clear()
    print("Pontos Excluidos!")

def LimpaTela():
    print("Limpa telaa")
    Curvas.clear()
    PontosClicados.clear()
    Linha.clear()

def SwitchPoligonoControle():
    global traca_pol_controle
    traca_pol_controle = not traca_pol_controle
    print(f"Poligono de Controle: {traca_pol_controle}")

# **********************************************************************
# Captura as coordenadas do mouse do mouse sobre a area de
# desenho, enquanto um dos botoes esta sendo pressionado
# **********************************************************************
def Motion(x: int, y: int):
    global PosAtualDoMouse
    
    P = Ponto(x, y)
    PosAtualDoMouse = ConvertePonto(P)
    # PosAtualDoMouse.imprime("Mouse:")
    # print('')

def PassiveMotion(x: int, y: int):
    global VerdadeiraPosMouse

    P = Ponto(x,y)
    VerdadeiraPosMouse = ConvertePonto(P)
    # VerdadeiraPosMouse.imprime("Mouse:")
    # print('')

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

print("Programa OpenGL")

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH | GLUT_RGB)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(1200, 700)
# glutInitWindowPosition(100, 100)

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
glutPassiveMotionFunc(PassiveMotion)

try:
    glutMainLoop()
except SystemExit:
    pass
