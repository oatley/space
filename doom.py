#!/usr/bin/env python
import pyglet
from game import resources, load, player
import random
from pyglet import clock

# Main window
game_window = pyglet.window.Window(800, 600, vsync=True, double_buffer=False)

# Batches
main_batch = pyglet.graphics.Batch()

# Labels
#score_label = pyglet.text.Label(text='Score: 0', x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text='My Game', x=400, y=575, anchor_x='center', batch=main_batch)

# Sprites
player_ship = player.Player(x=400, y=300, batch=main_batch)
#asteroids = load.asteroids(15, player_ship.position, main_batch)
#player_lives = load.player_lives(3, main_batch)

game_objects = [player_ship]
#game_window.push_handlers(player_ship.key_handler)

# Add any specified event handlers to the event handler stack
for obj in game_objects:
    for handler in obj.event_handlers:
        game_window.push_handlers(handler)

fps = clock.ClockDisplay()

def update(dt):
    #level_label.text = str(fps.draw())
    # Iterate over object pairs without doing anything
    for i in xrange(len(game_objects)):
        for j in xrange(i+1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]
            
            # Check if the 2 objects collide
            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)
    
    to_add = []
    # Loop through game objects 
    for obj in game_objects:
        obj.update(dt)
        game_objects.extend(obj.new_objects)
        obj.new_objects = []
    
    # Go through the list and remove dead objects 
    for to_remove in [obj for obj in game_objects if obj.dead]:
        to_remove.delete()
        game_objects.remove(to_remove)
    
    game_objects.extend(to_add)



@game_window.event
def on_draw():
    # Clear the screen before drawing
    game_window.clear()

    # Draw the main batch
    main_batch.draw()
    #fps.draw()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()

