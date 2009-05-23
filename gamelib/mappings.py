from util import resources, particle

door_types = {}
unit_images = {}

def init():
    global door_types, unit_images
    particle.fire_image = resources.fire
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
    unit_images = dict(
        Unit =              None,
        Beacon =            resources.beacon_1, 
        NormalTurretA =     resources.turret1, 
        Bomb =              resources.bomb_static,
        Bomb_active =       resources.bomb_static,
        Brain =             resources.core,
        Cargo =             resources.cargo,
        Decoy =             resources.decoy_off,
        Decoy_on =          resources.decoy_on,
        GluballBrain =      resources.core,
        Repair =            resources.repair, 
        Shield =            resources.shield, 
        Thruster =          resources.thruster_off,
        Thruster_on =       resources.thruster_on,
        Toxin =             resources.Harvester_1
    )
    