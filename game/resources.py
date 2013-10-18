#!/usr/bin/env python
import pyglet
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

player_image = pyglet.resource.image('player.png')
bullet_image = pyglet.resource.image('bullet.png')
asteroid_image = pyglet.resource.image('asteroid.png')
missile_image = pyglet.resource.image('missile.png')
#explosion_image = pyglet.resource.image('explosion.png')
explosion_image = pyglet.image.ImageGrid(pyglet.image.load('explosion_sprite.png'), 1, 5)
end = 5
start = 1
explosion_sprite = []

for explosion_sprite in explosion_image[start:end:1]:
    explosion_sprite.append(AnimationFrame(explosion_sprite, 0.1))

explosion_sprite[(5) -1].duration = None

def center_image(image):
    print("Sets an image anchor point to it's center")
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

center_image(player_image)
center_image(bullet_image)
center_image(asteroid_image)
center_image(missile_image)
#center_image(explosion_image)

engine_image = pyglet.resource.image('engine_flame.png')
engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height / 2
