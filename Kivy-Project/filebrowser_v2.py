import os
import math
import statistics

#from specialimage import SpecialImage
from specialimage_v2 import SpecialImage
from menu_and_bottom_bar import MenuBar, BottomBar
from constants import *

from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.graphics.context_instructions import Color  
from kivy.graphics.vertex_instructions import Rectangle

from kivy.uix.button import Button

from kivy.logger import Logger

import kivy.metrics

class FileBrowser(BoxLayout):
    def __init__(self, name):
        super().__init__()
        self.orientation = "vertical"
        self.size_hint = (1, 1)

        self.scroll_body = ScrollView()
        self.add_widget(self.scroll_body)

        self.body = StackLayout(orientation = "lr-tb", size_hint_y = None)
        self.scroll_body.add_widget(self.body)
        ##Settings##
        self.body.bind(minimum_height = self.body.setter('height'))

        self.draw()
        self.bind(pos = self.update_rectangles, size = self.update_rectangles)


        self.populate("placeholderforsource")


    def draw(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.8, 1, 1, 1)
            self.rectangle = Rectangle(pos = self.pos, size = self.size)


    def update_rectangles(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size

    def populate(self, source): # a means of setting source
        for i in range(0, 10):
            self.body.add_widget(SpecialImage("placeholderfordirentry"))
