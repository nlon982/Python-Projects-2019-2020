from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window

def true_if_within_false_if_not_within(widget, mouse_pos):
    return widget.collide_point(*widget.to_widget(*mouse_pos))

class MouseOver(Widget): #hello

    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self._mouse_move)
        self.hovering = BooleanProperty(False)
        self.poi = ObjectProperty(None)
        self.register_event_type('on_hover')
        self.register_event_type('on_exit')
        super(MouseOver, self).__init__(**kwargs)

    def _mouse_move(self, *args):
        if not self.get_root_window():
            return

        try: # this method to check if has an attribute is preffered wierdly
            # so far, this only allows for one be_within and one be_not_within
            if true_if_within_false_if_not_within(self.be_within, args[1]) == True and true_if_within_false_if_not_within(self.be_not_within, args[1]) == False and true_if_within_false_if_not_within(self.be_not_within_two, args[1]) == False:
                is_collide = self.collide_point(*self.to_widget(*args[1]))
            else:
                is_collide = False
        except: # i.e. do as normal
            is_collide = self.collide_point(*self.to_widget(*args[1]))


        
        if self.hovering == is_collide: # if not hovering, and not colliding. if hovering and colliding
            return
        self.poi = args[1]
        self.hovering = is_collide
        self.dispatch('on_hover' if is_collide else 'on_exit')

    def on_hover(self):
        """Mouse over"""

    def on_exit(self): # not hover may be more accurate, since it's like this if you're not hovering - not just when you exit
        """Mouse leaves"""