from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ListaDeCoresRGB import *
from Poligonos import *
import time

class Menu:
    

    def __init__(self):
        self.options = []
        
        
    def add_option(self, option, is_active):
        self.options.append({
            "option" : option,
            "is_active" : is_active
        })

    def setup_menu_options(self):
        self.add_option("Sem Continuidade", True)
        self.add_option("Cont de Posição", False)
        self.add_option("Cont de Derivada", False)
        self.add_option("Editar Vertices", False)
        self.add_option("Remover Vertices", False)
        self.add_option("Poligono de Controle", False)
        self.add_option("Limpa Tela", False)

    def draw(self):
        option_box = Polygon()
        option_box.LePontosDeArquivo("OptionBox.txt")

        glPushMatrix()

        menu_bar = Polygon()
        menu_bar.LePontosDeArquivo("MenuBar.txt")
        defineCor(White)
        menu_bar.desenhaRetangulo()

        for n in range(len(self.options)):
            background_color = White
            font_color = Black
            if (self.options[n]["is_active"]):
                background_color = Black
                font_color = White
            if(n > 0):
                glTranslated(4.28, 0, 0)
            defineCor(background_color)
            option_box.desenhaRetangulo()
            self.print_string(self.options[n].get("option"), -14.3, 14.3, font_color)
            defineCor(White)
        
        glPopMatrix()
    
    def print_string(self, S: str, x: int, y: int, cor: tuple):
        defineCor(cor)
        glRasterPos3f(x, y, 0) # define posicao na tela

        for c in S:
            # GLUT_BITMAP_HELVETICA_10
            # GLUT_BITMAP_TIMES_ROMAN_24
            # GLUT_BITMAP_HELVETICA_18
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c))

    def get_option_click(self, ponto: Ponto, state: int):
        if(ponto.y < 14):
            return

        option_index = int(7*(ponto.x + 15) / 30)

        option = self.options[option_index]
       
        if(state == GLUT_DOWN):
            if(option_index < 3):
                for i in range(3):
                    self.options[i]["is_active"] = False

                self.options[option_index]["is_active"] = True
                return
                
            
            if(option_index < 5):
                if(option["is_active"]):
                    option["is_active"] = not option["is_active"]
                    return
                else:
                    for i in range(3,5):
                        self.options[i]["is_active"] = False

                    option["is_active"] = True
                    return
            
            if(option_index == 5):
                option["is_active"] = not option["is_active"]
                return
            
            if(option_index == 6):
                option["is_active"] = True

                
                

    def reset(self):
        for option in self.options:
                option["is_active"] = False
