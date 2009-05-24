import pyglet
from pyglet.window import key
import env, gui, widget

class KeyGetter(object):
    def __init__(self, action):
        self.key = -1
        self.action = action
    
    def on_key_press(self, symbol, modifiers):
        if self.key != -1:
            if symbol == key.RETURN:
                self.action(self.key)
                return True
        self.key = symbol
    

class KeyLabel(pyglet.text.Label):
    def __init__(self, x, y, key_getter):
        super(KeyLabel, self).__init__(
            "", x=x, y=y, font_size=24, 
            anchor_x='center', anchor_y='center',
            color=(128,128,128,255)
        )
        self.key_getter = key_getter
    
    def on_key_press(self, symbol, modifiers):
        self.text = env.symbol_to_string(symbol)

screenshot = None
unit_to_bind = None
prev_card_func = gui.go_back_fast

def bind_key_and_return(key):
    env.bind_key(key, unit_to_bind)
    if hasattr(gui.last_card, 'push_handlers'):
        gui.go_back_fast()
    else:    
        gui.pop_handlers()
        gui.current_card = gui.last_card
        gui.last_card = None
        gui.next_card = None

def widgets(extra_image=None):
    background = widget.UnscaledImage(screenshot, 0, 0)
    darken = widget.Rect(0,0,env.norm_w,env.norm_h,(1,1,1,0.7))
    
    key_x = env.norm_w//2
    key_y = env.norm_h*0.75
    
    background_rect = (key_x-200, key_y-120, 400, 240)
    
    rect_fill = widget.Rect(*background_rect)
    rect_fill.color = (1,1,1,1)
    rect_outline = widget.RectOutline(*background_rect)
    rect_outline.color = (0,0,0,1)
    
    getter = KeyGetter(bind_key_and_return)
    
    choose_key_desc_1 = pyglet.text.Label(
        "You have acquired a new unit.", font_name='Gill Sans', font_size=20,
        x=key_x, y=key_y+90, anchor_x='center', anchor_y='center',
        color=(128,128,128,255)
    )
    choose_key_desc_2 = pyglet.text.Label(
        "Choose a key to assign.", font_name='Gill Sans', font_size=20,
        x=key_x, y=key_y+60, anchor_x='center', anchor_y='center',
        color=(128,128,128,255)
    )
    choose_key_desc_confirm = pyglet.text.Label(
        "Press Return to confirm.", font_name='Gill Sans', font_size=20,
        x=key_x, y=key_y-80, anchor_x='center', anchor_y='center',
        color=(128,128,128,255)
    )
    key_label = KeyLabel(key_x, key_y, getter)
    
    if extra_image == None:
        return [
            background, darken,
            rect_fill, rect_outline,
            choose_key_desc_1,
            choose_key_desc_2,
            choose_key_desc_confirm,
            key_label,
            getter
        ]
    else:
        img_x = env.norm_w//2-extra_image.width/2
        img_y = 50
        img_outline = widget.RectOutline(
            img_x, img_y, extra_image.width, extra_image.height
        )
        img_outline.color = (0,0,0,1)
        image_sprite = pyglet.sprite.Sprite(extra_image, img_x, img_y)
        return [
            background, darken,
            rect_fill, rect_outline,
            image_sprite, img_outline,
            choose_key_desc_1,
            choose_key_desc_2,
            choose_key_desc_confirm,
            key_label,
            getter
        ]