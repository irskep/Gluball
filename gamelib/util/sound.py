import pyglet, settings

players = []
PLAYER_LIMIT = 10
this_player = 0
i = 0

def play(sound):
    new_player = sound.play()
    new_player.volume = settings.sound_volume
