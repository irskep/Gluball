import pyglet
from util import env

decals = []
class Decal(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, rot, obj_id=0, scale=1.0, overhead=False):
        if overhead:
            gp = env.overlay_group
        else:
            gp = env.decal_group
        super(Decal, self).__init__(
            img, x, y, batch=env.batch, group=gp
        )
        if abs(rot) < 5: rot = 0
        self.rotation = rot
        self.scale = scale
        self.obj_id = obj_id
        self.overhead = overhead
        decals.append(self)
    
    def get_yaml_object(self):
        return YamlDecal(
            obj_id = self.obj_id,
            name=self.image.instance_name,
            x=self.x,
            y=self.y, 
            rotation=self.rotation,
            scale=self.scale,
            visible=self.visible,
            overhead=self.overhead
        )
    
    def make_invisible(self):
        self.visible = False
    
    def make_visible(self):
        self.visible = True