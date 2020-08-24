from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color  
from kivy.graphics.vertex_instructions import Rectangle

from kivy.logger import Logger

import kivy.metrics

import random


class BigViewport(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        
        # the below is handled by kwargs
        #self.size_hint = (None, None) #it would be nice if this could be optionally passed in with kwargs
        #self.size = (width, height)

        self.draw()
        self.bind(pos = self.update_rectangles, size = self.update_rectangles)
        

    def draw(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rectangle = Rectangle(pos = self.pos, size = self.size)

    def update_rectangles(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size