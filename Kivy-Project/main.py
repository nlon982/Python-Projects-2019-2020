from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

from filebrowser import FileBrowser
from viewport import Viewport
from bigviewport import BigViewport
#from filebrowser_v2 import FileBrowser
from kivy.uix.boxlayout import BoxLayout


Window.size = (1920, 1080)   
                  
class MyApp(App):
    def build(self):
        source_test = r"C:\Users\Nathan Longhurst\Documents\Git\kivy\files"
        source_test = r"C:\Users\Nathan Longhurst\Documents\UX\Image Test"
        #source_test = r"C:\Users\Nathan Longhurst\Documents\Windows Root\Harrisons Kivy Project\Actual Folder\Testing Images Folder\Harrison's Stock\Variants"
        #source_test = r"C:\Users\Nathan Longhurst\Documents\Windows Root\Harrisons Kivy Project\Actual Folder\Testing Images Folder\Harrison's Stock\36 images"
        source_test = r"C:\Users\Nathan Longhurst\Documents\Windows Root\Harrisons Kivy Project\Actual Folder\Testing Images Folder\Photoshop Template"

        # indexing starting at 1 because yolo

        width_of_file_browser = 270
        width_of_viewport = 270

        file_browser_1 = FileBrowser("Range", size_hint = (None, 1), width = width_of_file_browser)
        file_browser_1.populate(source_test)
        viewport_1 = Viewport(size_hint = (None, 1), width = width_of_viewport)

        file_browser_2 = FileBrowser("Range", size_hint = (None, 1), width = width_of_file_browser)
        file_browser_2.populate(source_test)
        viewport_2 = Viewport(size_hint = (None, 1), width = width_of_viewport)

        file_browser_3 = FileBrowser("Range", size_hint = (None, 1), width = width_of_file_browser)
        file_browser_3.populate(source_test)
        viewport_3 = Viewport(size_hint = (None, 1), width = width_of_viewport)



        #file_browser2 = FileBrowser("Variant", 270, 600)
        #file_browser2.populate(source_test)

        #file_browser3 = FileBrowser("Room", 270, 600)
        #file_browser3.populate(source_test)


        column_1 = BoxLayout(orientation = "vertical", size_hint = (None, 1), width = width_of_file_browser + width_of_viewport)

        file_browser_viewport_row_1 = BoxLayout(orientation = "horizontal", size_hint = (None, 1), width = width_of_file_browser + width_of_viewport) # this seems gross, should I get it to calculate the width of its children?
        file_browser_viewport_row_1.add_widget(file_browser_1)
        file_browser_viewport_row_1.add_widget(viewport_1)

        file_browser_viewport_row_2 = BoxLayout(orientation = "horizontal", size_hint = (None, 1), width = width_of_file_browser + width_of_viewport) 
        file_browser_viewport_row_2.add_widget(file_browser_2)
        file_browser_viewport_row_2.add_widget(viewport_2)

        file_browser_viewport_row_3 = BoxLayout(orientation = "horizontal", size_hint = (None, 1), width = width_of_file_browser + width_of_viewport)
        file_browser_viewport_row_3.add_widget(file_browser_3)
        file_browser_viewport_row_3.add_widget(viewport_3)

        column_1.add_widget(file_browser_viewport_row_1)
        column_1.add_widget(file_browser_viewport_row_2)
        column_1.add_widget(file_browser_viewport_row_3)


        column_2 = BoxLayout(orientation = "vertical")

        a_big_viewport = BigViewport(size_hint = (1, 1)) # size_hint by default is 1, 1
        column_2.add_widget(a_big_viewport)


        housing_widget = BoxLayout(orientation = "horizontal") # size hint by default is 1, 1
        housing_widget.add_widget(column_1)
        housing_widget.add_widget(column_2)

        return housing_widget


if __name__ == "__main__": # i.e. if this module is being run, but not by being imported
    MyApp().run()


"""


    def update_height(self, *args):
        self.height = self.space_0.height + ((self.width - 48 / self.a_image.texture_size[0]) * self.a_image.texture_size[1]) + self.space_1.height + self.title.height + self.space_2.height + self.description.height+ 5 # I need to replace self.boxlayout.width with the image height, if we can know it...


        







"""
