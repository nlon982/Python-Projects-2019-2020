from mouseover import MouseOver
from constants import *

from kivy.uix.label import Label
from kivy.graphics.context_instructions import Color  
from kivy.graphics.vertex_instructions import Rectangle


class MenuBar(Label, MouseOver):
    def __init__(self, name, text_color, main_color, accent_color):
        super().__init__()
        self.text = name
        self.color = almost_black
        self.halign = "center"
        self.valign = "center"
        self.font_size = '22dp' #31.9998, re: what it should be accordinging to the website em ratio
        self.size_hint_y = None
        self.height = '68dp'
        
        self.main_color = main_color
        self.accent_color = accent_color

        self.draw()
        self.bind(pos = self.update_rectangles, size = self.update_rectangles) #kivy tutorial does this so it passes the object that the size changed, I think this is unnecessary
        self.bind(width = self.update_textbox) # not necessary if using center anyway

    def draw(self):
        self.canvas.before.clear() # bug prevention. Preferably this would only do if not calling in init, which saves exactly one call, and isn't worth it.
        with self.canvas.before:
            Color(*self.main_color)
            self.main_rectangle = Rectangle(pos = self.pos, size = self.size)

            Color(*self.accent_color)
            self.accent_rectangle = Rectangle(pos = self.pos, size = (self.size[0], 8)) # draws on top

            #Color(1, 1, 1, 1)
            #self.line_rectangle = Rectangle(pos = self.pos, size = (self.size[0], 1))
            

    def update_rectangles(self, *args):
        self.main_rectangle.pos = self.pos
        self.main_rectangle.size = self.size
        
        self.accent_rectangle.pos = self.pos
        self.accent_rectangle.size = (self.size[0], 8)

        #self.line_rectangle.pos = self.pos
        #self.line_rectangle.size = (self.size[0], 1)

    def update_textbox(self, *args):
        self.text_size = [self.parent.width, self.height]

    def on_hover(self):
        pass

    def on_exit(self):
        pass



class BottomBar(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw()
        self.bind(pos = self.update_rectangle, size = self.update_rectangle)
        self.bind(width = self.update_textbox)
        self.text = "None selected"
        self.halign = "left"
        self.valign = "center"
        self.padding_x = 5
        self.color = orange

        


    def draw(self, *args):
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rectangle = Rectangle(pos = self.pos, size = self.size)


    def update_rectangle(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size


    def update_textbox(self, *args):
        self.text_size = [self.parent.width, self.height]

    def update_text(self, text):
        self.text = text