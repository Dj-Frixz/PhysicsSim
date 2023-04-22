from pickle import FALSE
from pygame.math import Vector2
from pygame.transform import smoothscale, rotozoom
from pygame.draw import circle
from numpy import floor

from utils import load_sprite, load_sound

UP = Vector2(0, -1)
# C = 299792458
# G = 6.6743e-11
# GRAVITY = {'direction': Vector2(0, 1), 'acceleration': 0.2}

class StaticObject:
    bounce = True
    sound = False
    gravity = True
    repulsion = True
    scale = 1

    def __init__(self, position, radius, mass=0, rect=None, velocity=Vector2()) -> None:
        self.next = None
        self.position = Vector2(position)
        self.mass = mass
        self.color = (0,0,0)
        self.radius = radius  # self.rect.width / 2
        self.velocity = Vector2(velocity)
        self.rect = rect
        self.collide = 0
        # self.inertial_energy = mass*(C**2)
        # self.kinetic_energy =  0.5*mass*(velocity*velocity)

    def move(self,*args):
        self.velocity *= 0

    def apply_forces(self, time=1/60):
        obj = self.next
        while obj is not None:
            direction = obj.position - self.position    # (x2 - x1)
            distance = direction.length()
            if distance!=0:
                
                # velocity = acceleration*time = Force*time/mass
                invsq_distance = 1/distance**2
                force = direction.normalize()*time*invsq_distance
                forces = (force*self.mass, force*obj.mass)
                self._gravitational_force(obj,forces,distance)
                self._repulsive_force(obj,forces,distance,invsq_distance)
                if distance<=(self.radius+obj.radius): self.collision(obj,obj.velocity,direction,invsq_distance)
                        
            obj = obj.next
    
    def _gravitational_force(self,obj,forces,radius):
        if radius>(self.radius+obj.radius) and self.gravity:
            self.velocity += forces[1]
            obj.velocity += -forces[0]
    
    def _repulsive_force(self,obj,forces,distance,invsq_distance):
        if (self.radius+obj.radius)/2<distance<(self.radius+obj.radius) and self.repulsion:
            self.velocity += -forces[1]*obj.mass*(invsq_distance**3)
            obj.velocity += forces[0]*self.mass*(invsq_distance**3)
    
    def collision(self,obj,v2,r,invsq_r):
        delta_v = self.velocity - v2
        obj.velocity = v2 - 2*self.mass/(self.mass + obj.mass) * (((-delta_v)*r) * invsq_r) * r
        self.velocity = delta_v - 2*(delta_v*r * invsq_r)*r + obj.velocity

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

    def draw(self, screen):
        # blit_position = self.position - Vector2(self.radius)
        # screen.blit(self.sprite, blit_position)
        circle(screen, self.color, self.position, self.radius)

class Object(StaticObject):
    ELASTICITY = 0.9

    def __init__(self, position, radius, mass=0, rect=None, velocity=Vector2()):
        self.boing = load_sound('boing')

        super().__init__(position, radius, mass, rect, velocity)

    def move(self,surface,wrapper:bool, time=1/60):
        if wrapper: self.window_border_collision(surface, time)
        else: self.position += self.velocity*time*self.scale
        kinetic_energy = 0.5*self.mass*(self.velocity*self.velocity)
        color_intensity = floor(255*(1 - 1.00001**-kinetic_energy))
        self.color = (color_intensity,color_intensity,color_intensity)

    def window_border_collision(self, surface, time):       ###### COSTRAINT REACTION OF THE BORDER ######
        k_el = self.ELASTICITY if Object.bounce else 1
        x_vel, y_vel = self.velocity                        #take position coords where (0,0)
        x_res, y_res = self.position + self.velocity*time   #is top-left of the screen
        width, height = surface.get_size()
        offset_x, offset_y = (self.radius, self.radius) if self.rect==None else (self.rect.w/2, self.rect.h/2)
                                                            #as the vector originates at the center of the obj
                                                            #this shift the collision to its edges
        width -= offset_x
        height -= offset_y
        
        if x_res <= offset_x:                               #in order: left, right, top, bottom (border checks)
            if x_res < offset_x:
                x_res = 2 * offset_x - x_res
                x_vel = -x_vel * k_el
                if -2 < x_vel < 2: x_res, x_vel = offset_x, 0
                if self.sound: self.boing.play()
        elif x_res >= width:                                ##########  the formula is composed by  ###########
            if x_res > width:
                x_res = 2 * width - x_res                   ## :: difference = resultant - offset_x          ##
                x_vel = -x_vel * k_el                       ##  (how much of the res vect is off the screen) ##
                if -2 < x_vel < 2: x_res, x_vel = width, 0
                if self.sound: self.boing.play()
        if y_res <= offset_y:                               ## :: sub_vect = 2 * difference                  ##
            if y_res < offset_y:
                y_res = 2 * offset_y - y_res                ##  (double the previous difference)             ##
                y_vel = -y_vel * k_el                       ## :: resultant - sub_vect                       ##
                if -2 < y_vel < 2: y_res, y_vel = offset_y, 0
                if self.sound: self.boing.play()
        elif y_res >= height:                               ##  (finds where the reflected vect points)      ##
            if y_res > height:
                y_res = 2 * height - y_res                  ###################################################
                y_vel = -y_vel * k_el
                if -2 < y_vel < 2: y_res, y_vel = height, 0
                if self.sound: self.boing.play()
        
        self.position, self.velocity = Vector2(x_res, y_res), Vector2(x_vel, y_vel)


class MainCharacter(Object):
    MANEUVERABILITY = 3
    ACCELERATION = 0.5

    def __init__(self, position):
        self.direction = Vector2(UP)
        self.brum = load_sound('brum')
        self.enabled = True
        self.sprite = load_sprite("spaceship.png")

        super().__init__(
            position,
            radius=0,
            mass=5,
            rect=self.sprite.get_rect()
        )
    
    def clear(self):    # erase everything?
        self.next = None
        self.enabled = False

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        if self.sound: self.brum.play(fade_ms=1000)
    
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        self.rect = rotated_surface.get_rect()