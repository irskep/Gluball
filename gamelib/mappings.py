from util import resources

door_types = {}
unit_images = {}
turret_yaml_types = []
unit_special_cases = {}

def init():
    global door_types, unit_images, turret_yaml_types, unit_special_cases
    door_types[0] = {
        'closed_static': resources.Door_red_closed,
        'open_static': resources.Door_red_open,
        'open_anim': resources.Door_red_open,
        'close_anim': resources.Door_red_closed,
        'underlay': resources.Door_red_open,
        'sound': resources.blast_door_quick_1,
        'collision_delay_open': 0,
        'collision_delay_close': 0
    }
    door_types[4] = {
        'open_static': resources.Door_blue_open,
        'closed_static': resources.Door_blue_closed,
        'open_anim': resources.Door_blue_open,
        'close_anim': resources.Door_blue_closed,
        'underlay': resources.Door_blue_open,
        'sound': resources.blast_door_quick_1,
        'collision_delay_open': 0,
        'collision_delay_close': 0
    }
    unit_images = dict(
        Unit =              None,
        Beacon =            resources.beacon_1, 
        Bomb =              resources.bomb_off,
        Bomb_active =       resources.bomb_on,
        Brain =             resources.core,
        BurstThruster =     resources.burst,
        Cargo =             resources.cargo,
        Decoy =             resources.decoy_off,
        Decoy_on =          resources.decoy_on,
        GluballBrain =      resources.core,
        NormalTurretA =     resources.turret1,
        Repair =            resources.repair, 
        Shield =            resources.shield, 
        Thruster =          resources.thruster_off,
        Thruster_on =       resources.thruster_on,
        TinyThruster =      resources.tinythruster
    )
    turret_yaml_types = [
        u'!NormalTurretA'
    ]
    unit_special_cases = {
        u"!FreeTurret": 'NormalTurretA'
    }
    