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
    background_color = ListProperty([1, 1, 1, 1]) # so I can set this if I want to when instantiating SpecialImage
    file_path = StringProperty("No path")
    file_name = StringProperty("No name")

    def __init__(self, direntry, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = "center"
        self.anchor_y = "center"

        if direntry != None: # should change to isinstance(direntry)
            self.file_path = direntry.path
            self.file_name = direntry.name
            
        self.file_description = "Extra wide Laminate plank"
        self.hover = False
        self.selected = False
        self.size_hint_x = None
        self.width = 82
        self.size_hint_y = None
        self.a_texture = get_texture()

        self.text_color = almost_black

        self.boxlayout = BoxLayout(orientation = "vertical", size_hint = (None, 1))
        self.add_widget(self.boxlayout)
        self.bind(size = self.update_boxlayout)

        ### inside boxlayout start ###
        self.space_0 = Widget(size_hint = (1, None), height = '0dp')
        self.boxlayout.add_widget(self.space_0)

        self.a_image = Image(size_hint = (1, None), source = self.file_path, allow_stretch = True) # do I need a function here that sets height
        self.boxlayout.add_widget(self.a_image)
        self.hover_widget = Widget()
        self.a_image.add_widget(self.hover_widget)
        self.a_image.bind(size = self.update_image_height)

        self.space_1 = Widget(size_hint = (1, None), height = '2dp')
        self.boxlayout.add_widget(self.space_1)
        
        self.title = Label(size_hint = (1, None), height = '27dp', text = self.file_name, halign = "center", valign = "top", color = self.text_color, font_size = '14dp', bold = True) # this could be one pixel lower (i.e. adjust height of this and above). Waiting to see what their text font is like i.e. the d's and l's stick out by one, but (all?) capitals are fine
        self.boxlayout.add_widget(self.title)

        self.space_2 = Widget(size_hint = (1, None), height = '1dp')
        self.boxlayout.add_widget(self.space_2)

        self.description = Label(size_hint = (1, None), height = 0, text = self.file_description, halign = "left", valign = "top", color = self.text_color, font_size = '13dp') # keeping this one pixels, otherwise it doesn't work 
        #self.boxlayout.add_widget(self.description)  

        # IMPORTANT. TO ADD DESCRIPTION BACK, UNCOMMENT THE ABOVE LINE, AND SET HEIGHT OF SELF.DESRCRIPTION TO SOMETHING (I THINK IT WAS 40PIXELS BEFORE)


        #self.space_3 = Widget(size_hint = (1, 1)) # takes up remaining space
        #self.boxlayout.add_widget(self.space_3)

        self.bind(size = self.update_text_textboxes)
        ### inside boxlayout end ##
        
        self.bind(size = self.update_height)

        self.draw_main(self, (1, 1, 1, 1)) # I need to kno how to access background color property and put it here
        self.draw_hover()
        self.bind(pos = self.update_rectangles, size = self.update_rectangles, height = self.update_rectangles)
        
        self.bind(background_color = self.draw_main)

        ### animations start ###
        self.animation_on_hover_image = Animation(opacity = 1, duration = 0.1, transition = "in_out_expo")
        self.animation_on_hover_text = Animation(color = rich_blue, duration = 0.1, transition = "in_out_expo")
        self.animation_on_hover_background = Animation(background_color = (1, 1, 1, 1), duration = 0.1, transition = "in_out_expo")

        self.animation_on_exit_image = Animation(opacity = 0, duration = 0.1, transition = "in_out_expo")
        self.animation_on_exit_text = Animation(color = self.text_color, duration = 0.1, transition = "in_out_expo")
        self.animation_on_exit_background = Animation(background_color = self.background_color, duration = 0.1, transition = "in_out_expo")

        self.animation_selected_image = Animation(background_color = rich_blue, duration = 0.1, transition = "in_out_expo")
        self.animation_deselected_image = Animation(background_color = self.background_color, duration = 0.1, transition = "in_out_expo") # I need to know how to access background color property and put it here
        
        self.animation_test_1 = Animation(color = (1, 1, 1, 1), duration = 0.1, transition = "in_out_expo")
        self.animation_test_2 = Animation(color = (1, 1, 1, 1), duration = 0.1, transition = "in_out_expo")
        self.animation_test_3 = Animation(color = almost_black, duration = 0.1, transition = "in_out_expo")
        ### animations end ###


    def draw_main(self, self_again, background_color): # no idea how to get around this self_again nonsense
        #Logger.critical("triggered")
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*background_color)
            self.rectangle = Rectangle(pos = self.pos, size  = self.size)

    def draw_hover(self):
        with self.hover_widget.canvas.after:
            self.hover_widget.canvas.opacity = 0
            self.hover_rectangle = Rectangle(texture=self.a_texture) # (not setting size and pos, because I can leave that to update_rectangles, which won't have the correct answer til the first hover anyway)

    def update_rectangles(self, *args): # I could merge all these "update" things
        self.rectangle.pos = self.pos
        self.rectangle.size = self.size
        
        self.hover_rectangle.pos = self.a_image.pos
        self.hover_rectangle.size = self.a_image.size
        

    def update_text_textboxes(self, *args):
        self.title.text_size = [self.boxlayout.width, self.title.height] # If this doesn't work, do self.title.parent.width
        self.description.text_size = [self.boxlayout.width, self.description.height]

    def update_image_height(self, *args):
        self.a_image.height = (self.a_image.width / self.a_image.texture_size[0]) * self.a_image.texture_size[1] # whatever the aspect ratio needs to be, alternatively, I could do a image manager thing

    def update_height(self, *args):
        self.height = self.space_0.height + ((self.boxlayout.width / self.a_image.texture_size[0]) * self.a_image.texture_size[1]) + self.space_1.height + self.title.height + self.space_2.height + self.description.height+ 5 # I need to replace self.boxlayout.width with the image height, if we can know it...

    def update_boxlayout(self, *args):
        self.boxlayout.width = 64

    def on_hover(self):
        #Window.set_system_cursor("hand") #this may need to be handled in filebrowser since on_exit and on_hover will always be simultaneously called. EDIT 21-02-2020, this could be done so that filebrowser sets to arrow IF NOT in specialimage
        if self.selected == False:
            self.hover = True
            #self.parent.parent.parent.hover_count += 1  not fool proof
            self.update_rectangles()
            self.animation_on_hover_image.start(self.hover_widget.canvas)
            self.animation_on_hover_text.start(self.title)
            self.animation_on_hover_background.start(self)  


    def on_exit(self):
        self.hover = False
        #self.parent.parent.parent.hover_count -= 1 not foo lproof
        #Window.set_system_cursor("arrow")
        if self.selected == False:
            self.animation_on_exit_image.start(self.hover_widget.canvas)
            self.animation_on_exit_text.start(self.title)
            self.animation_on_exit_background.start(self)  

    def on_press(self): # must have file browser as parent to work, I could always make a clause if I wanted to make specialimage work fine outside of filebrowser
        self.parent.parent.parent.set_selected(self) # let this decide if set_selected should be called
        #self.set_selected()

    def set_selected(self):
        self.selected = True
        self.animation_selected_image.start(self)
        self.animation_test_1.start(self.title)
        self.animation_test_2.start(self.description) 
        self.animation_on_exit_image.start(self.hover_widget.canvas) ### NEW 
        Window.set_system_cursor("arrow") # a quick thing

    def set_deselected(self):
        """
        foolproof is that on_exit can include self.animation_test_3, and this just play on_exit(). and call the onexit animations "text_default" "description_default", "description hover", "description pressed" etc.
        """
        self.selected = False
        self.animation_on_exit_image.start(self.hover_widget.canvas)
        self.animation_on_exit_text.start(self.title)
        self.animation_on_exit_background.start(self) # deselected (background) animation is now redundant?
        self.animation_test_3.start(self.description)