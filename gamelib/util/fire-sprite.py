import random; rr = random.randrange

import pyglet
from pyglet.gl import *
from pyglet import clock
from pyglet.image import *
from pyglet.window import *
from pyglet.window.event import *
from pyglet.window import key

FIRES = 500
SW,SH = 640,480

fres = None
fimg = None

batch = pyglet.graphics.Batch()

class Fire(pyglet.sprite.Sprite):
    def __init__(self,x,y,vy,frame,size):
        pyglet.sprite.Sprite.__init__(self,fimg,batch=batch,blend_src=GL_SRC_ALPHA, blend_dest=GL_ONE)
        self.x,self.y,self.vy,self.frame,self.size = x,y,vy,frame,size

fires = []

def fire_paint():
    #pass
    batch.draw()
        

def fire_loop(dt,init = False):
    if init:
        for n in xrange(0,FIRES):
            fires.append(Fire(0,0,0,0,0))
    for f in fires:
        if not f.frame:
            f.x = rr(0,SW)
            f.y = rr(500,520)
            f.vy = rr(-70,-40)/100.0
            f.frame = rr(50,250)
            f.size = 8+pow(rr(0.0,100)/100.0,2.0)*32;
            f.scale= f.size/32.0
        
        x,y = f._x,f._y
        #blah = rr(-50,50)/100.0
        f._x,f._y = x+rr(-50,50)/100.0,y+f.vy*6
        f._update_position() 
        #f.x += rr(-50,50)/100.0
        #f.y += f.vy*8
        c = 3*f.frame/255.0;
        f.color = (min(255,int(c*0xc2)),min(255,int(c*0x41)),min(255,int(c*0x21)))
        
        #f.color = (255,255,255)
        f.frame -= 1
  
    if init:
        for n in xrange(0,1):
            fire_loop(0)

def main():
    global fres,fimg
    window = pyglet.window.Window(SW,SH)
    fimg = pyglet.image.load('fire.jpg')
    #fimg = pyglet.image.load('ball.png')
    fimg.anchor_x = fimg.width//2
    fimg.anchor_y = fimg.height//2
    #fres = pyglet.resource.image('fire.jpg')
    #fres = pyglet.resource.image('fire.jpg')
    #fire_image = pyglet.sprite.Sprite(res)
    fire_loop(0,True)

    pyglet.clock.schedule(fire_loop)

    fps = pyglet.clock.ClockDisplay()
    pyglet.clock.schedule(fps.update_text)
    @window.event
    def on_draw():
        
        window.clear()
        
        fire_paint()
        fps.draw()
    

    pyglet.app.run()
    
if __name__ == '__main__': main()