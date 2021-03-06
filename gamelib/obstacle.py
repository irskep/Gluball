import pyglet, pymunk, math, random
from util import draw, env, physics, resources, serialize, sound
import decal, level, mappings

class Destructible(pyglet.sprite.Sprite):
    def __init__(self, x, y, rot, normal_img, exploded_img):
        self.normal_img = normal_img
        self.exploded_img = exploded_img
        super(Destructible, self).__init__(
            self.normal_img, x, y, batch=env.batch, group=env.tank_group
        )
        self.rotation = rot
        
        self.create_shapes()
        self.add_shapes()
        physics.body_update_list.append(self)
        
        self.should_explode = False
    
    def update(self):
        pass
    
    def update_physics(self):
        if self.should_explode:
            self.explode_now(make_boom=True)
    
    def make_invisible(self):
        if self.visible:
            self.remove_shapes()
            self.visible = False
    
    def make_visible(self):
        if not self.visible:
            self.add_shapes()
            self.visible = True
    
    def explode(self):
        if self.visible:
            self.should_explode = True
    
    def explode_now(self, make_boom=True):
        self.should_explode = False
        self.remove_shapes()
        physics.body_update_list.remove(self)
        new_decal = decal.Decal(
            self.exploded_img, self.x, self.y, self.rotation, self.obj_id
        )
        self.delete()
    
    def create_shapes(self):
        pass
    
    def add_shapes(self):
        pass
    
    def remove_shapes(self):
        pass
    

class DestructibleWall(Destructible):
    def __init__(self, x, y, rot, name, obj_id):
        self.obj_id = obj_id
        #self.health = physics.default_health*5
        self.name = name
        super(DestructibleWall, self).__init__(
            x, y, rot,
            getattr(resources, name),
            getattr(resources, name+"_destroyed")
        )
    
    def get_yaml_object(self):
        return serialize.YamlWall(
            self.x, self.y,
            self.rotation, 
            self.name,
            self.obj_id
        )
    
    def update_physics(self):
        #if self.health <= 0:
        #    self.should_explode = True
        super(DestructibleWall, self).update_physics()
    
    def explode(self):
        self.should_explode = True
    
    def create_shapes(self):
        angle = -math.radians(self.rotation)
        axw = math.cos(angle)*self.image.width*0.5
        ayw = math.sin(angle)*self.image.width*0.5
        axh = math.cos(angle+math.pi/2)*self.image.height*0.5
        ayh = math.sin(angle+math.pi/2)*self.image.height*0.5
        axh2 = axh
        ayh2 = ayh
        if self.name == "Shelf_H":
            axh2 *= 0.3
            ayh2 *= 0.3
        p1 = (self.x + axw + axh, self.y + ayw + ayh)
        p2 = (self.x - axw + axh, self.y - ayw + ayh)
        p3 = (self.x + axw - axh, self.y + ayw - ayh2)
        p4 = (self.x - axw - axh, self.y - ayw - ayh2)
        self.line1 = pymunk.Segment(physics.static_body, p1, p2, 1)
        self.line2 = pymunk.Segment(physics.static_body, p3, p4, 1)
        self.line3 = pymunk.Segment(physics.static_body, p1, p3, 1)
        self.line4 = pymunk.Segment(physics.static_body, p2, p4, 1)
        self.lines = [self.line1, self.line2, self.line3, self.line4]
        for line in self.lines:
            line.obj_id = self.obj_id
            line.friction = physics.default_friction
            line.elasticity = physics.default_elasticity
            line.parent = self
            line.collision_type = physics.WALL
    
    def add_shapes(self):
        for line in self.lines:
            physics.space.add_static(line)
    
    def remove_shapes(self):
        for line in self.lines:
            physics.space.remove_static(line)
    
    def draw_collisions(self):
        for line in self.lines:
            draw.line(line.a.x, line.a.y, line.b.x, line.b.y)
    

class StationaryRock(Destructible):
    def __init__(self, x, y, rot, kind, obj_id):
        self.obj_id = obj_id
        self.kind = kind
        
        self.rock_sizes = [0] * 7
        self.rock_sizes[0] = 60
        self.rock_sizes[1] = 42
        self.rock_sizes[4] = 35
        my_rock = getattr(resources, 'rock_'+str(kind+1))
        self.radius = self.rock_sizes[kind]
        if self.rock_sizes[kind] == 0:
            self.radius = my_rock.height*0.48
        super(StationaryRock, self).__init__(
            x, y, rot, my_rock,
            getattr(resources, "rock_exploded_"+str(kind+1))
        )
    
    def create_shapes(self):   
        self.circle = pymunk.Circle(
            physics.static_body, self.radius, (self.x, self.y)
        )
        self.circle.friction = physics.default_friction
        self.circle.elasticity = physics.default_elasticity
        self.circle.parent = self
        self.circle.collision_type = physics.WALL
        self.circle.obj_id = self.obj_id
    
    def add_shapes(self):
        physics.space.add_static(self.circle)
    
    def remove_shapes(self):    
        physics.space.remove_static(self.circle)
    
    def get_yaml_object(self):
        yaml_obj = serialize.YamlRock(
            kind = self.kind,
            obj_id = self.obj_id,
            position = (self.x, self.y),
            rotation = self.rotation,
            visible = self.visible
        )
        return yaml_obj
    
    def draw_collisions(self):
        r = self.circle.radius
        x, y = physics.static_body.local_to_world(self.circle.center)
        draw.ellipse_outline(x-r, y-r, x+r, y+r)
    

class FloatingObject(pyglet.sprite.Sprite):
    def __init__(self, x, y, rot, img, radius=0, mass=0, obj_id=0):
        if radius == 0: radius = img.height*0.48
        if mass == 0: mass = physics.default_mass
        super(FloatingObject, self).__init__(
            img, x, y, batch=env.batch, group=env.unit_group
        )
        self.rotation = rot
        self.obj_id = obj_id
        
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        self.body = pymunk.Body(mass, inertia)
        self.circle = pymunk.Circle(self.body, radius, (0,0))
        self.circle.friction = physics.default_friction
        self.circle.elasticity = physics.default_elasticity
        self.circle.parent = self
        self.circle.collision_type = physics.WALL
        self.circle.obj_id = self.obj_id
        
        physics.space.add([self.body, self.circle])
        self.body.position = (x,y)
        
        physics.body_update_list.append(self)
        
    def update(self):
        self.x, self.y = self.body.position.x, self.body.position.y
        self.rotation = math.degrees(self.body.angle)
    
    def update_physics(self):
        pass
    

class ImageDoor(pyglet.sprite.Sprite):
    def __init__(self, x, y, rotation, obj_id=0, key=0, closed=True, manual=False):
        self.obj_id = obj_id
        self.key = key
        
        self.range_sq = 300*300
        
        if mappings.door_types[self.key]['underlay'] != None:
            decal.decals.append(
                decal.Decal(mappings.door_types[self.key]['underlay'], x, y, rotation)
            )
        
        image = mappings.door_types[self.key]['open_static']
        self.door_width = image.width-image.anchor_x*2
        self.x2 = x + self.door_width*math.cos(-math.radians(rotation))
        self.y2 = y + self.door_width*math.sin(-math.radians(rotation))
        self.xm = (x + self.x2)/2
        self.ym = (y + self.y2)/2
        super(ImageDoor, self).__init__(
            image, x, y, batch=env.batch, group=env.door_group
        )
        self.rotation = rotation
        
        self.segment = pymunk.Segment(
            physics.static_body, (x, y), (self.x2, self.y2), 1
        )
        self.segment.collision_type = physics.WALL
        self.segment.elasticity = physics.default_elasticity
        self.segment.parent = self
        
        self.manual = manual
        self.closed = False
        self.physically_closed = False
        self.swap_countdown = -100
        if closed:
            self.close(fast=True)
        else:    
            mappings.door_types[self.key]['open_static']
        
        physics.body_update_list.append(self)
    
    def get_yaml_object(self):
        return serialize.YamlImageDoor(
            self.x, self.y, self.rotation, self.obj_id, self.key, self.closed, self.manual
        )
    
    def update(self):
        if level.player == None: return
        xd = (level.player.x - self.xm)
        yd = (level.player.y - self.ym)
        if not self.manual:
            if self.swap_countdown == -100:
                if self.closed:
                    if xd*xd+yd*yd < self.range_sq:
                        for unit in level.player.units:
                            if unit.label == "Key" and unit.number == self.key:
                                self.open()
                                return
                else:
                    if xd*xd+yd*yd >= self.range_sq and not self.closed:
                        self.close()
        if self.swap_countdown != -100:
            self.swap_countdown -= env.dt
            if self.swap_countdown <= 0:
                if self.closed:
                    self.close(fast=True)
                else:
                    self.open(fast=True)
                self.swap_countdown = -100
    
    def update_physics(self):
        pass
    
    def close(self, fast=False):
        if fast and not self.physically_closed:
            physics.space.add_static(self.segment)
            self.physically_closed = True
        if not self.closed:
            self.closed = True
            if fast:
                self.image = mappings.door_types[self.key]['closed_static']
            else:
                self.image = mappings.door_types[self.key]['close_anim']
                sound.play(mappings.door_types[self.key]['sound'])
                self.swap_countdown = mappings.door_types[self.key]['collision_delay_close']
    
    def open(self, fast=False):
        if fast and self.physically_closed:
            physics.space.remove_static([self.segment])
            self.physically_closed = False
        if self.closed:
            self.closed = False
            if fast:
                self.image = mappings.door_types[self.key]['open_static']
            else:
                self.image = mappings.door_types[self.key]['open_anim']
                sound.play(mappings.door_types[self.key]['sound'])
                self.swap_countdown = mappings.door_types[self.key]['collision_delay_open']
    
    def draw_collisions(self):
        if self.physically_closed:
            draw.line(self.x, self.y, self.x2, self.y2)
    
