import pyglet, math, pymunk
from util import physics, resources

EnemyPlasmaOrange = None
PlayerPlasmaOrange = None

def init():
    global EnemyPlasmaOrange, PlayerPlasmaOrange
    EnemyPlasmaOrange, PlayerPlasmaOrange = make_bullet_class(resources.bullet_orange, 700, 10)

def make_bullet_class(img, speed, damage):
    class EnemyBullet(Bullet):
        velocity = speed
        def __init__(self, x, y, vx, vy, batch=None, group=None):
            super(EnemyBullet, self).__init__(
                physics.ENEMY_BULLET, img, damage, 
                x, y, vx, vy, False, batch, group
            )
    class PlayerBullet(Bullet):
        velocity = speed
        def __init__(self, x, y, vx, vy, batch=None, group=None):
            super(PlayerBullet, self).__init__(
                physics.PLAYER_BULLET, img, damage, 
                x, y, vx, vy, False, batch, group
            )
    return EnemyBullet, PlayerBullet

class Bullet(pyglet.sprite.Sprite):
    velocity = 700.0
    def __init__(
                self, col_type, img, damage, 
                x, y, vx, vy, rotate=False, batch=None, group=None
            ):
        super(Bullet, self).__init__(img, x, y, batch=batch, group=group)
        self.damage = damage
        
        if rotate:
            self.rotation = math.degrees(-math.atan2(vy, vx))
        
        radius = 4
        mass = physics.default_density*(radius*radius*2*math.pi)
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = (x,y)
        self.body.velocity = (vx, vy)
        
        self.shape = pymunk.Circle(self.body, radius, (0,0))
        self.shape.friction = 1.0
        self.shape.elasticity = 0.0
        self.shape.parent = self
        self.shape.collision_type = col_type
        self.shape.layers = 1
        
        physics.space.add(self.body)
        physics.space.add(self.shape)
        
        physics.body_update_list.append(self)
    
    def update(self):
        self.x = self.body.position.x
        self.y = self.body.position.y
    
    def update_physics(self):
        pass
    
