import body, decal, obstacle, unit
from util import resources
from yamlobjects import *

def Decal(obj):
    if not hasattr(obj, 'overhead'): obj.overhead = False
    new_decal = decal.Decal(
        getattr(resources, obj.img_name), obj.x, obj.y, 
        obj.rotation, obj.obj_id, obj.scale, obj.overhead
    )

def DestructibleWall(obj):
    new_door = obstacle.DestructibleWall(
        obj.x, obj.y, obj.rotation, obj.img_name, obj.obj_id
    )

def Door(obj):
    new_door = obstacle.Door(
        obj.x1, obj.y1, obj.x2, obj.y2, 
        obj.obj_id, obj.key, obj.visible
    )

def ImageDoor(obj):
    new_door = obstacle.ImageDoor(
        obj.x, obj.y, obj.rotation, obj.obj_id, obj.key
    )

def Key(obj):
    free_unit = unit.Key(
        number=obj.number, obj_id=obj.obj_id
    )
    free_body = body.SingleBody((obj.x, obj.y), 0, free_unit)

def Rock(obj):
    new_rock = obstacle.StationaryRock(
        obj.x, obj.y, obj.rotation, obj.rock_type, obj.obj_id
    )