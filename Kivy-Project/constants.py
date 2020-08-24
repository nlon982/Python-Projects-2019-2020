from kivy.graphics.texture import Texture

def get_texture():
    texture = Texture.create(size=(2, 2), colorfmt='rgba')

    p1_color = [0, 157, 171, 75]
    p2_color = [0, 157, 171, 75]
    p3_color = [0, 0, 0, 0]
    p4_color = [0, 0, 0, 0]
    p = p1_color + p2_color + p3_color + p4_color

    buf = bytes(p)

    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    return texture

def get_255(one, two, three, four):
    return [one/255, two/255, three/255, four]

light_grey = get_255(230, 230, 230, 1)
almost_black = get_255(69, 77, 84, 1)

light_blue = get_255(198, 229, 235, 1)
rich_blue = get_255(0, 157, 171, 1)

orange = get_255(227, 111, 60, 1)

texture = get_texture()