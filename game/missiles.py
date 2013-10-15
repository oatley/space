import pyglet
import physicalobject, resources

class Missile(physicalobject.PhysicalObject):
    """Bullet fired by player"""

    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(resources.bullet_image, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, 0.5)
        self.is_bullet = True
        
    def update(self, dt):
        super(Bullet, self).update(dt)

    def die(self, dt):
        self.dead = True
