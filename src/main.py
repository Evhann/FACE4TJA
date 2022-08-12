from ursina import *
import os
from operator import attrgetter
from settings import SETTINGS

mode = 1 # 0: view, 1: notes

tja_editor_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(tja_editor_path)

bg_id = str(SETTINGS.editor.background_id)

window.title = "FACE4TJA - Untitled"
window.icon = "assets/icon.ico"
app = Ursina()
window.borderless = False
window.exit_button.enabled = False
window.size = (1152, 648)
camera.orthographic = True

notes = []

bpm = 120
title = "Untitled"
stars = 10

# assets
note_little_roll = Texture("assets/note_little_roll.png")
note_large_roll = Texture("assets/note_large_roll.png")
note_little_don = Texture("assets/note_little_don.png")
note_large_don = Texture("assets/note_large_don.png")
note_large_kat = Texture("assets/note_large_kat.png")
note_little_kat = Texture("assets/note_little_kat.png")
note_little_unselected = Texture("assets/note_little_unselected.png")
note_large_unselected = Texture("assets/note_large_unselected.png")

background = Entity(parent=camera.ui, model='quad', texture=f"assets/backgrounds/background_{bg_id}.png", scale=(window.aspect_ratio,1))

highway = Entity(parent=camera.ui, model='quad', color=color.hex('#2c2b2c'),
                 scale=(window.aspect_ratio,0.12), position=(0, 0.25))

note_preview = Entity(parent=camera.ui, model='quad', texture=note_little_unselected, color=color.white66,
                      scale=0.07)
note_preview.y = highway.y

bpm_input = TextField(parent=camera.ui, max_lines=1, text="120")
bpm_input.position = note_preview.position
bpm_input.y -= 0.2
bpm_input.x -= 0.8
bpm_label = Text(parent=camera.ui, text="BPM: ", position=bpm_input.position)
bpm_label.x -= 0.08

title_input = TextField(parent=camera.ui, max_lines=1, text="Untitled")
title_input.position = note_preview.position
title_input.y -= 0.25
title_input.x -= 0.8
title_label = Text(parent=camera.ui, text="Title: ", position=bpm_input.position)
title_label.x -= 0.08
title_label.y -= 0.05

stars_input = TextField(parent=camera.ui, max_lines=1, text="10")
stars_input.position = note_preview.position
stars_input.y -= 0.3
stars_input.x -= 0.8
stars_label = Text(parent=camera.ui, text="Stars: ", position=title_input.position)
stars_label.x -= 0.08
stars_label.y -= 0.05

def update():
    note_preview.x = mouse.position.x
    if int(stars_input.text) < 10:
        stars = int(stars_input.text)
    else:
        stars = 5
    
    title = str(title_input.text)
    # print(title)

    try:
        if int(bpm_input.text) < 9999:
            bpm = int(bpm_input.text)
        else:
            bpm = 120
    except Exception as e:
        # print(e)
        bpm = 120
        title = "Untitled"
    # print(bpm)

def input(key):
    # little don
    if key == 'left mouse down':
        e = Entity(parent=camera.ui, model='quad', texture=note_little_don,
                      scale=0.07)
        e.position = note_preview.position
        notes.append(e)
    # little kat
    if key == 'right mouse down':
        e = Entity(parent=camera.ui, model='quad', texture=note_little_kat,
                      scale=0.07)
        e.position = note_preview.position
        notes.append(e)
    
    # little roll
    if key == 'r':
        e = Entity(parent=camera.ui, model='quad', texture=note_little_roll,
                      scale=0.07)
        e.position = note_preview.position
        notes.append(e)

    if held_keys['shift']:
        note_preview.scale = 0.11
        note_preview.texture = note_large_unselected
        # large don
        if key == 'left mouse down':
            e = Entity(parent=camera.ui, model='quad', texture=note_large_don,
                        scale=0.11)
            e.position = note_preview.position
            notes.append(e)
        # large kat
        if key == 'right mouse down':
            e = Entity(parent=camera.ui, model='quad', texture=note_large_kat,
                        scale=0.11)
            e.position = note_preview.position
            notes.append(e)

        # large roll
        if key == 'r':
            e = Entity(parent=camera.ui, model='quad', texture=note_large_roll,
                        scale=0.11)
            e.position = note_preview.position
            notes.append(e)

    else:
        note_preview.scale = 0.07
        note_preview.texture = note_little_unselected
    
    # scroll
    if held_keys['right arrow']:
        for note in notes:
            if isinstance(note, Entity):
                note.x += 1 * time.dt
    if held_keys['left arrow']:
        for note in notes:
            if isinstance(note, Entity):
                note.x -= 1 * time.dt
    
    if held_keys['left control'] and key == 's':
        save_chart()

def load_chart(chart):
    window.title = "FACE4TJA - " + str(chart)
    for note in notes:
        if isinstance(note, Entity):
            destroy(note)

def save_chart():
    with open("test.tja", "w", encoding="utf-8") as tja:
        tja.write(f"TITLE:{title}\n")
        tja.write(f"BPM:{bpm}\n")
        tja.write(f"COURSE:oni\n")
        # tja.write("SCOREINIT:610\nSCOREDIFF:180\n")
        tja.write(f"WAVE:{title}.ogg\n")
        tja.write("OFFSET:-2\n")
        tja.write(f"LEVEL:{stars}\n\n")
        tja.write(f"#START\n")

        notes.sort(key=attrgetter('x'), reverse=False)

        for note in notes:
            if isinstance(note, Entity):
                if note.texture == note_little_don:
                    tja.write(f"1")
                elif note.texture == note_little_kat:
                    tja.write(f"2")
                elif note.texture == note_large_don:
                    tja.write(f"3")
                elif note.texture == note_large_kat:
                    tja.write(f"4")
                elif note.texture == note_little_roll:
                    tja.write(f"5")
                elif note.texture == note_large_roll:
                    tja.write(f"6")

        tja.write("\n#END")
        tja.close()
    print("saved as "+os.getcwd()+"test.tja")

try:
    app.run(info=False)
except Exception as e:
    print("WARNING: "+e)
    app.run()