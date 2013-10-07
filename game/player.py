#!/usr/bin/env python
import physicalobject, resources
import pyglet
import math
from pyglet.window import key
import bullet


class Player(physicalobject.PhysicalObject):
    
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
        
        # Forward thrust
        self.thrust = 150.0
        self.max_thrust = 300.0
        self.max_velocity = 500.0
        # Slow down
        self.alt_thrust = 50.0 
        self.rotate_speed = 200.0
        
        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]
        
        self.engine_sprite = pyglet.sprite.Sprite(img=resources.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False

        self.bullet_speed = 700.0
        self.reacts_to_bullets = False
        self.score = 0
       

    def update(self, dt):
        super(Player, self).update(dt)
        
        if self.key_handler[key.LEFT]:
             self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
             self.rotation += self.rotate_speed * dt
        #print self.rotation
        if self.key_handler[key.RSHIFT] or self.key_handler[key.LSHIFT]:
            angle_radians = -math.radians(self.rotation)
            # Slow down the ship, must use positive force
            force_x = math.sqrt((math.cos(angle_radians) * self.alt_thrust * dt)**2)
            force_y = math.sqrt((math.sin(angle_radians) * self.alt_thrust * dt)**2)
            if self.velocity_x > 0:
                self.velocity_x -= force_x
            if self.velocity_x < 0:
                self.velocity_x += force_x
            if self.velocity_y > 0:
                self.velocity_y -= force_y
            if self.velocity_y < 0:
                self.velocity_y += force_y
            if self.velocity_x > 0 and self.velocity_x < 1:
                self.velocity_x = 0.0
            if self.velocity_y > 0 and self.velocity_y < 1:
                self.velocity_y = 0.0
            print "force - ", force_x, " - ", force_y
            print "velocity - ", self.velocity_x, " - ", self.velocity_y
        
        if self.key_handler[key.Z]:
            if self.thrust < self.max_thrust:
                self.thrust += 1
            if self.thrust > self.max_thrust:
                self.thrust = self.max_thrust
            print self.thrust
        if self.key_handler[key.X]:
            if self.thrust < 0:
                self.thrust = 0
            if self.thrust > 0:
                self.thrust -= 1
            print self.thrust
      
        # Add thrust until velocity = 0 while continually changing the zero vector
        # Come to a stop using main thrusters and spinning the ship
        if self.key_handler[key.DOWN]:
            if self.velocity_x == 0 and self.velocity_y == 0:
                self.engine_sprite.visible = False
                return False
            zero_vector = math.radians(math.atan2(self.velocity_y, self.velocity_x) * 180 / math.pi + 180)
            fake = math.sqrt(self.rotation **2)
            # rotation less than 0, invert to positive
            # rotation less than -360, mod 360
            # rotation greater than 0, invert to negative and add 360
            # rotation greater than 360, mod 360
            if math.radians(fake) != zero_vector:
                if self.rotation < 0:
                    fake = -self.rotation
                if self.rotation > 0:
                    fake = (-self.rotation) + 360
                if self.rotation > 360 or self.rotation < -360:
                    fake = fake % 360
            fake = math.radians(fake)
            # Cartesian quadrant 1
            # Cartesian quadrant 2
            # Cartesian quadrant 3
            # Cartesian quadrant 4
            if round(fake, 1) != round(zero_vector, 1):
                self.rotation -= self.rotate_speed * dt
            elif round(fake, 1) == round(zero_vector, 1):
                 fake = zero_vector
                 if self.rotation < 0:
                    print "BANG - Rotation = ", self.rotation, " = ", -math.degrees(zero_vector)
                    self.rotation = -math.degrees(zero_vector)
                 else:
                    print "BANG - Rotation = ", self.rotation, " = ", math.degrees(zero_vector)
                    self.rotation = math.degrees(zero_vector)
           
            if fake == zero_vector and (self.velocity_x != 0 or self.velocity_y != 0):
                if (self.velocity_x < 7 and self.velocity_x > -7) and (self.velocity_y < 7 and self.velocity_y > -7):
                    self.velocity_x, self.velocity_y = 0.0, 0.0
                    return False
                angle_radians = -math.radians(self.rotation)
                force_x = math.cos(angle_radians) * self.thrust * dt
                force_y = math.sin(angle_radians) * self.thrust * dt
                self.velocity_x += force_x
                self.velocity_y += force_y
                self.engine_sprite.rotation = self.rotation
                self.engine_sprite.x = self.x
                self.engine_sprite.y = self.y
                self.engine_sprite.visible = True
            
                 

            print "velocity - ", self.velocity_x, " - ", self.velocity_y
            print "Rotation -> ", math.radians(self.rotation)
            print "zero_vector -> ", zero_vector, " = ", fake
            



        elif self.key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            if self.velocity_x <= self.max_velocity and self.velocity_x >= -self.max_velocity and force_x < 0:
                print "1"
                self.velocity_x += force_x
            elif self.velocity_x <= self.max_velocity and self.velocity_x >= -self.max_velocity and force_x > 0:
                print "2"
                self.velocity_x += force_x
            if self.velocity_y <= self.max_velocity and self.velocity_y >= -self.max_velocity and force_y < 0:
                print "3"
                self.velocity_y += force_y
            elif self.velocity_y <= self.max_velocity and self.velocity_y >= -self.max_velocity and force_y > 0:
                print "4"
                self.velocity_y += force_y
            print self.rotation
            #print "math.cos(angle_radians) - ", math.cos(angle_radians)
            #print "math.sin(angle_radians) - ", math.sin(angle_radians)
            print "angle_radians - ", angle_radians
            print "force - ", force_x, " - ", force_y
            print "velocity - ", self.velocity_x, " - ", self.velocity_y
            self.engine_sprite.rotation = self.rotation
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y
            self.engine_sprite.visible = True
        else:
            self.engine_sprite.visible = False
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.fire()
             
    def delete(self):
        self.engine_sprite.delete()
        super(Player, self).delete()

    def fire(self):
        angle_radians = -math.radians(self.rotation)
        ship_radius = self.image.width/2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = bullet.Bullet(bullet_x, bullet_y, batch=self.batch)

        bullet_vx = (self.velocity_x + math.cos(angle_radians) * self.bullet_speed)
        bullet_vy = (self.velocity_y + math.sin(angle_radians) * self.bullet_speed)
        new_bullet.velocity_x = bullet_vx
        new_bullet.velocity_y = bullet_vy
        self.new_objects.append(new_bullet)
        
        




















