import pyglet
from pyglet.window import key
from collections import defaultdict

fullscreen = False
profiler = None
norm_w = 1120
norm_h = 700
norm_theta = 0.558599315344
sidebar_w = 0
scale_factor = 1.0
main_window = None
dt = 0.0

enable_damping = True

camera_x = 0
camera_y = 0
camera_target_x = 0
camera_target_y = 0
cvx = 1
cvy = 1

key_bindings = defaultdict(list)

batch = None
floor_group = None
decal_group = None
tank_group = None
bullet_group = None
unit_group = None
door_group = None
overlay_group = None
prim_color = (0.4, 0.4, 0.4, 1)

def init():
    global key_bindings
    key_bindings = defaultdict(list)

def init_graphics():
    global batch, floor_group, decal_group, tank_group, unit_group, door_group
    global bullet_group, overlay_group
    batch = pyglet.graphics.Batch()
    floor_group = pyglet.graphics.OrderedGroup(0)
    decal_group = pyglet.graphics.OrderedGroup(1)
    tank_group = pyglet.graphics.OrderedGroup(2)
    unit_group = pyglet.graphics.OrderedGroup(3)
    door_group = pyglet.graphics.OrderedGroup(4)
    bullet_group = pyglet.graphics.OrderedGroup(5)
    overlay_group = pyglet.graphics.OrderedGroup(6)

def move_camera(x, y):
    global camera_x, camera_y
    if camera_x < camera_target_x-cvx: camera_x += cvx
    if camera_x > camera_target_x+cvx: camera_x -= cvx
    if abs(camera_x-camera_target_x) <= cvx: camera_x = camera_target_x
    if camera_y < camera_target_y-cvy: camera_y += cvy
    if camera_y > camera_target_y+cvy: camera_y -= cvy
    if abs(camera_y-camera_target_y) <= cvy: camera_y = camera_target_y

def scale():
    pyglet.gl.glScalef(scale_factor,scale_factor,1)

def apply_camera():
    pyglet.gl.glTranslatef( -camera_x+norm_w//2+sidebar_w//2, -camera_y+norm_h//2,0)

def clean_key_string(string):
    convert_dict = {
        "LSHIFT": "Shift",
        "RSHIFT": "Right Shift",
        "BACKSPACE": "Backspace",
        "TAB": "Tab",
        "CLEAR": "Clear",
        "RETURN": "Return",
        "ENTER": "Enter",
        "SCROLLLOCK": "Scroll Lock",
        "ESCAPE": "Escape",
        "HOME": "Home",
        "LEFT": "Left",
        "UP": "Up",
        "RIGHT": "Right",
        "DOWN": "Down",
        "PAGEUP": "Page Up",
        "PAGEDOWN": "Page Down",
        "END": "End",
        "DELETE": "Delete",
        "SELECT": "Select",
        "INSERT": "Insert",
        "SPACE": "Space",
        "CAPSLOCK": "Caps Lock"
    }
    try:
        return convert_dict[string]
    except:
        return string

def symbol_to_string(symbol):
    return clean_key_string(key.symbol_string(symbol))
    
def bind_key(symbol, unit):
    global key_bindings
    key_bindings[symbol].append(unit)

def bind_keys(symbols, unit):
    global key_bindings
    for symbol in symbols:
        key_bindings[symbol].append(unit)

def clear_key_bindings():
    global key_bindings
    key_bindings = defaultdict(list)

def unbind_keys_for_unit(unit):
    global key_bindings
    for k, unit_list in key_bindings.items():
        if unit in unit_list:
            key_bindings[k].remove(unit)