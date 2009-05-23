import pyglet, pymunk
from util import draw, env, physics

def add_line(x1, y1, x2, y2, obj_id=0, visible=True, collides=True, color=None):
    if color == None: color = env.prim_color
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    new_seg = pymunk.Segment(physics.static_body, (x1, y1), (x2, y2), 1)
    new_seg.obj_id = obj_id
    new_seg.elasticity = physics.default_elasticity
    vertex_list = None
    if collides:
        new_seg.collision_type = physics.WALL
    else:    
        new_seg.collision_type = physics.INVISIBLE
    if visible:
        vertex_list = env.batch.add(2, pyglet.gl.GL_LINES, env.floor_group,
            ('v2i', (x1, y1, x2, y2)), ('c4f', color*2))
    else:
        new_seg.elasticity = physics.default_elasticity
    physics.space.add_static([new_seg])

def add_circle(x, y, radius, obj_id=0, visible=True, collides=True, color=None):
    if color == None: color = env.prim_color
    new_circ = pymunk.Circle(physics.static_body, radius, (x, y))
    new_circ.obj_id = obj_id
    new_circ.elasticity = physics.default_elasticity
    if collides:
        new_circ.collision_type = physics.WALL
    else:    
        new_circ.collision_type = physics.INVISIBLE
    if visible:
        segs = draw._concat(
                        draw._iter_ellipse(x-radius,y-radius,x+radius,y+radius))
        numpoints = len(segs)/2
        vertex_list = env.batch.add(
                numpoints, pyglet.gl.GL_LINE_LOOP, env.floor_group,
                ('v2f', segs), ('c4f', color*numpoints))
    physics.space.add_static([new_circ])

def add_rect(x1, y1, x2, y2, obj_id=0, color=None):
    if color == None: color = env.prim_color
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    add_line(x1, y1, x2, y1, obj_id, color=color)
    add_line(x2, y1, x2, y2, obj_id, color=color)
    add_line(x2, y2, x1, y2, obj_id, color=color)
    add_line(x1, y2, x1, y1, obj_id, color=color)
    vertex_list = env.batch.add(
        4, pyglet.gl.GL_QUADS, env.floor_group,
        ('v2f', (x1, y1, x2, y1, x2, y2, x1, y2)), ('c4f', color*4))

def add_triangle(x1, y1, x2, y2, x3, y3, obj_id=0, color=None):
    if color == None: color = env.prim_color
    x1, y1 = int(x1), int(y1)
    x2, y2 = int(x2), int(y2)
    x3, y3 = int(x3), int(y3)
    add_line(x1, y1, x2, y2, obj_id, color=color)
    add_line(x2, y2, x3, y3, obj_id, color=color)
    add_line(x3, y3, x1, y1, obj_id, color=color)
    vertex_list = env.batch.add(
        3, pyglet.gl.GL_TRIANGLES, env.floor_group,
        ('v2f', (x1, y1, x2, y2, x3, y3)), ('c4f', color*3))

def Line(obj):
    c = True
    if hasattr(obj, 'collides'):
        c = obj.collides
    add_line(
        obj.x1, obj.y1, obj.x2, obj.y2, obj.obj_id, obj.visible, c
    )

def Circle(obj):
    c = True
    if hasattr(obj, 'collides'):
        c = obj.collides
    add_circle(
        obj.x, obj.y, obj.radius, obj.obj_id, obj.visible, c
    )

def FilledRect(obj):
    add_rect(
        obj.x1, obj.y1, obj.x2, obj.y2, obj.obj_id
    )

def FilledTriangle(obj):
    add_triangle(
        obj.x1, obj.y1, obj.x2, obj.y2, obj.x3, obj.y3, obj.obj_id
    )