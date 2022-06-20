import pygame
pygame.font.init()

from utils import load_sprite
from models import OBJECTS

class Settings:
    FONT = pygame.font.SysFont('monospace',20)

    def __init__(self):
        self.pos = (1780,15)
        self.active = False
        self.img = self.FONT.render('"settings"',True,(255,255,255))
        self.rect = self.img.get_rect(topleft=self.pos)
        check = load_sprite('check.png')
        self.buttons = {
            'wrapper': Settings._Selection(self.FONT.render('wrapper',True,(255,255,255)), check, (1850,1000)),
            'movement': Settings._Selection(self.FONT.render('movement',True,(255,255,255)), check, (1000,1000)),
            'clear': Settings._Button(self.FONT.render('clear',True,(255,255,255)), (100,1000), OBJECTS.clear),
            'funny': Settings._Selection(self.FONT.render('fun',True,(255,255,255)), check, (1000,500))
        }
    
    def handle_input(self,click_pos):
        if self.rect.collidepoint(click_pos):  #left=1780,top=15
            self.active = self.active == False
        elif self.active:
            for butt in self.buttons:
                if self.buttons[butt].rect.collidepoint(click_pos):
                    self.buttons[butt].select()
                    return

    def draw(self,screen):
        screen.blit(self.img, self.pos)
        if self.active:
            for butt in self.buttons:
                self.buttons[butt].draw(screen)

    class __Interactive:
        '''Creates an interactive'''

        def __init__(self,base:pygame.Surface,pos:tuple):
            self.box = base                                             # Surface of the button
            self.rect = base.get_rect(center=pos)
            self.pos = self.rect.topleft                                # top-left corner

        def draw(self,screen):
            screen.blit(self.box, self.pos)
    
    class _Selection(__Interactive):
        def __init__(self, base: pygame.Surface, check: pygame.Surface, pos: tuple, status: bool = False):
            super().__init__(base, pos)
            self.check = check                                          # Surface for the checkmark
            self.checkpos = check.get_rect(center=pos).topleft
            self.status = status                                        # checked/not
        
        def select(self):
            self.status = self.status == False
        
        def draw(self,screen):
            screen.blit(self.box, self.pos)
            if self.status:
                screen.blit(self.check, self.checkpos)
    
    class _Button(__Interactive):
        def __init__(self, base: pygame.Surface, pos: tuple, action):
            super().__init__(base, pos)
            self.action = action
        
        def select(self):
            self.action()