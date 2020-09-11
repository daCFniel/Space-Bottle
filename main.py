import pygame
import scenes_and_characters
import functions
from sys import exit

# initialize the pygame
pygame.init()

# CONSTANT VARIABLES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 120


def start_game(fps, starting_scene):
    # set clock
    clock = pygame.time.Clock()

    # set frame itself, title and icon of the frame
    pygame.display.set_icon(functions.get_image('img/logo-32.png'))
    pygame.display.set_caption("Space Bottle")

    # set default volume
    pygame.mixer.music.set_volume(scenes_and_characters.music_volume / 100)
    for sound in scenes_and_characters.sounds:
        sound.set_volume(scenes_and_characters.sounds_volume / 100)

    # set active scene
    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()
        filtered_events = []

        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            if quit_attempt:
                active_scene.terminate()
            else:
                filtered_events.append(event)

        active_scene.event_handling(filtered_events)
        active_scene.render()
        active_scene.update(pressed_keys)

        active_scene = active_scene.next
        clock.tick(fps)

        pygame.display.update()


# make the frame stay until pressing quit
'''We put exit() after pygame.quit(), because pygame.quit() 
makes the system exit and exit() closes that window.'''
start_game(FPS, scenes_and_characters.MenuScene())
pygame.quit()
exit()

# Done
# Early development: fixed
# 1. Graphics
# 2. Audio
# 3. Better smoother ship's movement
# 5. Alien movement and destruction
# 6. Creating classes OOP
# 4. Bullet rect (hiding under the ship) and multiple bullets


# What to do: late development
# I. Intro
# II. Menu (credits, start, scoreboard)
# III. Option to restart the game
# IV. Advanced graphics (dynamic background)
# V. Authorised audio


# Pomysly od testerów
# mnoznik punktow, w zaleznosci od poziomów
# formacje alienów aka wzorki
# rozne rodzaje strzałow
# przyśpieszenie statku
# mozliwosc przyciszenia dzwieku

# suwak
# inne typy alienów
# liczenie czasu podczas gry
# ruszające się tło
# levele
# actual gameplay (trudnosc)

# Done
# podnoszenie pociskow
# Dodatkowe życie, aka pancerz
# nowy typ aliena + timer
# nieco zmienione tekstury (shield statek, nowy alien)
# trudnosc gry (speed alienow i collectable)
# umiejetnosc (op laser),
# intro (with transition)
# przechodzenie od lewej do prawej przez sciane
# poprawić hitboxy
# alieny na koniec fali zestrzelone dalej spadają
# nakładające sie na siebie alieny
# tekstury alienow nowych i za maly laser
# fpsy
# klasa sprite
# Pressing key done by keys = pygame.key.get_pressed()
# CONSTANT VARIABLES (get rid of magic numbers)
# Nowy sposób kolizji sprite.spritecollide
# Nowy sposób umierania i respawnu alienow oraz colleclablow
# mask collision system (pixel to pixel)
# laser
# scene menagement
# option menu
# player turbo with shift
# podzial na pliki
# option menu
# main menu
# option to restart the game
# odliczanie po wyjsciu z pauzy
# fullscreen mode
# nowy typ aliena
# endless mode difficulty
# new collectable - immunity
# sterowanie strzalkami
# controls settings - arrows/wsad
# topscore + saving
# ranks/exp + saving
# endless mode menu page
# ranks images and names
# menu and options improvments (back buttom)
# all settings are now saved to the file
# new controls for arrows control settings  (+new controls image)
# dwa nowe typy aliena
# ruszające się tło
# turbo animations
