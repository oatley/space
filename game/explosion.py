import pyglet
import physicalobject, resources

class Explosion(physicalobject.PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(Explosion, self).__init__(resources.explosion_image, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, 1)
        self.is_explosion = True
        self.reacts_to_bullets = False
        self.reacts_to_missiles = False

    def die(self, dt):
        self.dead = True
