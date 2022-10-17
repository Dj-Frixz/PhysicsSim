from math import sqrt
import sys
sys.path.append('lib')
import pygame

from models import *
from utils import load_sprite
from settings import Settings

class Space:
    def __init__(self):
        self.screen = self._init_pygame()
        self.screen_width, self.screen_height = pygame.display.get_window_size()
        StaticObject.scale = self.screen_height/1080
        pygame.display.set_icon( load_sprite("icon.ico", False))
        self.background = load_sprite("space.jpg", False)
        self.FONT = pygame.font.SysFont('monospace',int(20*(self.screen_height/1080)))
        self.version = self.FONT.render("v2.1",True,(255,255,255))
        self.hint = self.FONT.render("Right click to spawn something, scroll to change mass. Use the arrows to move the spaceship.",True,(255,255,255))
        self.clock = pygame.time.Clock()
        self.main_character = MainCharacter((int(self.screen_width/2), int(self.screen_height/2)))
        self.last = self.main_character
        self.count = 1
        self.selected_mass = 2000
        self.settings = Settings(self.screen, self)
        self.SPHERE = load_sprite("sphere.png")
#       self.ENEMY = load_sprite("enemy.png")

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic_()
            self._draw()
    
    def _init_pygame(self):
        '''Initialization of the Pygame module'''
        pygame.init()
        pygame.display.set_caption("PhysicsSim")
        return pygame.display.set_mode(flags= pygame.FULLSCREEN)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3: # right click
                    self.spawn(event.pos,self.settings.buttons['movement'].status) # ,self.settings.buttons['funny'].status)
                elif event.button == 1: # left click
                    self.settings.handle_input(event.pos)
            if event.type == pygame.MOUSEWHEEL:
                self.change_mass(event.y)

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT] and not is_key_pressed[pygame.K_LEFT]:
            self.main_character.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT] and not is_key_pressed[pygame.K_RIGHT]:
            self.main_character.rotate(clockwise=False)
        if is_key_pressed[pygame.K_UP]:
            self.main_character.accelerate()

    def _process_game_logic_(self):
        limit = pygame.Vector2(2*self.screen_height,2*self.screen_width).length()
        if self.main_character.enabled and self.main_character.position.length()<limit:
            self.main_character.apply_forces()
        else:
            self.main_character.enabled = False
        obj = self.main_character
        while obj.next is not None:
            if obj.next.position.length()>limit:
                self._delete_next(obj)
                if obj.next is None: break
            else:
                obj.next.apply_forces()
            obj = obj.next
        # if self.settings.buttons['sound'].status
        
        obj = self.main_character if self.main_character.enabled else self.main_character.next
        while obj is not None:
            obj.move(self.screen,self.settings.buttons['wrapper'].status)
            obj = obj.next

    def _draw(self):
        '''Displays the objects on the screen'''
        if not self.settings.buttons['trails'].status:
            self.screen.blit(self.background, (0,0))
        self.screen.blit(self.version, (0,0))
        self.screen.blit(self.hint, (0.26*self.screen_width,0.93*self.screen_height))
        self.settings.draw(self.screen)
        if self.settings.buttons['info'].status:
            self.screen.blit(
                self.FONT.render(f'particles: {self.count}, res: {self.screen_width,self.screen_height}',True,(255,255,255)),
                (0, 0.19*self.screen_height))
        self.screen.blit(
            self.FONT.render('mass: %i'%(self.selected_mass),True,(255,255,255)), 
            (0.7*self.screen_width,0.04*self.screen_height)
        )

        obj = self.main_character if self.main_character.enabled else self.main_character.next
        while obj is not None:
            obj.draw(self.screen)
            # TESTING STUFF
            # obj.rect.center=obj.position
            # pygame.draw.rect(self.screen, (255,255,255), obj.rect, 1)
            obj = obj.next
        
        pygame.display.flip()
        self.clock.tick(60)

    def _delete_next(self,obj):
        obj.next = obj.next.next
        if obj.next is None:
            self.last = obj
        self.count -= 1

    def spawn(self,pos,movable): # ,fun):
        '''Spawns a single particle'''
        # diameter = self.screen_height/10
        sprite =  self.SPHERE # if not fun else pygame.transform.smoothscale(self.ENEMY,(diameter,diameter))
        Obj = Object if movable else StaticObject
        self.last.next = Obj(
            position = pos,
            radius = sqrt(self.selected_mass/100),
            mass = self.selected_mass)
        self.last = self.last.next
        self.count += 1

    def change_mass(self, value:int|float):
        self.selected_mass += (value**5)*100
        if self.selected_mass < 0: self.selected_mass = 0

    def toggle_sound(self):
        '''Switch sound on/off'''
        Object.sound = Object.sound == False

    def clear(self):
        '''Clears every object on the screen'''
        self.main_character.next = None
        self.main_character.enabled = False
        self.last = self.main_character
        self.count = 0
    
    def reset(self):
        '''Resets to the starting position'''
        self.main_character.next = None
        self.main_character.position = Vector2(int(self.screen_width/2), int(self.screen_height/2))
        self.main_character.velocity = Vector2(0,0)
        self.main_character.direction = Vector2(0,-1)
        self.main_character.enabled = True
        self.last = self.main_character
        self.count = 1
