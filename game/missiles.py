import pyglet
import physicalobject, resources

class Missile(physicalobject.PhysicalObject):
    """Bullet fired by player"""

    def __init__(self, *args, **kwargs):
        super(Missile, self).__init__(resources.missile_image, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, 2.0)
        self.is_missile = True
        
    def update(self, dt):
        super(Missile, self).update(dt)

    def die(self, dt):
        self.dead = True
