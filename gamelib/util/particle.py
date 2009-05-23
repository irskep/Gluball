#Originally by Phil Hassey
#Modifications by Steve Johnson
#I couldn't find the license he put on it, so I assume public domain

import random, math, env
rr = random.randrange

import pyglet, resources
from pyglet.gl import *
from pyglet import clock
from pyglet.image import *
from pyglet.window import *
from pyglet.window.event import *
from pyglet.window import key

fires = []

class Fire: 
    def __init__(self,x,y,vx,vy,frame,size):
        self.x,self.y,self.vx,self.vy,self.frame,self.size = x,y,vx,vy,frame,size

class FireManager:
    def __init__(self, x, y, num=30, speed=150.0, spread=15.0, decay=100.0):
        self.delete_me = False
        self.goodies = []
        self.batch = pyglet.graphics.Batch()
        self.fimg = fire_image
        self.group = pyglet.sprite.SpriteGroup(self.fimg.texture,
            blend_src=GL_SRC_ALPHA, blend_dest=GL_ONE)
        self.vertex_list = self.batch.add(4*num, GL_QUADS, self.group,
            'v2i', 'c4B', ('t3f', self.fimg.texture.tex_coords*num))
        self.decay = decay
        for n in xrange(0, num):
            angle = random.random()*math.pi*2
            speed_local = random.random()*speed
            spread_local = random.random()*spread
            vx, vy = speed_local*math.cos(angle), speed_local*math.sin(angle)
            px, py = x+spread_local*math.cos(angle), y+spread_local*math.sin(angle)
            f = Fire(
                px, py, vx, vy, random.randrange(50,250),
                8+pow(random.randrange(0.0,100)/100.0,2.0)*32
            )
            f.scale= f.size/32.0
            self.goodies.append(f)
            self.vertex_list.vertices[n*8:(n+1)*8] = [0, 0, 0, 0, 0, 0, 0, 0]
            self.vertex_list.colors[n*16:(n+1)*16] = [0,0,0,0,] * 4

    def update(self,dt):
        if self.delete_me: return
        w,h = self.fimg.width,self.fimg.height
        fires = self.goodies
        verts, clrs = self.vertex_list.vertices, self.vertex_list.colors
        to_delete = []
        num_alive = 0
        for n,f in enumerate(fires):
            if f.frame > 0:
                num_alive += 1
                x = f.x = f.x+f.vx*dt
                y = f.y = f.y+f.vy*dt
                c = 3*f.frame/255.0;
                r,g,b = (min(255,int(c*0xc2)),min(255,int(c*0x41)),min(255,int(c*0x21)))
                f.frame -= dt*self.decay
                ww,hh = w*f.scale,h*f.scale
                x -= ww/2
                y -= hh/2
                verts[n*8:(n+1)*8] = [int(i) for i in [x,y,x+ww,y,x+ww,y+hh,x,y+hh]]
                clrs[n*16:(n+1)*16] = [r,g,b,255] * 4
            else:    
                verts[n*8:(n+1)*8] = [0, 0, 0, 0, 0, 0, 0, 0]
                clrs[n*16:(n+1)*16] = [0,0,0,0,] * 4
        if num_alive == 0:
            self.delete_me = True
    
    def draw(self):
        if not self.delete_me:
            self.batch.draw()
            

def new_explosion(x, y, num=30, speed=150.0, spread=15.0, decay=100.0):
    fires.append(FireManager(x,y,num,speed,spread,decay))

def update():
    global fires
    to_remove = []
    for fire in fires:
        fire.update(env.dt)
        if fire.delete_me:
            to_remove.append(fire)
    for fire in to_remove:
        fires.remove(fire)
        del fire

def draw():
    for fire in fires:
        fire.draw()

def main():
    window = pyglet.window.Window()
    
    fires = []

    @window.event
    def on_draw(dt=0):
        window.clear()
        to_remove = []
        for fire in fires:
            fire.update(dt)
            fire.draw()
            if fire.delete_me:
                to_remove.append(fire)
        for fire in to_remove:
            fires.remove(fire)
            del fire
    pyglet.clock.schedule(on_draw)
    
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        fires.append(FireManager(x, y))
    
    pyglet.app.run()
    
if __name__ == '__main__': main()