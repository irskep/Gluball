import os, sys, math, yaml
import pyglet, pymunk
import body, decal, enemy, event, mappings, unit
import objloaders, saveloaders, shapeloaders
from util import env, resources, music, sound
from util import physics, serialize, settings
from util import save as savegame
from pyglet.window import key

width = 50*40
height = 50*40
player_start_x = 100
player_start_y = 100
player_start_angle = 1.57
player_config = 'normal'

background_image = None

current_level = ""
level_dir = ""
entry_point = ""
entry_points = []

restart_countdown = -1

player = None
decoy_present = 0
decoy_x = 0
decoy_y = 0
mass = 0
power = 0
logic = 0
power_per_unit = 0

music_player = None

root_1 = os.path.join('Data','Levels')
root_2 = os.path.join(settings.settings_dir,'Levels')

def init_player(x, y, angle, config='normal'):
    global player
    if config == 'enhanced_1' or config == 'enhanced_3':
        ot = (10, 48)
        rt = 15
    elif config == 'enhanced_2':
        ot = (10, 48)
        rt = 45
    else:
        ot = (15, 45)
        rt = 0
    thruster_left_bottom = unit.Thruster(None, (-32,33), -rt, obj_id=-5)
    thruster_right_bottom = unit.Thruster(None, (-32,-33), rt, obj_id=-4)
    thruster_left_top = unit.Thruster(None, (ot[0], ot[1]), 180, obj_id=-3)
    thruster_right_top = unit.Thruster(None, (ot[0], -ot[1]), 180, obj_id=-2)
    
    if config == 'enhanced_3':
        brain = unit.Brain2(None, (0,0), 90, obj_id=-1)
    else:
        brain = unit.Brain(None, (0,0), 90, obj_id=-1)
    
    new_shapes = [brain, thruster_left_bottom, thruster_right_bottom,
                thruster_left_top, thruster_right_top]
    
    if config == 'enhanced_1' or config == 'enhanced_3':
        repair = unit.Repair(None, (40, 0), 0, obj_id=-6)
        gun_left = unit.NormalTurretA(None, (55, 30), 10, obj_id=-7)
        gun_right = unit.NormalTurretA(None, (55, -30), -10, obj_id=-8)
        new_shapes.extend([repair, gun_left, gun_right])
        env.bind_keys([key.SPACE], gun_left)
        env.bind_keys([key.SPACE], gun_right)
    if config == 'enhanced_2':
        repair = unit.Repair(None, (40, 0), 0, obj_id=-6)
        gun_left = unit.NormalTurretA(None, (55, 30), 10, obj_id=-7)
        gun_right = unit.NormalTurretA(None, (55, -30), -10, obj_id=-8)
        thruster_left_out = unit.Thruster(None, (-27,81), -20, obj_id=-9)
        thruster_right_out = unit.Thruster(None, (-27,-81), 20, obj_id=-10)
        new_shapes.extend([repair, thruster_right_out, thruster_left_out, gun_left, gun_right])
        env.bind_keys([key.SPACE], gun_left)
        env.bind_keys([key.SPACE], gun_right)
        env.bind_keys([key.RIGHT, key.UP], thruster_left_out)
        env.bind_keys([key.LEFT, key.UP], thruster_right_out)
    
    env.bind_keys([key.RIGHT, key.UP], thruster_left_bottom)
    env.bind_keys([key.LEFT, key.UP], thruster_right_bottom)
    env.bind_keys([key.LEFT, key.DOWN], thruster_left_top)
    env.bind_keys([key.RIGHT, key.DOWN], thruster_right_top)
    
    player = body.GlueBody((x, y), angle, new_shapes)

def add_free_object(Class, x, y, rot, obj_id=0):
    free_unit = Class(obj_id=obj_id)
    free_body = body.SingleBody((x, y), rot, free_unit)
    return free_unit

def load_yaml_objects(yaml_objects):
    global player_start_x, player_start_y, player_start_angle, player_config
    
    for obj in yaml_objects:
        try:
            getattr(objloaders, obj.yaml_tag[1:])(obj)
        except TypeError:
            if obj.yaml_tag == u"!Env":
                player_start_x, player_start_y = obj.player_x, obj.player_y
                if not hasattr(obj, 'player_angle'):
                    obj.player_angle = 1.57
                player_start_angle = obj.player_angle
                if not hasattr(obj, 'player_config'):
                    obj.player_config = 'normal'
                player_config = obj.player_config
            elif obj.yaml_tag.startswith(u"!Free"):
                try:
                    unitclass = mappings.unit_special_cases[obj.yaml_tag]
                except:
                    unitclass = obj.yaml_tag[5:]
                add_free_object(
                    getattr(unit, unitclass), 
                    obj.x, obj.y, obj.rotation, obj.obj_id
                )
            elif obj.yaml_tag in mappings.turret_yaml_types:
                if not hasattr(obj, 'base_type'):
                    obj.base_type = 'normal'
                    obj.base_rotation = 0.0
                new_static_object = getattr(enemy, obj.yaml_tag[1:])(
                    obj.x, obj.y, obj.rotation, obj.obj_id,
                    getattr(resources, "turret_base_"+obj.base_type), obj.base_rotation
                )

def load_geometry(yaml_objects):
    global width, height
    global background_image, prim_color
    decal.decals = []
    
    for obj in yaml_objects:
        if obj.yaml_tag == u"!Env":
            width, height = obj.width, obj.height
            env.prim_color = tuple([c/255.0 for c in obj.prim_color])
            background_image = pyglet.image.TileableTexture.create_for_image(
                getattr(resources, obj.background_image)
            )
        else:
            try:
                getattr(shapeloaders, obj.yaml_tag[1:])(obj)
            except:
                pass #yeah, I know, bad
    
    shapeloaders.add_line(0, 0, width, 0)
    shapeloaders.add_line(width, 0, width, height)
    shapeloaders.add_line(width, height, 0, height)
    shapeloaders.add_line(0, height, 0, 0)

def change_entry_point(new_level_dir, new_entry_point):
    global level_dir, entry_point
    if level_dir != "":
        sys.path.remove(level_dir)
    sys.path.append(new_level_dir)
    level_dir = new_level_dir
    entry_point = new_entry_point

def change_level_set(set_name):
    global level_dir
    set_name = os.path.split(set_name)[-1]
    for info in entry_points:
        if os.path.split(info['Path'])[-1] == set_name:
            if level_dir != "":
                sys.path.remove(level_dir)
            sys.path.append(info['Path'])
            level_dir = info['Path']

def reset():
    restart_countdown = -1
    env.init_graphics()

def load(level_name, keep_config=False, keep_velocity=False):
    global current_level, player
    reset()
    current_level = level_name
    
    path = os.path.join(level_dir, level_name+".yaml")
    stream = file(path, 'r')
    yaml_objects = yaml.load(stream)
    stream.close()
    
    load_geometry(yaml_objects)
    load_yaml_objects(yaml_objects)
    
    shapeloaders.add_line(0, 0, width, 0)
    shapeloaders.add_line(width, 0, width, height)
    shapeloaders.add_line(width, height, 0, height)
    shapeloaders.add_line(0, height, 0, 0)
    
    physics.space.resize_static_hash()
    physics.space.resize_active_hash()
    if not keep_config:
        init_player(player_start_x, player_start_y, math.pi/2, player_config)
        player.body.angle = player_start_angle
    else:
        player.body.position.x = player_start_x
        player.body.position.y = player_start_y
        if not keep_velocity:
            player.body.velocity.x = 0.0
            player.body.velocity.y = 0.0
        physics.body_update_list.append(player)
        physics.unit_update_list.extend(player.units)
        physics.space.add(player.body)
        for unit in player.units:
            if hasattr(unit, 'update_patients_now'):
                unit.update_patients_now = True
            unit.add_shapes()
            unit.batch = None
            unit.batch = batch
            unit.migrate()
    resources.wall_sound = resources.metal_against_metal2        
    event.update_player_units(player.units)
    level_module = __import__(level_name)
    if hasattr(level_module, 'init'): level_module.init()

def load_save_from_path(path, keep_config=False, keep_velocity=False):
    global player, current_level
    reset()
    event.init()
    stream = file(path, 'r')
    yaml_objects = [obj for obj in yaml.load(stream) if obj != None]
    stream.close()
    
    level_module = None
    
    target_queue = []
    
    if player != None:
        for unit in player.units:
            unit.batch = None
    
    for obj in yaml_objects:
        try:
            getattr(saveloaders, obj.yaml_tag[3:])(obj)
        except:
            if obj.yaml_tag == u"!i_LevelData":
                change_level_set(obj.level_dir)
                current_level = obj.level_name
                savegame.set_current_level(obj.level_dir, current_level)
                level_module = __import__(current_level)
                path = os.path.join(level_dir, obj.level_name+".yaml")
                stream = file(path, 'r')
                yaml_geometry = yaml.load(stream)
                stream.close()
                load_geometry(yaml_geometry)
            elif obj.yaml_tag == u"!i_GlueBody":
                if not obj.is_player or not keep_config:
                    unit_list = [saveloaders.unit_from_dict(u) for u in obj.units]
                    new_gluebody = body.GlueBody(
                        obj.position, obj.angle, unit_list
                    )
                    new_gluebody.attachable = obj.attachable
                    new_gluebody.body.velocity = obj.velocity
                    new_gluebody.body.angular_velocity = obj.angular_velocity
                    if obj.is_player:
                        player = new_gluebody
                    for unit in unit_list:
                        if hasattr(unit, 'update_patients_now'):
                            unit.update_patients_now = True
                    
                if obj.is_player and keep_config:
                    player.body.position = obj.position
                    if not keep_velocity:
                        player.body.velocity.x = 0.0
                        player.body.velocity.y = 0.0
                    physics.body_update_list.append(player)
                    physics.unit_update_list.extend(player.units)
                    physics.space.add(player.body)
                    for unit in player.units:
                        unit.add_shapes()
                        unit.batch = batch
                        unit.migrate()
                        if unit.using_sound: unit.init_sound(unit.sound, unit.loop_sound)
            elif obj.yaml_tag == u"!i_Turret":
                new_turret = saveloaders.make_turret(obj)
                new_turret.active = obj.active
                target_queue.append((new_turret, obj.target))
                if not obj.visible: new_turret.make_invisible()
            else:
                print "Did not load", obj
    
    for obj, target in target_queue:
        if target > 0:
            obj.target = event.get_object(target)
    event.update_player_units(player.units)
    resources.wall_sound = resources.metal_against_metal2
    if hasattr(level_module, 'on_load'):
        level_module.on_load()

def load_save(name, keep_config=False, keep_velocity=False):
    new_set, path = savegame.load_from(name)
    change_level_set(new_set)
    load_save_from_path(path, keep_config, keep_velocity)

def save(dest = ""):
    if event.end_game: return
    level_set = os.path.split(level_dir)[-1]
    save_path = os.path.join(savegame.save_path, current_level+".yaml")
    savegame.set_current_level(level_set, current_level)
    event_obj = event.get_yaml_object()
    decal_obj = serialize.YamlDecalInvisList(
        [d.obj_id for d in decal.decals if not d.visible]
    )
    save_list = physics.body_update_list + decal.decals
    level_obj = serialize.YamlLevelData(level_dir, current_level)
    yaml_list = [level_obj, event_obj]
    serialize.save(
        level_dir, current_level, save_list, save_path, yaml_list
    )
    if dest != "":
        savegame.save_to(dest)

def init_entry_points():
    global entry_points
    if not os.path.exists(settings.settings_dir):
        os.makedirs(settings.settings_dir)
    level_sets = [
        f for f in os.listdir(root_1) 
        if os.path.isdir(os.path.join(root_1, f))
    ]
    if not os.path.exists(root_2):
        os.mkdir(root_2)
    level_sets_2 = [
        f for f in os.listdir(root_2) 
        if os.path.isdir(os.path.join(root_2, f))
    ]
    level_sets.extend(level_sets_2)
    for level_set in level_sets:
        info_dict = {'Name': level_set}
        level_path = os.path.join(root_1, level_set)
        if not os.path.exists(os.path.join(level_path, 'Info.txt')):
            level_path = os.path.join(root_2, level_set)
        if os.path.exists(os.path.join(level_path, 'Info.txt')):
            info_dict['Path'] = level_path
            f = open(os.path.join(level_path, 'Info.txt'), 'r')
            for line in f:
                k, v = [s.strip() for s in line.split(":")]
                info_dict[k] = v
                if k == 'Rank': info_dict[k] = int(v)
            entry_points.append(info_dict)
