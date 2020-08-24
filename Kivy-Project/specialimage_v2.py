from mouseover import MouseOver
from constants import *


from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics.context_instructions import Color  
from kivy.graphics.vertex_instructions import Rectangle
from kivy.core.window import Window

import kivy.metrics

class SpecialImage(AnchorLayout, ButtonBehavior, MouseOver):
    def __init__(self, direntry, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.width = 100
        self.height = 50

        self.add_widget(Label(text = "Special Image"))

        self.draw_main()
        self.bind(pos = self.draw_main, size = self.draw_main) # make draw main take background colour


    def draw_main(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 0, 0, 1)
            self.rectangle = Rectangle(pos = self.pos, size = self.size)

    def update_rectangles(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size

    def on_hover(self):
        pass

    def on_exit(self):
        pass

    def on_press(self):
        pass