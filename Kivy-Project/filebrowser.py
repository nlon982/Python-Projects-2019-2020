import os
import math
import statistics
import time

from specialimage import SpecialImage
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

from kivy.logger import Logger

import kivy.metrics

class FileBrowser(BoxLayout):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        # the below is now handled
        #self.size_hint = (None, None) #it would be nice if this could be optionally passed in with kwargs
        #self.size = (width, height)
        self.source = ""
        self.show_file_names = True
        self.selected_image = SpecialImage(None)
        self.image_width_hint = 1 # big one
        self.bind(size = partial(self.set_image_width_hint)) # will need size or just height, depending on what's being used in the function

        Window.bind(mouse_pos=self._mouse_move)
        self.hover_count = None # set this during populate
        
        

        self.menu_bar = MenuBar(name, almost_black, light_grey, light_blue)
        self.add_widget(self.menu_bar)

        self.scroll_body = ScrollView(bar_width = '12dp', scroll_wheel_distance = '20dp', scroll_type = ['bars', 'content'], bar_inactive_color = [.7, .7, .7, .2]) ### add settings
        self.add_widget(self.scroll_body)
        self.scroll_body.bind(on_scroll_stop = self.on_scroll_stop_function)

        self.body = StackLayout(orientation = "lr-tb", size_hint_x = 0.99, size_hint_y = None, spacing = [1, 5]) # the horizontal spacing isn't like the website, but they didn't have background colours like I do
        self.scroll_body.add_widget(self.body)
        self.body.bind(minimum_height = self.body.setter('height'))
        self.body.bind(height = self.scroll_test_function)

        self.bottom_bar = BottomBar(size_hint = (1, None), height = '17dp', font_size = '13dp', bold = True)
        self.add_widget(self.bottom_bar)

        self.draw()
        self.bind(pos = self.update_rectangles, size = self.update_rectangles)

        self.bind(size = self.test_function)

        self.size = self.size

        self.test_function()

    def scroll_test_function(self, *args):
        self.scroll_body.scroll_wheel_distance = kivy.metrics.dp(20) * math.log(self.body.height) / 4 #< I think I stumbled across a combination here hat's quite effective (it goes between 35-45 depending on number of items, maybe more maybe less)

    def test_function(self, *args):
        self.body.padding = [3, 5, kivy.metrics.dp(12), 0]
        #self.body.padding = [(self.width - (self.width * 0.99)), 5, kivy.metrics.dp(12), 0] #  
        

    def draw(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rectangle = Rectangle(pos = self.pos, size = self.size)

    def update_rectangles(self, *args):
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size

    def populate(self, source): # a means of setting source
        self.source = source
        if self.body.children != []:
            self.body.clear_widgets()

        if source != "":
            direntry_iterator = os.scandir(self.source)
            for direntry in direntry_iterator:
                if direntry.is_file() == True: # Could also check if they are images (.png, .jpg)
                    a_special_image = SpecialImage(direntry)
                    self.body.add_widget(a_special_image)

                    a_special_image.be_within = self
                    a_special_image.be_not_within = self.menu_bar
                    a_special_image.be_not_within_two = self.bottom_bar

                    # set sizes of specialimage. This might be a dumb way to do it, they only need to be called once, you see.
                    a_special_image.update_height() 
                    a_special_image.update_image_height()
                    a_special_image.update_boxlayout()
                    a_special_image.update_text_textboxes()


    def set_selected(self, a_special_image):
        if a_special_image != self.selected_image:

            if self.selected_image != None:
                self.selected_image.selected = False
                self.selected_image.set_deselected()

            self.selected_image = a_special_image
            a_special_image.set_selected()
            self.bottom_bar.update_text(self.selected_image.file_name + " selected")

    def set_image_width_hint(self, *args):
        pass
            

    def _mouse_move(self, *args):
        if not self.get_root_window():
            return
    
        is_collide = self.collide_point(*self.to_widget(*args[1]))

        hovered = False
        for child in self.body.children:
            if child.hover == True and child.selected == False: # since until you on_exit a special image, and it's selected, hover will be true (and we don't want to have a hand cursor)
                hovered = True
                break

        if is_collide == True and hovered == True:
            Window.set_system_cursor("hand")
        elif is_collide == False:
            pass
        else:
            Window.set_system_cursor("arrow")

    def on_scroll_stop_function(self, *args):
        for child in self.body.children: # i.e. when on_scroll_stop is called for scroll_body, iterate through the special images and get them to check if they should be on_hovered or exits (this wouldn't be done otherwise: because a scroll isn't a mouse move)
            child._mouse_move("hifdidl", Window.mouse_pos) # THANK FUCK THAT THIS WORKS. My doubt was that it would pass some bull shit Window.mouse_pos.