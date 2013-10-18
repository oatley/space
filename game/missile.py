import pyglet
import physicalobject, resources
import math
import player
import explosion_sprite

class Missile(physicalobject.PhysicalObject):
    """Bullet fired by player"""

    def __init__(self, *args, **kwargs):
        super(Missile, self).__init__(resources.missile_image, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, 4.0)
        self.is_missile = True
        self.thrust = 400.0
        self.rotate_speed = 100.0
        self.max_velocity = 300.0
        
        
    def update(self, dt):
        super(Missile, self).update(dt)
        angle_radians = -math.radians(self.rotation)
        force_x = (math.cos(angle_radians) * self.thrust * dt)
        force_y = (math.sin(angle_radians) * self.thrust * dt)
        self.velocity_x += force_x
        self.velocity_y += force_y


    def die(self, dt):
        new_explosion = explosion_sprite.Explosion(self.x, self.y, batch=self.batch)
        new_explosion.rotation = self.rotation
        self.new_objects.append(new_explosion)
        self.dead = True

