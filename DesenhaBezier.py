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
# CurvasAux = []
# CurvasSemContinuidade = []
# CurvasDerivadas = []
# CurvasPosicao = []
PontosClicados = []
PoligonoDeControle = None

PosAtualDoMouse = Ponto()
VerdadeiraPosMouse = Ponto()
PontoClicado = Ponto()
nPontoAtual = 0
mouseClicked = False
traca_pol_controle = True
moving_vertex = None
editing = False
isDrawing = False
isConecting = False

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
idCurva = 0
# lastState = ""

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
    # if nPontoAtual > 0:
    #     PrintString("Ultimo ponto clicado: ", -14, 11, Red)
    #     ImprimePonto(PontosClicados[nPontoAtual-1], -14, 9, Red)
    PrintString(f"Mouse pos: {PosAtualDoMouse.to_string()}", -3, -14, White)
    #ImprimePonto(PosAtualDoMouse, -1, -14, White)
    
    PrintString(f"Mouse: {'Down' if  mouseClicked else 'Up'}", 11, -14, White)
    #PrintString("Down", 13, -14, White) if mouseClicked else PrintString("Up", 13, -14, White)

    PrintString(f"{len(Curvas)} Curvas", 7, -14, White)

    if(menu.active_option < 3):
        PrintString(Mensagens[len(PontosClicados)], -15, -14, White)
    elif(menu.active_option == 3):
        PrintString("Editando vértices", -14, -14, White)
    elif(menu.active_option == 4):
        PrintString("Removendo curvas", -14, -14, White)
    

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
def CriaCurvas(tipo, id_curva, ponto_projetado = None, derivadaDe = None):
    global Curvas 
    # global idCurva

    C = Bezier(PontosClicados[0], PontosClicados[1], PontosClicados[2])
    C.Tipo = tipo
    C.ponto_projetado = ponto_projetado
    C.derivadaDe = derivadaDe
    C.idCurva = id_curva
    Curvas.append(C)
    # CurvasAux.append(C)

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
                    # print("Curva removida")

# ***********************************************************************************
def point_on_edge(point, edge):
    TOLERANCE = 0.1
    
    # verifica se o ponto está dentro do retângulo delimitado pelos pontos da aresta
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

#  retorna o vertex clicado
def whichClickedVertex(vertex, posMouseClicked):
    v0 = mouse_on_vertex(vertex[0], posMouseClicked)
    v1 = mouse_on_vertex(vertex[1], posMouseClicked)
    
    if(v0):
        return vertex[0]
    elif(v1):
        return vertex[1]
    else:
        return vertex[2]

# retorna se o mouse clicou em um vertex
def mouse_on_vertex(vertex, posMouseClicked, tolerance=0.5):
    if(vertex.x - tolerance < posMouseClicked.x < vertex.x + tolerance):
        if(vertex.y - tolerance < posMouseClicked.y < vertex.y + tolerance):
            return True

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
    
    if(len(PontosClicados) == 2):
        temp_curve = Bezier(PontosClicados[0], PontosClicados[1], PosAtualDoMouse)
        defineCor(Aquamarine)
        temp_curve.Traca()
        defineCor(IndianRed)
        temp_curve.TracaPoligonoDeControle()

    if(isConecting):
        ClearPontosClicados()

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
    
    if a_keys == GLUT_KEY_END:
        done_drawing()

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

def get_vertice_curva():
    for curva in Curvas:
            for coord in curva.Coords:
                if(mouse_on_vertex(coord, VerdadeiraPosMouse)):
                    return {"curva": curva,
                            "ponto": coord}
    
    return None
    
# ***********************************************************************************
# Captura o clique do botao esquerdo do mouse sobre a area de desenho
# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    global PontosClicados
    global PosAtualDoMouse
    global VerdadeiraPosMouse
    global mouseClicked
    global isDrawing
    global idCurva
    global isConecting

    PontoClicado = ConvertePonto(Ponto(x,y))

    if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        mouseClicked = True
        if(VerdadeiraPosMouse.y > 14 and VerdadeiraPosMouse.x < 12):
            last_active_option = str(menu.active_option)
            menu.get_option_click(PontoClicado, state)
            new_active_option = str(menu.active_option)
            
            if(last_active_option != new_active_option and len(Curvas) > 0):
                done_drawing()
            
    elif(button == GLUT_LEFT_BUTTON and state == GLUT_UP):
        mouseClicked = False

    clicked_inside_canvas = PontoClicado.y < 14 and PontoClicado.y >= -13

    if(clicked_inside_canvas):
        isDrawing = True
        
        # *********************************************************************
        # OPÇÃO MENU = CURVA SEM CONTINUIDADE
        # *********************************************************************
        if(menu.active_option == 0):
            CriaNovaCurva(state,PontoClicado, idCurva,"sem_continuidade")
            
        # *********************************************************************
        # OPÇÃO MENU = CURVA COM CONTINUIDADE DE POSICAO
        # *********************************************************************
        if(menu.active_option == 1):
            CriaNovaCurva(state,PontoClicado, idCurva,"posicao")
                
        # *********************************************************************
        # OPÇÃO MENU = CURVA COM CONTINUIDADE DE DERIVADA
        # *********************************************************************
        if(menu.active_option == 2):
            CriaNovaCurva(state,PontoClicado, idCurva,"derivada")

        # *********************************************************************
        # OPÇÃO MENU = EDITAR CURVA
        # *********************************************************************
        if(menu.active_option == 3):
            editaCurva(button, state, x, y)

        # *********************************************************************
        # OPÇÃO MENU = CONECTAR CURVAS
        # *********************************************************************
    
        if(traca_pol_controle and isConecting):
            print("conectando")
            compartilhado = False
            if(state == GLUT_DOWN):
                aux_vertex = get_vertice_curva()
                if(aux_vertex != None):
                    print("aux_vertex seleciondado")
                    id_curva_selecionada = aux_vertex["curva"].idCurva
                    for curva in Curvas:
                        if aux_vertex['ponto'] in curva.Coords and aux_vertex["curva"] != curva:
                            print("TA NI OTRA JA")
                            compartilhado = True
                print("onde que eu to")            
                if(not compartilhado):
                    if(menu.active_option == 0):
                        isConecting = False
                        menu.options[6]['is_active'] = False
                        CriaNovaCurva(state, aux_vertex['ponto'], id_curva_selecionada, 'sem_continuidade')

                    elif(menu.active_option == 1):
                        isConecting = False
                        menu.options[6]['is_active'] = False
                        CriaNovaCurva(state, aux_vertex['ponto'], id_curva_selecionada, 'posicao')

                    elif(menu.active_option == 2):
                        print("conectando com derivada")
                        isConecting = False
                        menu.options[6]['is_active'] = False
                        PontosClicados.append(aux_vertex["curva"].Coords[2])
                        PontosClicados.append(aux_vertex["curva"].ponto_projetado)
                        CriaNovaCurva(state, PontoClicado, id_curva_selecionada, 'derivada')

        # *********************************************************************
        # OPÇÃO MENU = ALTERAR TIPO DA CURVA
        # *********************************************************************
        if(menu.active_option == 5):
            if(traca_pol_controle):
                if(state == GLUT_DOWN):
                    aux_vertex = get_vertice_curva()
                    if(aux_vertex != None):
                        print(f"ponto clicado:\nx={aux_vertex['ponto'].x}\ny={aux_vertex['ponto'].y}\nTipo: {aux_vertex['curva'].Tipo}")
                        for i,curva in enumerate(Curvas):
                            if aux_vertex['ponto'] in curva.Coords:
                                if curva.Tipo == "posicao":
                                    curva.Tipo = "derivada"
                                    if curva != aux_vertex["curva"]:
                                        curva.Coords[1] = aux_vertex['curva'].ponto_projetado
                                        curva.derivadaDe = aux_vertex['curva'].Coords[1]

                                elif curva.Tipo == "derivada":
                                    curva.Tipo = "posicao"
                            
        # *********************************************************************
        # OPÇÃO MENU = REMOVER CURVA
        # *********************************************************************
        if(menu.active_option == 4):
           removeCurva(button, state, x, y)      

    glutPostRedisplay()

def editaCurva(button, state, x, y):
    global moving_vertex
    global editing
    global PontoClicado
    global PontosClicados
    global PosAtualDoMouse
    global VerdadeiraPosMouse
    global mouseClicked
    global isDrawing
    
    if(traca_pol_controle):
        if(state == GLUT_DOWN):
            aux_vertex = get_vertice_curva()
            if(aux_vertex != None):
                print(f"Movendo a curva: {aux_vertex['curva'].idCurva}")
                moving_vertex = aux_vertex
                editing = True
        
        if(state == GLUT_UP):
            editing = False
            moving_vertex = None

def removeCurva(button, state, x, y):
    global PontoClicado
    global PontosClicados
    global PosAtualDoMouse
    global VerdadeiraPosMouse
    global mouseClicked
    global isDrawing
    
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

def setup_menu_options():
        menu.add_option("Sem Continuidade", True, ClearPontosClicados)
        menu.add_option("Cont de Posição", False, ClearPontosClicados)
        menu.add_option("Cont de Derivada", False, ClearPontosClicados)
        menu.add_option("Editar Vertices", False, ClearPontosClicados)
        menu.add_option("Remover Curva", False, ClearPontosClicados)
        menu.add_option("Alt Tipo Curva", False, ClearPontosClicados)
        menu.add_option("Conectar Curva", False, SwtichIsConectando)
        menu.add_option("Pol de Controle", True, SwitchPoligonoControle)
        menu.add_option("Limpa Tela", False, LimpaTela)

def ClearPontosClicados():
    global PontosClicados
    PontosClicados.clear()

def LimpaTela():
    Curvas.clear()
    PontosClicados.clear()
    
def SwtichIsConectando():
    global isConecting
    isConecting = not isConecting
    print(isConecting)

def assertCurvesIds():
    for curva in Curvas:
        for curva_i in Curvas:
            for coord in curva_i.Coords:
                if coord in curva.Coords:
                    curva_i.idCurva = curva.idCurva

def CriaNovaCurva(state, PontoClicado, id_curva, tipo):
    global PosAtualDoMouse
    global Curvas
    global PontosClicados
    global idCurva
    global isConecting
    
    if(not isConecting):
        if(state == GLUT_DOWN):
            if(len(PontosClicados) == 0):
                PontosClicados.append(PontoClicado)
                PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
        
        if(state == GLUT_UP):
            PontosClicados.append(PontoClicado)
            PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
        
        if(len(PontosClicados) == 3):
            checkpoint_b = PontosClicados[1]
            checkpoint_c = PontosClicados[2]
            projected_point = projeta_ponto(checkpoint_b, checkpoint_c)
            if(len(Curvas) > 0 and Curvas[-1].Tipo == tipo and idCurva == Curvas[-1].idCurva):
                CriaCurvas(tipo,id_curva, projected_point, Curvas[-1].Coords[1])
            else:
                CriaCurvas(tipo,id_curva, projected_point, None)
            ClearPontosClicados()

            if(menu.active_option == 0):
                idCurva += 1

            if(menu.active_option == 1 or menu.active_option == 2):
                PontosClicados.append(checkpoint_c)
                PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]
                if(menu.active_option == 2):
                    PontosClicados.append(projected_point)
                    PosAtualDoMouse = PontosClicados[len(PontosClicados)-1]

            assertCurvesIds()


def SwitchPoligonoControle():
    global traca_pol_controle
    traca_pol_controle = not traca_pol_controle

def projeta_ponto(checkpoint_b, checkpoint_c):
    return checkpoint_c.__add__(checkpoint_c.__sub__(checkpoint_b))

def done_drawing():
    global idCurva
    global isDrawing

    ClearPontosClicados()
    isDrawing = False
    idCurva += 1
    
def move_curvas_derivadas():
    if(menu.active_option == 3):
        if(editing and (PosAtualDoMouse.y < 13.8 and PosAtualDoMouse.y > -13)):
            moving_vertex["ponto"].x = PosAtualDoMouse.x
            moving_vertex["ponto"].y = PosAtualDoMouse.y
            
            if(moving_vertex["curva"].Tipo == "derivada"):

                idCurvaEditada = moving_vertex["curva"].idCurva

                indice_ponto_atual = Curvas.index(moving_vertex["curva"])
                print(indice_ponto_atual)
                curvas_antes = Curvas[:indice_ponto_atual+1]
                curvas_antes.reverse()
                print(curvas_antes)
                curvas_depois = Curvas[indice_ponto_atual:]
                print(curvas_depois)
                
                for i,curva in enumerate(curvas_antes):

                    if len(curvas_antes) != i + 1:
                        if(curva.Tipo == "derivada" and curvas_antes[i+1].Tipo == "derivada"):
                            if curva.derivadaDe != None and curva.idCurva == idCurvaEditada:
                                ponto_a = curva.Coords[0]
                                ponto_b = curva.Coords[1]
                                ponto_reprojetado_para_tras = projeta_ponto(ponto_b, ponto_a)
                                curva.derivadaDe.x = ponto_reprojetado_para_tras.x
                                curva.derivadaDe.y = ponto_reprojetado_para_tras.y
                            else:
                                break

                for i,curva in enumerate(curvas_depois):
                    if len(curvas_depois) != i + 1:
                        if curva.idCurva == idCurvaEditada and curva.Tipo == "derivada" and curvas_depois[i+1].Tipo == "derivada":
                            ponto_b = curva.Coords[1]
                            ponto_c = curva.Coords[2]
                
                            ponto_reprojetado = projeta_ponto(ponto_b, ponto_c)
                            curva.ponto_projetado.x = ponto_reprojetado.x
                            curva.ponto_projetado.y = ponto_reprojetado.y

# **********************************************************************
# Captura as coordenadas do mouse do mouse sobre a area de
# desenho, enquanto um dos botoes esta sendo pressionado
# **********************************************************************
def Motion(x: int, y: int):
    global PosAtualDoMouse
    
    P = Ponto(x, y)
    PosAtualDoMouse = ConvertePonto(P)
    move_curvas_derivadas()
    
                        
def PassiveMotion(x: int, y: int):
    global VerdadeiraPosMouse

    P = Ponto(x,y)
    VerdadeiraPosMouse = ConvertePonto(P)

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

# print("Programa OpenGL")

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
