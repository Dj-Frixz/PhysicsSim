import pygame
from sys import exit

from models import MainCharacter
from actions import *
from utils import load_sprite
from settings import Settings

class SpaceRocks:
    def __init__(self):
        self.screen = self._init_pygame()
        self.screen_width, self.screen_height = pygame.display.get_window_size()
        pygame.display.set_icon( load_sprite("icon.ico", False))
        self.background = load_sprite("space.jpg", False)
        font = pygame.font.SysFont('monospace',20)
        self.mex = font.render("v2.1",True,(255,255,255))
        self.mexpos = (0,0)
        self.clock = pygame.time.Clock()
        self.main_character = MainCharacter((int(self.screen_width / 2), int(self.screen_height / 2)))
        self.settings = Settings()

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic_()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("BRUH")
        return pygame.display.set_mode(flags=pygame.FULLSCREEN)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    spawn(self.screen_height,event.pos,self.settings.buttons['movement'].status,self.settings.buttons['funny'].status)
                elif event.button == 1:
                    self.settings.handle_input(event.pos)

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
            obj.move(self.screen,self.settings.buttons['wrapper'].status)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.mex,self.mexpos)
        self.settings.draw(self.screen)

        for obj in OBJECTS:
            obj.draw(self.screen)
        
        pygame.display.flip()
        self.clock.tick(60)
