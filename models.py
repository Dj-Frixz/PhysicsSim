from pickle import FALSE
from pygame.math import Vector2
from pygame.transform import scale,smoothscale, rotozoom

from utils import load_sprite, load_sound

UP = Vector2(0, -1)
#GRAVITY = {'direction': Vector2(0, 1), 'acceleration': 0.2}
OBJECTS = set()

class StaticObject:

    def __init__(self, position, sprite, mass=0) -> None:
        self.position = Vector2(position)
        self.mass = mass
        self.sprite = sprite
        self.radius = sprite.get_width() / 2

    def move(*args):
        pass

    def apply_forces(*args):
        pass

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

class Object(StaticObject):
    ELASTICITY = 0.9

    def __init__(self, position, sprite, mass=0, velocity=Vector2()):
        self.velocity = Vector2(velocity)
        self.boing = load_sound('boing.mp3')

        super().__init__(position, sprite, mass)

    def apply_forces(self, time=1/60):
        for obj in OBJECTS:
            direction = obj.position - self.position
            radius = direction.length()
            if radius!=0:
                force = direction.normalize()
                force *= obj.mass/(radius**2)
                self.velocity += force*time

    def move(self,surface,wrapper:bool):
        if wrapper: self.window_border_collision(surface)
        else: self.position += self.velocity

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

    def window_border_collision(self, surface):         ###### COSTRAINT REACTION OF THE BORDER ######
        x_vel, y_vel = self.velocity                    #take position coords where (0,0)
        x_res, y_res = self.position + self.velocity    #is top-left of the screen
        width, height = surface.get_size()
        offset_x, offset_y = self.sprite.get_size()
        offset_x /= 2                                   #as the vector originates at the center of the obj
        offset_y /= 2                                   #this shift the collision to its edges
        width -= offset_x
        height -= offset_y
        
        if x_res <= offset_x:                           #in order: left, right, top, bottom (border checks)
            x_res = 2 * offset_x - x_res
            x_vel = -x_vel * self.ELASTICITY            ###################################################
            if -2 < x_vel < 2: x_res, x_vel = offset_x, 0
            self.boing.play()
        elif x_res >= width:                            ##########  the formula is composed by  ###########
            x_res = 2 * width - x_res                   ## :: difference = resultant - offset_x          ##
            x_vel = -x_vel * self.ELASTICITY            ##  (how much of the res vect is off the screen) ##
            if -2 < x_vel < 2: x_res, x_vel = width, 0
            self.boing.play()
        if y_res <= offset_y:                           ## :: sub_vect = 2 * difference                  ##
            y_res = 2 * offset_y - y_res                ##  (double the previous difference)             ##
            y_vel = -y_vel * self.ELASTICITY            ## :: resultant - sub_vect                       ##
            if -2 < y_vel < 2: y_res, y_vel = offset_y, 0
            self.boing.play()
        elif y_res >= height:                           ##  (finds where the reflected vect points)      ##
            y_res = 2 * height - y_res                  ###################################################
            y_vel = -y_vel * self.ELASTICITY
            if -2 < y_vel < 2: y_res, y_vel = height, 0
            self.boing.play()
        
        self.position, self.velocity = Vector2(x_res, y_res), Vector2(x_vel, y_vel)


class MainCharacter(Object):
    MANEUVERABILITY = 3
    ACCELERATION = 0.3

    def __init__(self, position):
        self.direction = Vector2(UP)
        self.brum = load_sound('brum.wav')

        super().__init__(
            position,
            smoothscale(
                load_sprite("main_character.png"),
                (int(1/5*position[0]), int(1/5*position[0]))
            ),
            mass=5
        )
        OBJECTS.add(self)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        self.brum.play(fade_ms=1000)
    
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