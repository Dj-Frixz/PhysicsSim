import pygame
pygame.font.init()

from utils import load_sprite
from models import OBJECTS

class Settings:
    width = 0
    height = 0
    FONT = pygame.font.SysFont('monospace',20)

    def __init__(self,screen):
        Settings.width,Settings.height = screen.get_width(),screen.get_height()
        self.pos = (int(0.927*self.width),int(0.0139*self.height))
        self.active = False
        self.img = self.FONT.render('"settings"',True,(255,255,255))
        self.rect = self.img.get_rect(topleft=self.pos)
        check = load_sprite('check.png')
        self.buttons = {
            'wrapper': Settings._Selection(self.FONT.render('wrapper',True,(255,255,255)), check, (0,964,0.926)),
            'movement': Settings._Selection(self.FONT.render('movement',True,(255,255,255)), check, (0.521,0.926)),
            'clear': Settings._Button(self.FONT.render('clear',True,(255,255,255)), (0.052,0.926), OBJECTS.clear),
            'funny': Settings._Selection(self.FONT.render('fun',True,(255,255,255)), check, (0.521,0.463)),
            'megafun': Settings._Selection(self.FONT.render('megafun',True,(255,255,255)), check, (0.26,0.463)),
            'info': Settings._Selection(self.FONT.render('info',True,(255,255,255)), check, (0.74,0.463))
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
            pos = (int(pos[0]*Settings.width),int(pos[1]*Settings.height))
            self.rect = base.get_rect(center=pos)
            self.pos = self.rect.topleft                                # top-left corner

        def draw(self,screen):
            screen.blit(self.box, self.pos)
    
    class _Selection(__Interactive):
        def __init__(self, base: pygame.Surface, check: pygame.Surface, pos: tuple, status: bool = False):
            super().__init__(base, pos)
            self.check = check                                          # Surface for the checkmark
            self.checkpos = check.get_rect(center=self.rect.center).topleft
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