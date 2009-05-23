import pyglet, settings

players = []
PLAYER_LIMIT = 10
this_player = 0
i = 0

def play(sound):
    global this_player, players, i
    i += 1
    print i
    if len(players) < PLAYER_LIMIT:
        new_player = pyglet.media.Player()
        new_player.volume = settings.sound_volume
        new_player.eos_action = pyglet.media.Player.EOS_PAUSE
        players.append(new_player)
        this_player = len(players)-1
        new_player.queue(sound)
        new_player.play()
    else:
        this_player = (this_player + 1) % PLAYER_LIMIT
        players[this_player].next()
        players[this_player].queue(sound)
        players[this_player].play()
