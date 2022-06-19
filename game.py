import pygame
from sys import exit

from models import MainCharacter
from actions import *
from utils import load_sprite

SETTINGS = False

class SpaceRocks:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.screen_width, self.screen_height = pygame.display.get_window_size()
        pygame.display.toggle_fullscreen()
        pygame.display.set_icon( load_sprite("icon.ico", False))
        self.background = load_sprite("space.jpg", False)
        font = pygame.font.SysFont('monospace',20)
        self.mex = font.render("v2.0",True,(255,255,255))
        self.mexpos = (0,0)#self.screen.get_width()-font.size('')[0]*2,1000)
        self.clock = pygame.time.Clock()
        self.main_character = MainCharacter((int(self.screen_width / 2), int(self.screen_height / 2)))
        #self.settings = pygame.transform.smoothscale(load_sprite('settings.png'),(60,60))
        self.settings = font.render('"settings"',True,(255,255,255))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic_()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("BRUH")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    spawn(self.screen_height,event.pos)
                elif event.button == 1 and self.settings.get_rect(left=1780,top=15).collidepoint(event.pos):
                    global SETTINGS
                    SETTINGS = SETTINGS == False

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT] and not is_key_pressed[pygame.K_LEFT]:
            self.main_character.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT] and not is_key_pressed[pygame.K_RIGHT]:
            self.main_character.rotate(clockwise=False)
        if is_key_pressed[pygame.K_UP]:
            self.main_character.accelerate()

    def _process_game_logic_(self):
        limit = pygame.Vector2(2*self.screen_height,2*self.screen_width).length()
        escaped = set()
        for obj in OBJECTS:
            if obj.position.length()>limit:
                escaped.add(obj)
            else:
                obj.apply_forces()
        OBJECTS.difference_update(escaped)
        for obj in OBJECTS:
            obj.move(self.screen)
        print(OBJECTS)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.mex,self.mexpos)

        for obj in OBJECTS:
            obj.draw(self.screen)
        
        self.screen.blit(self.settings, (1780,15))
        if SETTINGS:
            settings(self.screen)
        
        pygame.display.flip()
        self.clock.tick(60)
