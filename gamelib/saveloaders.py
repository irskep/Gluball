import math
import body, decal, enemy, event, obstacle, unit
from util import env, resources

def unit_from_dict(unit_dict):
    if unit_dict['ClassName'] == 'Key':
        new_unit = unit.Key(
            number=unit_dict['number'], obj_id=unit_dict['obj_id'],
            load_from=unit_dict
        )
    else:
        try:
            new_unit = getattr(unit, unit_dict['ClassName'])(load_from=unit_dict)
        except:
            print "Did not load", unit_dict['ClassName']
            return None
    env.bind_keys(unit_dict['key_bindings'], new_unit)
    return new_unit

def make_turret(obj):
    if obj == None: return None
    turret_class = None
    turret_dict = {
        "Turret": enemy.NormalTurretA
    }
    if obj.turret_type in turret_dict.keys():
        turret_class = turret_dict[obj.turret_type]
        base_img = getattr(resources, obj.base_type)
        base_rotation = obj.base_rotation
        new_turret = turret_class(
            obj.position[0], obj.position[1], 
            math.degrees(obj.angle), obj.obj_id, base_img, base_rotation
        )
        new_turret.alive = obj.alive
        new_turret.health = obj.health
        new_turret.on_target = obj.on_target
        new_turret.recoil_status = obj.recoil_status
        new_turret.targeting = obj.targeting
        return new_turret
    return None

def EventData(obj):
    event.load_from_yaml_obj(obj, level_module)

def DecalInvisList(obj):
    for d in decal.decals:
        if d.obj_id in obj.invisibles:
            d.make_invisible()

def Decal(obj):
    if not hasattr(obj, 'overhead'): obj.overhead = False
    new_decal = decal.Decal(
        getattr(resources, obj.name), obj.x, obj.y, 
        obj.rotation, obj.obj_id, obj.scale, obj.overhead
    )
    if not obj.visible: new_decal.make_invisible()

def ImageDoor(obj):
    new_door = obstacle.ImageDoor(
        obj.x, obj.y, obj.rotation, obj.obj_id, obj.key, obj.closed, obj.manual
    )

def Rock(obj):
    new_rock = obstacle.StationaryRock(
        obj.position[0], obj.position[1], obj.rotation,
        obj.kind, obj.obj_id
    )
    if not obj.visible: new_rock.make_invisible()

def SingleBody(obj):
    free_unit = unit_from_dict(obj.unit)
    if free_unit != None:
        free_body = body.SingleBody(
            obj.position, math.degrees(obj.angle), free_unit
        )
        free_body.attachable = obj.attachable
        free_body.body.velocity = obj.velocity
        free_body.body.angular_velocity = obj.angular_velocity
        if not obj.visible:
            free_body.make_invisible()

def Wall(obj):
    new_wall = obstacle.DestructibleWall(
        obj.x, obj.y, obj.rotation, obj.name, obj.obj_id
    )