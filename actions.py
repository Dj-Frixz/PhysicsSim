from models import *
from utils import load_sprite

def spawn(screen,pos,movable,fun):
    SPHERE = load_sprite("enemy.png")
    ENEMY = load_sprite("sphere.svg")
    diameter = screen/10
    sprite = scale(SPHERE,(diameter,diameter)) if fun else smoothscale(ENEMY,(diameter,diameter))
    if movable:
        OBJECTS.add(
            Object(
                position = pos,
                sprite = sprite,
                mass = 2000)
            )
    else:
        OBJECTS.add(
            StaticObject(
                position = pos,
                sprite = sprite,
                mass = 2000)
            )

def settings(screen):
    square = load_sprite('square.png')
    screen.blit(square,(1900,1000))