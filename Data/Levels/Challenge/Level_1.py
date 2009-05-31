from gamelib import event

NEXT_LEVEL = 48
HELP_1 = 50
HELP_2 = 51
HELP_3 = 52
HELP_4 = 54

BOMB_1 = 42

def show_help_1():
    if event.get_flag('help1'):
        return
    else:
        event.set_flag('help1', True)
    event.show_message("Hold Shift")

def show_help_2():
    if event.get_flag('help2'):
        return
    else:
        event.set_flag('help2', True)
    event.show_message("Get a bomb and press Z to drop it here")

def show_help_3():
    if event.get_flag('help3'):
        return
    else:
        event.set_flag('help3', True)
    event.show_message("Press Escape to reconfigure")

def show_help_4():
    if event.get_flag('help4'):
        return
    else:
        event.set_flag('help4', True)
    event.show_message("RAM IT.")

def level_up():
    event.go_to_level("Level_2")

def init():
    event.register_collision_func(NEXT_LEVEL, level_up)
    event.register_collision_func(HELP_1, show_help_1)
    event.register_collision_func(HELP_2, show_help_2)
    event.register_collision_func(HELP_3, show_help_3)
    event.register_collision_func(HELP_4, show_help_4)
