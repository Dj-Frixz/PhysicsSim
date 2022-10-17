import pygame
import numpy as np
from math import ceil
from random import shuffle
pygame.font.init()

from utils import load_sprite

class Settings:
    '''This is a class to create an interface for the settings'''

    FONT = pygame.font.SysFont('monospace',20)
    writing = False

    def __init__(self,screen,space_class):
        self.width,self.height = screen.get_width(),screen.get_height()
        self.top = space_class.main_character
        # self.pos = (int(0.927*self.width),int(0.0139*self.height))
        self.active = False
        self.img = load_sprite('settings.png') # self.FONT.render('"settings"',True,(255,255,255))
        self.rect = self.img.get_rect(topright=(self.width,0))
        self.pos = self.rect.topleft
        check = load_sprite('check.png')
        self.buttons = {
            'wrapper': Settings._Selection(load_sprite('wrapper.png'), check), #, space_class.toggle_wrapper),
            'static': Settings._Selection(load_sprite('pinned.png'), check),
            'clear': Settings._Button(load_sprite('clear.png'), space_class.clear),
            'reset': Settings._Button(load_sprite('reset.png'), space_class.reset),
            'funny': Settings._Selection(load_sprite('fun.png'), check),
            'trails': Settings._Selection(load_sprite('trails.png'), check),
            'info': Settings._Selection(load_sprite('info.png'), check),
            'bounce': Settings._Selection(load_sprite('bounce.png'), check, space_class.toggle_bounce, True),
            'sound': Settings._Selection(load_sprite('sound.png'), check, space_class.toggle_sound),
            'friction': Settings._Selection(load_sprite('friction.png'), check),
            'gravity': Settings._Selection(load_sprite('gravity.png'), check, space_class.toggle_gravity, True),
            'repulsion': Settings._Selection(load_sprite('repulsion.png'), check, space_class.toggle_repulsion, True)
#           'fullscreen': Settings._Button(self.FONT.render('fullscreeeen',True,(255,255,255)), lambda:pygame.display.toggle_fullscreen())
        }
        N = len(self.buttons)
        self.X = np.random.randint(1,8)
        self.Y = ceil(max(3,N/self.X))
        self.grid = np.full(self.X*self.Y, None)
        choices = [i for i in range(self.X*self.Y)]
        shuffle(choices)
        for i,butt in zip(choices,self.buttons):
            self.grid[i] = butt
            self.buttons[butt].position(np.round(
                (np.array( divmod(i,self.X) )+0.5) * [self.height/self.Y, self.width/self.X])
            )

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
    
    def assignment(var, value):
        var = value

    class __Interactive:
        '''Creates a generic interactive'''
        def __init__(self,base:pygame.Surface):
            self.sprite = base                                             # Surface of the button
            self.rect = None
            self.pos = (0,0)                                # top-left corner

        def position(self,pos:tuple):
            pos = (pos[1],pos[0])
            self.rect = self.sprite.get_rect(center=pos)
            self.pos = self.rect.topleft

        def draw(self,screen):
            screen.blit(self.sprite, self.pos)
    
    class _Selection(__Interactive):
        '''A simple on/off switch'''
        def __init__(self, base: pygame.Surface, check: pygame.Surface, action = None, status: bool = False):
            super().__init__(base)
            self.check = check                                          # Surface for the checkmark
            self.checkpos = (0,0)
            self.status = status                                        # checked/not
            self.action = action

        def position(self,pos:tuple):
            pos = (pos[1],pos[0])
            self.rect = self.sprite.get_rect(center=pos)
            self.pos = self.rect.topleft
            self.checkpos = self.check.get_rect(center=self.rect.center).topleft

        def select(self):
            Settings.writing = False
            self.status = self.status == False
            if self.action!=None:
                self.action()
        
        def draw(self,screen):
            screen.blit(self.sprite, self.pos)
            if self.status:
                screen.blit(self.check, self.checkpos)
    
    class _Button(__Interactive):
        '''A clickable button'''
        def __init__(self, base: pygame.Surface, action):
            super().__init__(base)
            self.action = action
        
        def select(self):
            Settings.writing = False
            self.action()

    class _TextInput(_Button):
        '''A text box'''
        def __init__(self, base: pygame.Surface, action, variable:int='write here'):
            super().__init__(base, self._on_click)
            self.FONT = Settings.FONT
            self.value = variable
        
        def _on_click(self):
            if not Settings.writing:
                self.sprite = self.FONT.render(str(self.value), True, (128,128,128), (0,0,0))
                Settings.writing = True

        def on_key_press(self, key) -> int:
            pass