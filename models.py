from pickle import FALSE
from pygame.math import Vector2
from pygame.transform import smoothscale, rotozoom
from pygame.draw import circle

from utils import load_sprite, load_sound

UP = Vector2(0, -1)
C = 299792458
# G = 6.6743e-11
# GRAVITY = {'direction': Vector2(0, 1), 'acceleration': 0.2}

class StaticObject:
    sound = False
    scale = 1

    def __init__(self, position, radius, mass=0, velocity=Vector2()) -> None:
        self.next = None
        self.position = Vector2(position)
        self.mass = mass
        # self.sprite = sprite
        self.color = (255,0,0)
        # self.rect = sprite.get_bounding_rect()
        self.radius = radius  # self.rect.width / 2
        self.velocity = Vector2(velocity)
        self.inertial_energy = mass*(C**2)
        self.kinetic_energy =  0.5*mass*(velocity*velocity)

    def move(self,*args):
        self.velocity *= 0

    def apply_forces(self, time=1/60):
        obj = self.next
        while obj is not None:
            direction = obj.position - self.position
            radius = direction.length()
            if radius!=0:
                # velocity = acceleration*time = Force*time/mass
                force = direction.normalize()*time/(radius**2)
                self.velocity += force*obj.mass - force*(obj.mass**2)/(radius**2)
                obj.velocity += -force*self.mass + force*(self.mass**2)/(radius**2)
            obj = obj.next

    def draw(self, screen):
        # blit_position = self.position - Vector2(self.radius)
        # screen.blit(self.sprite, blit_position)
        circle(screen, self.color, self.position, self.radius)

class Object(StaticObject):
    ELASTICITY = 0.9
    bounce = False

    def __init__(self, position, radius, mass=0, velocity=Vector2()):
        self.boing = load_sound('boing')

        super().__init__(position, radius, mass, velocity)

    def gravity(self,obj,force):
        '''Gravitational_force  = G*mass*mass2/radius^2'''
        pass

    def electric_field(self,obj):
        pass

    def move(self,surface,wrapper:bool, time=1/60):
        if wrapper: self.window_border_collision(surface, time)
        else: self.position += self.velocity*time*self.scale
        self.kinetic_energy = 0.5*self.mass*(self.velocity*self.velocity)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

    def window_border_collision(self, surface, time):       ###### COSTRAINT REACTION OF THE BORDER ######
        k_el = self.ELASTICITY if Object.bounce else 1
        x_vel, y_vel = self.velocity                        #take position coords where (0,0)
        x_res, y_res = self.position + self.velocity*time   #is top-left of the screen
        width, height = surface.get_size()
        offset_x, offset_y = self.radius, self.radius       #self.sprite.get_size()
        #offset_x /= 2                                      #as the vector originates at the center of the obj
        #offset_y /= 2                                      #this shift the collision to its edges
        width -= offset_x
        height -= offset_y
        
        if x_res <= offset_x:                               #in order: left, right, top, bottom (border checks)
            if x_res < offset_x:
                x_res = 2 * offset_x - x_res
                x_vel = -x_vel * self.ELASTICITY
                if -2 < x_vel < 2: x_res, x_vel = offset_x, 0
                if self.sound: self.boing.play()
        elif x_res >= width:                                ##########  the formula is composed by  ###########
            if x_res > width:
                x_res = 2 * width - x_res                   ## :: difference = resultant - offset_x          ##
                x_vel = -x_vel * self.ELASTICITY            ##  (how much of the res vect is off the screen) ##
                if -2 < x_vel < 2: x_res, x_vel = width, 0
                if self.sound: self.boing.play()
        if y_res <= offset_y:                               ## :: sub_vect = 2 * difference                  ##
            if y_res < offset_y:
                y_res = 2 * offset_y - y_res                ##  (double the previous difference)             ##
                y_vel = -y_vel * self.ELASTICITY            ## :: resultant - sub_vect                       ##
                if -2 < y_vel < 2: y_res, y_vel = offset_y, 0
                if self.sound: self.boing.play()
        elif y_res >= height:                               ##  (finds where the reflected vect points)      ##
            if y_res > height:
                y_res = 2 * height - y_res                  ###################################################
                y_vel = -y_vel * self.ELASTICITY
                if -2 < y_vel < 2: y_res, y_vel = height, 0
                if self.sound: self.boing.play()
        
        self.position, self.velocity = Vector2(x_res, y_res), Vector2(x_vel, y_vel)


class MainCharacter(Object):
    MANEUVERABILITY = 3
    ACCELERATION = 0.2

    def __init__(self, position):
        self.direction = Vector2(UP)
        self.sprite = smoothscale(
                load_sprite("main_character.png"),
                (int(1/5*position[0]), int(1/5*position[0]))
            )
        self.brum = load_sound('brum')
        self.enabled = True

        super().__init__(
            position,
            radius=0,
            mass=5
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