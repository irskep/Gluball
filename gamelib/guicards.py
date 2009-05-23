import pyglet, operator
import level
from util import env, gui, resources, settings, sound, widget
from pyglet.window import key

def start_widgets():
    back_trigger = widget.KeyTrigger(key.ESCAPE, gui.go_back)
    widgets = [back_trigger]
    def level_starter(d, n):
        def start():
            sound.play(resources.whoosh_1)
            level.change_entry_point(d, n)
            if settings.first_launch:
                gui.change_to_card(Card(gui.instruction_widgets_first()))
            else:
                gui.state_goer(gui.START)()
        return start
    
    y = env.norm_h/16*10
    sorted_entry_points = sorted(level.entry_points, key=operator.itemgetter('Rank'))
    
    for info in sorted_entry_points:
        new_button = widget.TextButton(
            info['Name'], env.norm_w/2, y,
            level_starter(info['Path'], info['First level']), 
            anchor_x='center'
        )    
        widgets.append(new_button)
        if 'Author' in info.keys():
            y -= 30
            new_label = pyglet.text.Label(
                "By "+info['Author'], x=env.norm_w/2, y=y,
                color=new_button.color, font_name='Gill Sans',
                font_size=14
            )
            widgets.append(new_label)
        if 'Difficulty' in info.keys():
            y -= 20
            new_label = pyglet.text.Label(
                "Difficulty: "+info['Difficulty'], x=env.norm_w/2, y=y,
                color=new_button.color, font_name='Gill Sans',
                font_size=14
            )
            widgets.append(new_label)
        y -= env.norm_h/8-30
    
    start_trigger = widget.KeyTrigger(key.SPACE, widgets[1].action)
    widgets.append(start_trigger)
    return widgets

def save_widgets():
    back_trigger = widget.KeyTrigger(key.RETURN, gui.go_back)
    back_trigger_2 = widget.KeyTrigger(key.ESCAPE, gui.go_back)
    
    text_box = widget.TextEntry(
        "Save ", env.norm_w/2, env.norm_h/2, env.norm_w-10, 
        level.save, anchor_x='center'
    )
    back_button = widget.TextButton(
        "Back",
        env.norm_w/2, text_box.layout.y-50,
        gui.go_back, 
        size=36, anchor_x='center'
    )
    underline = widget.Line(
        env.norm_w/4, text_box.layout.y-3, env.norm_w/4*3, text_box.layout.y-3
    )
    return [text_box, back_button, back_trigger, back_trigger_2, underline]
