from pygame.image import load
from pygame.mixer import Sound
from os.path import abspath,join
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)

def load_sprite(name, with_alpha=True, folder='sprites'):
    path = resource_path(f"assets\{folder}\{name}")
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def load_sound(name, ext='mp3'):
    path = resource_path(f"assets\sounds\{name}.{ext}")
    return Sound(path)
