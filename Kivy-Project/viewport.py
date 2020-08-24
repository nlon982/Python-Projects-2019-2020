from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color  
from kivy.graphics.vertex_instructions import Rectangle

from kivy.logger import Logger

import kivy.metrics

import random

def get_random():
    return 0.5 + (random.randrange(0, 101) * 0.01) # randrange's stop is exclusive (go figure, all ranges tend to be)
    # this returns 0.4 to 0.6 at 0.1 increments?

class Viewport(BoxLayout):
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
            Color(get_random(), get_random(), get_random(), 1)
            self.rectangle = Rectangle(pos = self.pos, size = self.size)

    def update_rectangles(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size