import pygame
import os

pygame.mixer.init()
pygame.font.init()

image_library = {}


def get_image(path):
    global image_library
    image = image_library.get(path)
    if image is None:
        safe_path = path.replace('/', os.sep).replace('\\', os.sep).lower()
        image = pygame.image.load(safe_path)
        image_library[path] = image
    return image


# Audio: soundtrack and sound effects
def get_sound(path):
    safe_path = path.replace('/', os.sep).replace('\\', os.sep).lower()
    sound = pygame.mixer.Sound(safe_path)
    return sound


def load_music(path):

    safe_path = path.replace('/', os.sep).replace('\\', os.sep).lower()
    pygame.mixer.music.load(safe_path)


def get_font(path, size):
    safe_path = path.replace('/', os.sep).replace('\\', os.sep).lower()
    font = pygame.font.Font(safe_path, size)
    return font


def get_current_time():
    return int((pygame.time.get_ticks()) / 1000)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
