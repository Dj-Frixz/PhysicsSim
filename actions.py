from models import *
from utils import load_sprite
from pygame import display

def spawn(screen,pos):
    diameter = screen/10
    OBJECTS.add(
        Object(
            position = pos,
            sprite = scale(load_sprite("sphere.svg"),(diameter,diameter)),
            mass = 2000)
        )

def wrap():
    WRAPPER = WRAPPER and FALSE

def settings(screen):
    square = load_sprite('square.png')
    screen.blit(square,(1900,1000))