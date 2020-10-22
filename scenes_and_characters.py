import pygame
import math
import functions
import random
import gui_elements

# CONSTANT VARIABLES
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (70, 70, 70)
ORANGE = (255, 117, 26)
BLUE = (54, 191, 191)
OCEAN = (58, 127, 160)
PURPLE = (24, 32, 43)
TOMATO = (255, 99, 71)
GOLD = (255, 215, 0)
DARKBLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)

# Global variables
frame = pygame.display.set_mode((WIDTH, HEIGHT))
frame_rect = frame.get_rect()
current_score = 0
current_coins = 0
map_score = 0
alien_default_speed = 3
immunity_time = 10
angry_mode_time = 10
weapon_damaged_time = 15
pause_time = 3

# audio
bullet_sound = functions.get_sound('audio/bullet.wav')
explosion_sound = functions.get_sound('audio/explosion.wav')
shield_broke_sound = functions.get_sound('audio/shield_broke.wav')
laser_beam_sound = functions.get_sound('audio/laser_beam.wav')
cow_sound = functions.get_sound('audio/cow.wav')
fail_sound = functions.get_sound('audio/fail.wav')
promotion_sound = functions.get_sound('audio/promotion.wav')
top_score_sound = functions.get_sound('audio/top_score.wav')
promotion_and_score_sound = functions.get_sound('audio/promotion_and_score.wav')
menu_sound = functions.get_sound('audio/entering_menu.wav')
accept_sound = functions.get_sound('audio/accept.wav')
big_explosion_sound = functions.get_sound('audio/big_explosion.wav')
collectable_collection_sound = functions.get_sound('audio/score.wav')
shield_collection_sound = functions.get_sound('audio/shield.wav')
immunity_collection_sound = functions.get_sound('audio/immunity.wav')
angry_mode_collection_sound = functions.get_sound('audio/angry_mode.wav')
weapon_damaged_collection_sound = functions.get_sound('audio/weapon_damaged.wav')
coin_collection_sound = functions.get_sound('audio/coin.wav')
laser_collection_sound = functions.get_sound('audio/laser.wav')
purchase_sound = functions.get_sound('audio/purchase.wav')
sounds = [bullet_sound, explosion_sound, shield_broke_sound, collectable_collection_sound, laser_beam_sound, cow_sound,
          fail_sound, promotion_sound, top_score_sound, promotion_and_score_sound, menu_sound, accept_sound,
          big_explosion_sound, shield_collection_sound, immunity_collection_sound, laser_collection_sound,
          angry_mode_collection_sound, weapon_damaged_collection_sound, coin_collection_sound, purchase_sound]

#  open file responsible for storing the progress
#  and load the data

with open('fonts/font_size.txt', 'r') as file:  # with-as is like try .. finally block
    # read a list of lines into data
    data = file.readlines()

# current rank
current_rank = int(data[0])
# current top score
top_score = int(data[1])
# current experience
current_exp = int(data[2])
# current controls
current_controls = int(data[3])  # Integer 0 or 1 where 0 - wsad; 1 - arrows
# current music volume
music_volume = int(data[4])  # default value 50
# current sound volume
sounds_volume = int(data[5])  # default value 40
# current display mode
display_mode = int(data[6])  # Integer 0 or 1 where 0 - window; 1 - fullscreen
# total current coins
total_coins = int(data[7])
# skins owned
skins_owned = [int(x) for x in data[8]]  # list comprehension

# exp required for next promotion based on current rank (math module used to make the numbers nonlinear)
exp_required_total = int(999 * math.sqrt(math.pow(2, current_rank)))

# set controls
if current_controls == 0:
    controls = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE,
                pygame.K_c, pygame.K_LSHIFT]  # default controls W A S D
else:
    controls = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_x, pygame.K_c, pygame.K_z]

# set display mode
if display_mode == 1:
    frame = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


# super class
class Character(pygame.sprite.Sprite):

    # constructor
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.rect = self.image[0].get_rect(topleft=(x, y))
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image[0])
        self.radius = 15 * self.rect.width / 32


# sub classes
class Player(Character):

    # constructor
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)
        self.has_shield = False
        self.has_laser = False
        self.is_immune = False
        self.weapon_damaged = False
        self.num_of_bullets = 3
        self.num_of_shields = 0
        self.images = []
        self.images.append(self.image[0])
        self.images.append(functions.get_image('img/spaceship_l2.png').convert_alpha())
        self.images.append(functions.get_image('img/spaceship_r2.png').convert_alpha())
        self.images.append(functions.get_image('img/shielded_spaceship.png').convert_alpha())
        self.images.append(functions.get_image('img/shielded_spaceship_l2.png').convert_alpha())
        self.images.append(functions.get_image('img/shielded_spaceship_r2.png').convert_alpha())
        self.images.append(functions.get_image('img/jet.png').convert_alpha())
        self.images.append(functions.get_image('img/immune_small.png').convert_alpha())
        self.images.append(functions.get_image('img/jet_left.png').convert_alpha())
        self.images.append(functions.get_image('img/jet_right.png').convert_alpha())
        self.images.append(functions.get_image('img/parachute.png').convert_alpha())
        self.images.append(functions.get_image('img/wind.png').convert_alpha())
        self.images.append(functions.get_image('img/wind2.png').convert_alpha())

    def check_boundaries(self):
        if self.rect.left < -self.rect.width / 2:  # check if character hits the boundaries
            self.rect.right = WIDTH + self.rect.width / 2  # left-right wall tp
        elif self.rect.right > WIDTH + self.rect.width / 2:
            self.rect.left = -self.rect.width / 2
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    # methods
    def draw(self, key):
        if key[controls[1]] and key[controls[3]] and (key[controls[0]] or key[controls[2]]):
            frame.blit(self.images[0], self.rect)  # when player presses all the buttons at once
        else:
            if key[controls[1]]:
                if self.has_shield:
                    frame.blit(self.images[4], self.rect)
                else:
                    frame.blit(self.images[1], self.rect)
            elif key[controls[3]]:
                if self.has_shield:
                    frame.blit(self.images[5], self.rect)
                else:
                    frame.blit(self.images[2], self.rect)
            else:
                if self.has_shield:
                    frame.blit(self.images[3], self.rect)
                else:
                    frame.blit(self.images[0], self.rect)
            # show that player is immune
        if self.is_immune:
            frame.blit(self.images[7], (self.rect.centerx - 12, self.rect.bottom))

    def update(self, key):
        shift_pressed = key[controls[6]] or key[pygame.K_RSHIFT]
        if key[controls[0]]:  # forward
            if shift_pressed:
                self.rect.move_ip(0, -self.speed)
                if not key[controls[1]] and not key[controls[3]] and not key[controls[2]]:
                    frame.blit(self.images[6], self.rect.bottomleft)
                    frame.blit(self.images[6], self.rect.midbottom)
                elif key[controls[1]] and not key[controls[3]] and not key[controls[2]]:
                    frame.blit(self.images[8], (self.rect.centerx + 3, self.rect.centery + 20))
                elif key[controls[3]] and not key[controls[1]] and not key[controls[2]]:
                    frame.blit(self.images[9], (self.rect.centerx - 35, self.rect.centery + 19))
            else:
                self.rect.move_ip(0, -self.speed + 1)
        if key[controls[2]]:  # back
            if shift_pressed:
                self.rect.move_ip(0, self.speed)
                if not key[controls[0]]:
                    frame.blit(self.images[10], (self.rect.left, self.rect.bottom - 20))
            else:
                self.rect.move_ip(0, self.speed - 1)
        if key[controls[1]]:  # left
            if shift_pressed:
                self.rect.move_ip(-self.speed, 0)
                if not key[controls[3]] and not key[controls[0]] and not key[controls[2]]:
                    frame.blit(self.images[11], (self.rect.centerx + 15, self.rect.centery - 20))
            else:
                self.rect.move_ip(-self.speed + 1, 0)
        if key[controls[3]]:  # right
            if shift_pressed:
                self.rect.move_ip(self.speed, 0)
                if not key[controls[1]] and not key[controls[0]] and not key[controls[2]]:
                    frame.blit(self.images[12], (self.rect.centerx - 50, self.rect.centery - 20))
            else:
                self.rect.move_ip(self.speed - 1, 0)


class Alien(Character):
    shared_speed = alien_default_speed  # speed of all the aliens
    angry_mode = False  # if this is true all aliens move faster

    # constructor
    def __init__(self, image, x, y, speed, health):
        super().__init__(image, x, y, speed)
        self.level = 1
        self.health = health
        self.animation_count = 0
        self.drop_chance = 1

    # methods
    def draw(self):
        frame.blit(self.image[0], self.rect)

    def update(self):
        if Alien.angry_mode:
            self.rect.move_ip(0, Alien.shared_speed)  # move faster
        else:
            self.rect.move_ip(0, self.speed)
        # check if alien's health reaches 0, if so - kill it
        if self.health == 0:
            # galactic dust animation upon death
            # animation speed - x(here 4) * number of images (here 4) + x(here 4) = 20
            # too speed up animation make x lower, to slow down animation, make x larger
            self.image[0] = self.image[self.animation_count // 4]
            if self.animation_count + 1 < 20:
                self.animation_count += 1
            else:
                self.drop_collectable(self.drop_chance)
                self.kill()

    def action(self):
        pass

    def check_boundaries(self):
        if self.rect.top > HEIGHT:
            self.kill()
            global current_score, map_score
            current_score += 1
            map_score += 1

    # Param drop_chance: chance (0-100%) that alien will drop collectable upon death
    def drop_collectable(self, drop_chance):
        collectable_drop = random.randint(0, 100)
        if collectable_drop <= drop_chance:
            collectable_type_drop = random.randint(0, 100)
            position_fix = 15  # so the collectable appears in the middle of destroyed alien
            if self.level == 4:  # for big alien
                position_fix = 110
            if collectable_type_drop <= 55:  # 55% chance that dropped collectable will be ammo
                GameScene.collectables.add(Collectable([functions.get_image('img/bullet2.png').convert_alpha()],
                                                       self.rect.x + position_fix,
                                                       self.rect.y, 2, "ammo"))
            elif 55 < collectable_type_drop <= 65:  # 10% chance that dropped collectable will be shield
                GameScene.collectables.add(
                    Collectable([functions.get_image('img/shield.png').convert_alpha()],
                                self.rect.x + position_fix,
                                self.rect.y, 2, "shield"))
            elif 65 < collectable_type_drop <= 75:  # 10% chance that dropped collectable will be laser
                GameScene.collectables.add(
                    Collectable([functions.get_image('img/laser_gun.png').convert_alpha()],
                                self.rect.x + position_fix,
                                self.rect.y, 2, "laser"))
            elif 75 < collectable_type_drop <= 85:  # 10% chance that dropped collectable will be immunity
                GameScene.collectables.add(
                    Collectable([functions.get_image('img/immune.png').convert_alpha()],
                                self.rect.x + position_fix,
                                self.rect.y, 2, "immunity"))
            elif 85 < collectable_type_drop <= 95:  # 9% chance that dropped collectable will be angry mode
                GameScene.collectables.add(
                    Collectable([functions.get_image('img/angry_mode.png').convert_alpha()],
                                self.rect.x + position_fix,
                                self.rect.y, 2, "angry_mode"))
            elif 95 < collectable_type_drop <= 100:  # 5% chance that dropped collectable will be coin
                GameScene.collectables.add(
                    Collectable([functions.get_image('img/coin0.png').convert_alpha(),
                                 functions.get_image('img/coin1.png').convert_alpha(),
                                 functions.get_image('img/coin2.png').convert_alpha(),
                                 functions.get_image('img/coin3.png').convert_alpha(),
                                 functions.get_image('img/coin4.png').convert_alpha(),
                                 functions.get_image('img/coin5.png').convert_alpha(),
                                 functions.get_image('img/coin6.png').convert_alpha(),
                                 functions.get_image('img/coin7.png').convert_alpha()],
                                self.rect.x + position_fix,
                                self.rect.y, 1, "coin"))


class AlienLevel2(Alien):
    def __init__(self, image, x, y, speed, health):
        super().__init__(image, x, y, speed, health)
        self.level = 2
        self.drop_chance = 30


class AlienLevel3(Alien):
    def __init__(self, image, x, y, speed, health):
        super().__init__(image, x, y, speed, health)
        self.level = 3
        self.drop_chance = 60

    def draw(self):
        if self.health == 1:
            self.image[0] = self.image[1]
        frame.blit(self.image[0], self.rect)

    def update(self):
        if Alien.angry_mode:
            self.rect.move_ip(Alien.shared_speed, 1)  # move faster
        else:
            self.rect.move_ip(self.speed, 1)
        # check if alien's health reaches 0, if so - kill it
        if self.health == 0:
            self.image[0] = self.image[(self.animation_count // 5) + 1]
            if self.animation_count + 1 < 25:
                self.animation_count += 1
            else:
                self.drop_collectable(self.drop_chance)
                self.kill()

    def action(self):
        if random.randint(0, 200) == 0:
            GameScene.enemy_bullets.add(
                BulletEnemy([functions.get_image('img/bullet3.png').convert_alpha()], self.rect.x, self.rect.y, 4))

    def check_boundaries(self):
        if self.rect.left <= 0 or self.rect.right >= WIDTH:  # check if character hits the boundaries
            self.speed *= -1
        if self.rect.top > HEIGHT:
            self.kill()
            global current_score, map_score
            current_score += 1
            map_score += 1


class AlienLevel4(Alien):
    def __init__(self, image, x, y, speed, health):
        super().__init__(image, x, y, speed, health)
        self.level = 4
        self.drop_chance = 90

    def draw(self):
        if self.health == 2:
            self.image[0] = self.image[2]
        if self.health == 1:
            self.image[0] = self.image[1]
        frame.blit(self.image[0], self.rect)

    def update(self):
        if Alien.angry_mode:
            self.rect.move_ip(0, Alien.shared_speed)  # move faster
        else:
            self.rect.move_ip(0, self.speed)
        # check if alien's health reaches 0, if so - kill it
        if self.health == 0:
            self.image[0] = self.image[(self.animation_count // 8) + 2]
            # explosion animation upon death
            big_explosion_sound.play()
            if self.animation_count + 1 < 56:
                self.animation_count += 1
            else:  #
                self.drop_collectable(self.drop_chance)
                self.kill()
                GameScene.aliens.empty()


class Bullet(Character):

    # constructor
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)

    # methods
    def draw(self):
        frame.blit(self.image[0], self.rect)

    def update(self):
        self.rect.move_ip(0, -self.speed)

    def check_boundaries(self):
        if self.rect.bottom < 0:
            self.kill()


class BulletEnemy(Bullet):

    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)

    def update(self):
        self.rect.move_ip(0, self.speed)

    def check_boundaries(self):
        if self.rect.top > HEIGHT:
            self.kill()


class Laser(Character):

    # constructor
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)
        self.state = "loaded"

    # methods
    def draw(self):
        self.state = "moving"
        frame.blit(self.image[0], (self.rect.x, self.rect.y))

    def update(self):
        # get the coordinates of the player's ship and fix
        GameScene.laser.rect.x = GameScene.player.rect.x - 220
        GameScene.laser.rect.y = GameScene.player.rect.y - 460


class Collectable(Character):

    # constructor
    def __init__(self, image, x, y, speed, category):
        super().__init__(image, x, y, speed)
        self.category = category
        self.animation_count = 0

    # methods
    def draw(self):
        frame.blit(self.image[0], self.rect)

    def update(self):
        self.rect.move_ip(0, self.speed)  # collectables have same speed as aliens
        # coin animation
        if self.category == "coin":
            self.image[0] = self.image[(self.animation_count // 8)]
            if self.animation_count + 1 < 64:
                self.animation_count += 1
            else:
                self.animation_count = 0

    def check_boundaries(self):
        if self.rect.top > HEIGHT:
            self.kill()


class Skin:
    def __init__(self, image, name, cost):
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.cost = cost


class Scene:
    def __init__(self):
        self.next = self

    def event_handling(self, events):
        raise NotImplementedError

    def update(self, pressed_keys):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def switch_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)


class GameScene(Scene):
    # score
    score_label_x = 10
    score_label_y = 10

    # fonts
    game_over_font = functions.get_font('fonts/Space_Galaxy.ttf', 90)
    score_font = functions.get_font('fonts/Space_Galaxy.ttf', 26)
    counter_font = functions.get_font('fonts/Space_Galaxy.ttf', 140)

    # OBJECTS
    # player object
    player_sprite = pygame.sprite.Group()
    player = Player([functions.get_image('img/spaceship.png').convert_alpha()], 370, 480, 3)
    player_sprite.add(player)

    # alien objects groups
    aliens = pygame.sprite.Group()

    # bullet objects
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    bullets_label_x = 705
    bullets_label_y = 10

    # laser object
    laser = Laser([functions.get_image('img/laser_beam.png').convert_alpha()], 370, 480, 0)

    # collectable objects
    collectables = pygame.sprite.Group()

    # events
    COLLECTABLE_WEAPON_DAMAGED = pygame.USEREVENT - 4
    COLLECTABLE_ANGRY_RESPAWN = pygame.USEREVENT - 3
    ALIEN_LVL4_RESPAWN = pygame.USEREVENT - 2
    COLLECTABLE_IMMUNITY_RESPAWN = pygame.USEREVENT - 1
    ALIEN_LVL1_RESPAWN = pygame.USEREVENT
    COLLECTABLE_LASER_RESPAWN = pygame.USEREVENT + 1
    COLLECTABLE_SHIELD_RESPAWN = pygame.USEREVENT + 2
    COLLECTABLE_AMMO_RESPAWN = pygame.USEREVENT + 3
    ALIEN_LVL3_RESPAWN = pygame.USEREVENT + 4
    ALIEN_LVL1_STOP = pygame.USEREVENT + 5
    ALIEN_LVL2_RESPAWN = pygame.USEREVENT + 6
    ALIEN_LVL2_STOP = pygame.USEREVENT + 7
    # active the game and alien phase, set start time, initialise cheats
    game_is_active = True
    pause = False
    is_alien_phase = True
    start_time = None  # start time used for laser and pause after quiting the options
    start_time_immunity = None  # start time used for immunity bonus
    start_time_angry_mode = None  # start time used for agry mode debuff
    start_time_weapon_damaged = None  # start time used for weapon damaged debuff
    cheats_on = False  # ammo bonus easter egg code code cheat]]

    def __init__(self):
        super().__init__()
        self.background = functions.get_image('img/background1.png').convert()  # default background player starts with
        # list of other backgrounds,
        # background changes through the game
        self.backgrounds = [functions.get_image('img/background2.png').convert(),
                            functions.get_image('img/background3.png').convert(),
                            functions.get_image('img/background4.png').convert(),
                            functions.get_image('img/background5.png').convert(),
                            functions.get_image('img/background6.png').convert(),
                            functions.get_image('img/background7.png').convert()]
        self.bg_y = 0
        self.bg_transparency = 0

        self.current_bg = None  # makes the bg change possible (doesn't include first, default bg)
        self.previous_background = None  # saves the last bg so it allows new bg to appear smoothly
        self.current_bg_index = -1  # determines which gb is currently displayed, goes up every x points
        self.switch_background = True  # flag that allows to change backgrounds

        for i in range(len(self.backgrounds)):  # iterate over all backgrounds and change their transparency to 0
            self.backgrounds[i].set_alpha(0)

    def change_background(self):
        global map_score
        if map_score >= 200:  # every 200 points(score) background changes to a random one
            # allow to change background once and prevent from going out of index
            if self.switch_background is True and self.current_bg_index < len(self.backgrounds) - 1:
                if self.current_bg is not None:
                    self.previous_background = self.current_bg
                self.current_bg_index += 1
                self.current_bg = self.backgrounds[self.current_bg_index]
                self.switch_background = False
                self.bg_transparency = 0
            if self.bg_transparency < 255:
                self.bg_transparency += 0.1
            self.current_bg.set_alpha(self.bg_transparency)
            if self.bg_transparency >= 255:
                map_score = 0  # reset map score
                self.switch_background = True

    def event_handling(self, events):
        if not GameScene.pause:
            if GameScene.game_is_active:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0:
                            # ammo bonus easter egg code code cheat
                            GameScene.cheats_on = True
                        elif event.key == pygame.K_9:
                            # laser bonus easter egg code code cheat
                            GameScene.player.has_laser = True
                        elif event.key == pygame.K_8:
                            # shield bonus easter egg code code cheat
                            GameScene.player.has_shield = True
                            if GameScene.player.num_of_shields < 4:
                                GameScene.player.num_of_shields += 1
                        elif event.key == pygame.K_7:
                            # immunity bonus easter egg code cheat
                            GameScene.start_time_immunity = functions.get_current_time() + 50
                            GameScene.player.is_immune = True
                        elif event.key == controls[4]:  # shoot bullet
                            if GameScene.player.num_of_bullets > 0 and GameScene.player.weapon_damaged is False:
                                GameScene.player.num_of_bullets -= 1
                                bullet_sound.play()  # shooting sound effect
                                # fix position by 16 pixels so bullet appears in the middle of spaceship
                                GameScene.bullets.add(
                                    Bullet([functions.get_image('img/bullet.png').convert_alpha()],
                                           GameScene.player.rect.x + 16,
                                           GameScene.player.rect.y, 5))
                        elif event.key == controls[5]:  # shoot laser
                            if GameScene.player.has_laser:
                                laser_beam_sound.play()  # laser sound effect
                                GameScene.player.has_laser = False
                                GameScene.start_time = functions.get_current_time()
                                GameScene.laser.update()
                                GameScene.laser.state = "moving"
                        elif event.key == pygame.K_ESCAPE:
                            pygame.time.set_timer(GameScene.ALIEN_LVL2_STOP, 0)
                            self.switch_to_scene(GameOptionsScene())
                            menu_sound.play()

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_0:
                            GameScene.cheats_on = False
                    elif event.type == GameScene.ALIEN_LVL1_RESPAWN:  # spawn level 1 alien
                        GameScene.aliens.add(
                            Alien([functions.get_image('img/alien.png').convert_alpha(),
                                   functions.get_image('img/dust0.png').convert_alpha(),
                                   functions.get_image('img/dust1.png').convert_alpha(),
                                   functions.get_image('img/dust2.png').convert_alpha(),
                                   functions.get_image('img/dust3.png').convert_alpha()], random.randint(0, 736),
                                  random.randint(-500, -200), 2, 1))
                    elif event.type == GameScene.ALIEN_LVL2_RESPAWN:  # spawn level 2 alien
                        # generate random number which indicates where the hole in alien level 2 wall will be
                        random_number = random.randint(0, 11)
                        extra = 0
                        for i in range(11):  # range(number of level 2 aliens in a row)
                            if random_number == i:
                                extra = 95  # width of the hole in the alien level 2 wall
                            GameScene.aliens.add(
                                AlienLevel2([functions.get_image('img/alien2.png').convert_alpha(),
                                             functions.get_image('img/dust0.png').convert_alpha(),
                                             functions.get_image('img/dust1.png').convert_alpha(),
                                             functions.get_image('img/dust2.png').convert_alpha(),
                                             functions.get_image('img/dust3.png').convert_alpha()],
                                            64 * i + extra, -100, 2, 1))
                    elif event.type == GameScene.ALIEN_LVL3_RESPAWN:  # spawn level 1 alien
                        GameScene.aliens.add(
                            AlienLevel3([functions.get_image('img/alien3.png').convert_alpha(),
                                         functions.get_image('img/alien3_1hp.png').convert_alpha(),
                                         functions.get_image('img/alien3_explosion0.png').convert_alpha(),
                                         functions.get_image('img/alien3_explosion1.png').convert_alpha(),
                                         functions.get_image('img/alien3_explosion2.png').convert_alpha(),
                                         functions.get_image('img/alien3_explosion3.png').convert_alpha()],
                                        random.randint(0, 736),
                                        random.randint(-1000, -200), 2, 2))
                    elif event.type == GameScene.ALIEN_LVL4_RESPAWN:  # spawn level 1 alien
                        GameScene.aliens.add(
                            AlienLevel4([functions.get_image('img/big_alien.png').convert_alpha(),
                                         functions.get_image('img/big_alien_1hp.png').convert_alpha(),
                                         functions.get_image('img/big_alien_2hp.png').convert_alpha(),
                                         functions.get_image('img/big_alien_explosion0.png').convert_alpha(),
                                         functions.get_image('img/big_alien_explosion1.png').convert_alpha(),
                                         functions.get_image('img/big_alien_explosion2.png').convert_alpha(),
                                         functions.get_image('img/big_alien_explosion3.png').convert_alpha(),
                                         functions.get_image('img/big_alien_explosion4.png').convert_alpha(),
                                         functions.get_image('img/big_alien_explosion5.png').convert_alpha()],
                                        random.randint(0, 544),
                                        random.randint(-1000, -500), 2, 3))
                    elif event.type == GameScene.ALIEN_LVL1_STOP:  # stop level  alien
                        pygame.time.set_timer(GameScene.ALIEN_LVL2_RESPAWN, 5000)
                        pygame.time.set_timer(GameScene.ALIEN_LVL1_RESPAWN, 0)
                        pygame.time.set_timer(GameScene.ALIEN_LVL1_STOP, 0)
                        pygame.time.set_timer(GameScene.ALIEN_LVL2_STOP, 22000)
                    elif event.type == GameScene.ALIEN_LVL2_STOP:  # stop level 2 alien
                        pygame.time.set_timer(GameScene.ALIEN_LVL2_RESPAWN, 0)
                        pygame.time.set_timer(GameScene.ALIEN_LVL1_RESPAWN, random.randint(180, 230))
                        pygame.time.set_timer(GameScene.ALIEN_LVL1_STOP, random.randint(30000, 50000))
                        pygame.time.set_timer(GameScene.ALIEN_LVL2_STOP, 0)
                    elif event.type == GameScene.COLLECTABLE_AMMO_RESPAWN:
                        GameScene.collectables.add(
                            Collectable([functions.get_image('img/bullet2.png').convert_alpha()],
                                        random.randint(0, 736),
                                        -100, 2, "ammo"))
                    elif event.type == GameScene.COLLECTABLE_SHIELD_RESPAWN:
                        GameScene.collectables.add(
                            Collectable([functions.get_image('img/shield.png').convert_alpha()],
                                        random.randint(0, 736),
                                        -100, 2, "shield"))
                    elif event.type == GameScene.COLLECTABLE_LASER_RESPAWN:
                        GameScene.collectables.add(
                            Collectable([functions.get_image('img/laser_gun.png').convert_alpha()],
                                        random.randint(0, 736),
                                        -100, 2, "laser"))
                    elif event.type == GameScene.COLLECTABLE_IMMUNITY_RESPAWN:
                        GameScene.collectables.add(
                            Collectable([functions.get_image('img/immune.png').convert_alpha()],
                                        random.randint(0, 736),
                                        -100, 2, "immunity"))
                    elif event.type == GameScene.COLLECTABLE_ANGRY_RESPAWN:
                        GameScene.collectables.add(
                            Collectable([functions.get_image('img/angry_mode.png').convert_alpha()],
                                        random.randint(0, 736),
                                        -100, 2, "angry_mode"))
                    elif event.type == GameScene.COLLECTABLE_WEAPON_DAMAGED:
                        GameScene.collectables.add(
                            Collectable([functions.get_image('img/weapon_damaged.png').convert_alpha()],
                                        random.randint(0, 736),
                                        -100, 2, "weapon_damaged")
                        )

    def update(self, keys):
        # player movement
        for player in GameScene.player_sprite:
            player.check_boundaries()
            if not GameScene.pause:
                player.update(keys)
            player.draw(keys)

        # alien movement
        for alien in GameScene.aliens:
            if not GameScene.pause:
                alien.update()
            alien.check_boundaries()
            alien.draw()  # draw alien
            alien.action()  # draw alien
            fix_alien_overlapping(alien)  # prevent from going on top of each other
        if not GameScene.player.is_immune:
            check_if_alien_collide()  # collisions

        # collectables movement
        for collectable in GameScene.collectables:
            if not GameScene.pause:
                collectable.update()
            collectable.draw()  # draw collectable
            collectable.check_boundaries()  # respawn collectable
        check_if_collectable_collide()  # collectable - player collision

        # player bullets movement
        for bullet in GameScene.bullets:
            if not GameScene.pause:
                bullet.update()
            bullet.draw()
            bullet.check_boundaries()

        # alien bullets movement
        for bullet in GameScene.enemy_bullets:
            if not GameScene.pause:
                bullet.update()
            bullet.draw()
            bullet.check_boundaries()

        # laser movement
        if GameScene.laser.state == "moving":
            GameScene.laser.update()
            GameScene.laser.draw()
            if functions.get_current_time() - GameScene.start_time > 2:
                GameScene.laser.state = "loaded"

        # activate the cheats (ammo boost)
        if GameScene.cheats_on:
            GameScene.player.num_of_bullets += 1

        # disable immunity bonus - it lasts 7 seconds
        if GameScene.player.is_immune:
            immunity_timer()

        # disable angry_mode debuff
        if Alien.angry_mode:
            angry_mode_timer()

        # disable weapon_damaged
        if GameScene.player.weapon_damaged:
            weapon_damaged_timer()

        # pause the game for 3 seconds after resuming the game
        if GameScene.pause:
            get_ready()

    def render(self):

        # default background color(RGB) and image
        # now animated
        rel_y = self.bg_y % self.background.get_rect().height
        frame.blit(self.background, (0, rel_y - self.background.get_rect().height))
        if rel_y < HEIGHT:
            frame.blit(self.background, (0, rel_y))
        if not GameScene.pause:
            self.bg_y += 1

        # change background
        self.change_background()
        # draw the new background
        if self.previous_background is not None:
            frame.blit(self.previous_background, (0, 0))
        if self.current_bg is not None:
            frame.blit(self.current_bg, (0, 0))

        # show ammo (bullets left)
        update_bullets_label(GameScene.bullets_label_x, GameScene.bullets_label_y)

        # show score label
        update_score_label(GameScene.score_label_x, GameScene.score_label_y)

        # show collectables
        show_collectables()

        # indicate that game is over via label
        if not GameScene.game_is_active:
            # game_over_label()
            self.switch_to_scene(GameFailScene())


class GameOptionsScene(Scene):
    def __init__(self):
        super().__init__()
        # pause main theme
        pygame.mixer.music.pause()

        self.rect = functions.get_image(
            'img/controls_wsad.png').convert_alpha().get_rect()  # rect of the menu (size + x,y)
        self.rect.center = frame_rect.center  # rect but centered in the frame (size + x,y(centered))
        self.menu = pygame.Surface((self.rect.width, self.rect.height))  # new surface for the menu
        self.menu.set_colorkey(RED)
        self.rect1 = pygame.Rect(0, 0, self.rect.width, self.rect.height)  # rect to make the border of the menu

        pygame.draw.rect(self.menu, RED, self.rect1)

        # font
        self.menu_font = functions.get_font('fonts/Space_Galaxy.ttf', 32)
        self.menu_font_big = functions.get_font('fonts/Space_Galaxy.ttf', 96)

        # colors
        self.golden = (120, 120, 50)
        self.green = (52, 150, 50)
        self.blue = (10, 110, 160)

        # buttons objects
        self.button1 = gui_elements.Button(0, 40, 160, 40, WHITE, self.golden, "Audio", True)
        self.button2 = gui_elements.Button(0, 120, 160, 40, WHITE, self.green, "Info", True)
        self.button3 = gui_elements.Button(0, 200, 160, 40, WHITE, self.blue, "Restart", True)
        self.button4 = gui_elements.Button(0, 280, 160, 40, WHITE, (52, 45, 79), "Main Menu", True)
        self.buttons = [self.button1, self.button2, self.button3, self.button4]
        self.button1.rect.centerx = self.rect1.centerx  # center buttons horizontally in the menu
        self.button2.rect.centerx = self.rect1.centerx
        self.button3.rect.centerx = self.rect1.centerx
        self.button4.rect.centerx = self.rect1.centerx

        # text
        self.game_paused_text = gui_elements.Text("Game Paused", WHITE, self.menu_font_big)
        self.game_paused_text.rect.centerx = self.rect.centerx
        self.game_paused_text.rect.y += 30

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(GameScene())
                GameScene.pause = True
                GameScene.start_time = functions.get_current_time()

    def update(self, pressed_keys):
        # Button action
        def button1_action():
            self.switch_to_scene(GameOptionsAudioScene())

        def button2_action():
            pygame.time.wait(150)
            self.switch_to_scene(GameOptionsInfoScene())

        def button3_action():
            game_erase()
            game_restart()
            self.switch_to_scene(GameScene())

        def button4_action():
            pygame.time.wait(150)
            functions.load_music('audio/menu_music.mp3')
            pygame.mixer.music.play(-1)
            self.switch_to_scene(MenuScene())

        self.button1.on_click_action(lambda: button1_action())
        self.button2.on_click_action(lambda: button2_action())
        self.button3.on_click_action(lambda: button3_action())
        self.button4.on_click_action(lambda: button4_action())

    def render(self):
        # menu surface
        frame.blit(functions.get_image('img/background1.png').convert(), (0, 0))
        frame.blit(self.menu, self.rect)

        # game paused text
        self.game_paused_text.write(frame)

        # Button draw with mouse hover effect
        # Button text
        for button in self.buttons:
            button.draw(self.menu)
            button.draw_border(self.menu, BLACK)
            button.write(self.menu, self.menu_font)


class GameOptionsInfoControlsScene(Scene):
    def __init__(self):
        super().__init__()
        if current_controls == 0:
            self.background = functions.get_image('img/controls_wsad.png').convert_alpha()
        else:
            self.background = functions.get_image('img/controls_arrows.png').convert_alpha()
        self.rect = self.background.get_rect()  # rect of the menu (size + x,y)
        self.rect.center = frame_rect.center  # rect but centered in the frame (size + x,y(centered))

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(GameOptionsInfoScene())

    def update(self, pressed_keys):
        pass

    def render(self):
        frame.blit(self.background, self.rect)


class GameOptionsInfoSheetScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = functions.get_image('img/sheet.png').convert_alpha()
        self.rect = self.background.get_rect()  # rect of the menu (size + x,y)
        self.rect.center = frame_rect.center  # rect but centered in the frame (size + x,y(centered))

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(GameOptionsInfoScene())

    def update(self, pressed_keys):
        pass

    def render(self):
        frame.blit(self.background, self.rect)


class GameOptionsInfoScene(GameOptionsScene):
    def __init__(self):
        super().__init__()
        self.button1.text = "Controls"
        self.button2.text = "Cheat Sheet"
        self.buttons = [self.button1, self.button2]

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(GameOptionsScene())

    def update(self, pressed_keys):
        # Button action
        def button1_action():
            self.switch_to_scene(GameOptionsInfoControlsScene())

        def button2_action():
            self.switch_to_scene(GameOptionsInfoSheetScene())

        self.button1.on_click_action(lambda: button1_action())
        self.button2.on_click_action(lambda: button2_action())

    def render(self):
        # menu surface
        frame.blit(functions.get_image('img/background1.png').convert(), (0, 0))
        frame.blit(self.menu, self.rect)
        # game paused text
        self.game_paused_text.write(frame)
        # Button draw with mouse hover effect
        # Button text
        for button in self.buttons:
            button.draw(self.menu)
            button.draw_border(self.menu, BLACK)
            button.write(self.menu, self.menu_font)


class MenuCreditsScene(Scene):
    def __init__(self):
        super().__init__()
        # text that will be shown in credits
        self.credits_list = ["Space Bottle", " ", " ", " ", "Programming -- daCFniel", "Graphics -- daCFniel",
                             "Design -- daCFniel", " ", " ", " ",
                             "Menu song -- Namrox", "Testing -- Namrox", "Ideas -- Namrox"]
        # fonts
        self.credits_font = functions.get_font('fonts/Space_Galaxy.ttf', 40)
        self.credits_font_big = functions.get_font('fonts/Space_Galaxy.ttf', 90)
        self.text_objects = []
        # list containing all lines of the credits (as objects and their rects)
        for i, line in enumerate(self.credits_list):
            text_object = self.credits_font.render(line, True, WHITE)
            text_object_rect = text_object.get_rect(centerx=frame_rect.centerx, y=frame_rect.bottom + i * 50)
            self.text_objects.append((text_object, text_object_rect))

        # ending credit text
        self.ending_text = gui_elements.Text("Hope you enjoyed", WHITE, self.credits_font_big)
        self.ending_text.rect.center = frame_rect.center

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(MenuScene())
                pygame.mixer.music.load('audio/menu_music.mp3')
                pygame.mixer.music.play(-1)

    def update(self, pressed_keys):
        for text, rect in self.text_objects:
            frame.blit(text, rect)
            rect.move_ip(0, -1)

        if not frame_rect.collidelistall([r for (_, r) in self.text_objects]):
            self.ending_text.write(frame)

    def render(self):
        frame.fill(BLACK)


class GameOptionsAudioScene(GameOptionsScene):
    def __init__(self):
        super().__init__()
        # fonts
        self.audio_font = functions.get_font('fonts/Space_Galaxy.ttf', 40)
        self.percentage_font = functions.get_font('fonts/Symbols.otf', 40)

        # Texts
        self.music_volume_text = gui_elements.Text("Music volume", WHITE, self.audio_font)
        self.sound_volume_text = gui_elements.Text("Sound effects volume", WHITE, self.audio_font)
        self.percentage_text = gui_elements.Text("%", WHITE, self.percentage_font)
        self.percentage_text2 = gui_elements.Text("%", WHITE, self.percentage_font)
        self.texts = [self.music_volume_text, self.sound_volume_text, self.percentage_text, self.percentage_text2]
        self.music_volume_text.rect.centerx = self.rect1.centerx
        self.music_volume_text.rect.y += 40
        self.sound_volume_text.rect.center = self.rect1.center
        self.percentage_text2.rect = (320, 200)
        self.percentage_text.rect = (320, 90)

        # Input boxes
        self.box1 = gui_elements.InputBox(0, 90, 120, 40, WHITE, BLACK, str(int(music_volume)), True)
        self.box2 = gui_elements.InputBox(0, 200, 120, 40, WHITE, BLACK, str(int(sounds_volume)), True)
        self.input_boxes = [self.box1, self.box2]
        self.box1.rect.centerx = self.rect1.centerx
        self.box2.rect.centerx = self.rect1.centerx

        # Color
        self.light_green = (50, 210, 25)

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(GameOptionsScene())
            for box in self.input_boxes:
                box.handle_input(event)

    def update(self, pressed_keys):

        def box1_action():
            if self.box1.active:
                if self.box1.active2:
                    if functions.is_number(self.box1.text):
                        if 0 <= int(self.box1.text) <= 100:
                            global music_volume
                            music_volume = int(self.box1.text)
                            save_data()
                            pygame.mixer.music.set_volume(music_volume / 100)
                            accept_sound.play()
                            self.percentage_text.text_color = self.light_green
                        self.box1.active2 = False

        def box2_action():
            if self.box2.active:
                if self.box2.active2:
                    if functions.is_number(self.box2.text):
                        if 0 <= int(self.box2.text) <= 100:
                            global sounds_volume
                            sounds_volume = int(self.box2.text)
                            save_data()
                            for sound in sounds:
                                sound.set_volume(sounds_volume / 100)
                            accept_sound.play()
                            self.percentage_text2.text_color = self.light_green
                        self.box2.active2 = False

        box1_action()
        box2_action()

    def render(self):
        # menu surface
        frame.blit(functions.get_image('img/background1.png').convert(), (0, 0))
        frame.blit(self.menu, self.rect)

        for text in self.texts:
            text.write(self.menu)
        self.game_paused_text.write(frame)
        for box in self.input_boxes:
            box.draw(self.menu)
            box.write(self.menu, self.menu_font)
            box.check_if_active()


class MenuScene(Scene):
    # menu music
    functions.load_music('audio/menu_music.mp3')
    pygame.mixer.music.play(-1)

    def __init__(self):
        super().__init__()
        # logo
        self.logo = functions.get_image('img/logo_full.png')
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.midtop = frame_rect.midtop

        # bg
        self.background_img = functions.get_image('img/menu_bg.jpg')
        self.rect = self.background_img.get_rect()

        # font
        self.menu_font = functions.get_font('fonts/Space_Galaxy.ttf', 32)

        # buttons objects
        self.button1 = gui_elements.Button(0, 210, 160, 40, WHITE, BLACK, "Play")
        self.button2 = gui_elements.Button(0, 290, 160, 40, WHITE, BLACK, "Settings")
        self.button3 = gui_elements.Button(0, 370, 160, 40, WHITE, BLACK, "Credits")
        self.button4 = gui_elements.Button(0, 450, 160, 40, WHITE, BLACK, "Quit")
        self.shop_button = gui_elements.Button(0, 0, 120, 40, WHITE, OCEAN, "Shop", False, 3)
        self.buttons = [self.button1, self.button2, self.button3, self.button4, self.shop_button]
        self.button1.rect.centerx = frame_rect.centerx  # center buttons horizontally in the menu
        self.button2.rect.centerx = frame_rect.centerx
        self.button3.rect.centerx = frame_rect.centerx
        self.button4.rect.centerx = frame_rect.centerx
        self.shop_button.rect.topright = frame_rect.topright
        # back button
        self.back_button_font = functions.get_font('fonts/Space_Galaxy.ttf', 40)
        self.back_button = gui_elements.Button(0, 0, 80, 40, WHITE, BLACK, "Back")

        self.back_button.rect.bottomleft = frame_rect.bottomleft
        # rank img
        self.rank_img = get_current_rank()
        self.rank_img_rect = self.rank_img.get_rect()
        self.rank_img_rect.bottomright = frame_rect.bottomright

        # coins text and img
        self.coin_img = functions.get_image('img/coin3.png')
        self.coin_img_rect = self.coin_img.get_rect()
        self.coin_img_rect.bottomleft = frame_rect.bottomleft
        self.coin_img_rect.x += 15
        if total_coins >= 10:
            self.coin_img_rect.x += 10
        self.coins_text = gui_elements.Text(str(total_coins), WHITE, self.menu_font)
        self.coins_text.rect.bottomleft = frame_rect.bottomleft

    def event_handling(self, events):
        pass

    def update(self, pressed_keys):
        # Button action
        def button1_action():
            self.switch_to_scene(MenuPlayScene())

        def button2_action():
            pygame.time.delay(150)  # trick to prevent double clicking the button
            self.switch_to_scene(MenuSettingsScene())

        def button3_action():
            pygame.mixer.music.load('audio/credits_music.mp3')
            pygame.mixer.music.play(-1)
            self.switch_to_scene(MenuCreditsScene())

        def button4_action():
            self.terminate()

        def shop_button_action():
            self.switch_to_scene(MenuShopScene())

        self.button1.on_click_action(lambda: button1_action())
        self.button2.on_click_action(lambda: button2_action())
        self.button3.on_click_action(lambda: button3_action())
        self.button4.on_click_action(lambda: button4_action())
        self.shop_button.on_click_action(lambda: shop_button_action())

    def render(self):
        # menu background and logo
        frame.blit(self.background_img, (0, 0))
        frame.blit(self.logo, self.logo_rect)
        # rank preview
        frame.blit(self.rank_img, self.rank_img_rect)
        # coins preview
        self.coins_text.write(frame)
        frame.blit(self.coin_img, self.coin_img_rect)
        # Button draw with mouse hover effect
        # Button text
        for button in self.buttons:
            button.draw(frame)
            button.write(frame, self.menu_font)
        self.shop_button.draw_border(frame, (138, 197, 230))


class MenuShopScene(MenuScene):
    def __init__(self):
        super().__init__()
        # Font
        self.font_big = functions.get_font('fonts/Space_Galaxy.ttf', 80)
        self.font_medium = functions.get_font('fonts/Space_Galaxy.ttf', 30)
        # Text
        self.text = gui_elements.Text("Shop", WHITE, self.font_big)
        self.text.rect.midtop = frame_rect.midtop
        self.text.rect.y += 40
        # Back button
        self.back_button.rect.topleft = frame_rect.topleft
        # Skins
        self.common_skin = Skin(functions.get_image('img/spaceship.png'), "Rocket Alpha", 0)
        self.rare_skin = Skin(functions.get_image('img/spaceship2.png'), "Falcon 68", 3)
        self.epic_skin = Skin(functions.get_image('img/spaceship3.png'), "Force QPA", 6)
        self.legendary_skin = Skin(functions.get_image('img/spaceship4.png'), "Galaxy Warship Prime", 10)
        self.skins = [self.common_skin, self.rare_skin, self.epic_skin, self.legendary_skin]
        self.common_skin.rect.midleft = frame_rect.midleft
        self.rare_skin.rect.midleft = frame_rect.midleft
        self.epic_skin.rect.midleft = frame_rect.midleft
        self.legendary_skin.rect.midleft = frame_rect.midleft
        self.common_skin.rect.x += 100
        self.rare_skin.rect.x += 260
        self.epic_skin.rect.x += 410
        self.legendary_skin.rect.x += 610
        # Skin names
        self.common_skin_name = gui_elements.Text(self.common_skin.name, WHITE, self.font_medium)
        self.rare_skin_name = gui_elements.Text(self.rare_skin.name, WHITE, self.font_medium)
        self.epic_skin_name = gui_elements.Text(self.epic_skin.name, WHITE, self.font_medium)
        self.legendary_skin_name = gui_elements.Text(self.legendary_skin.name, WHITE, self.font_medium)
        self.common_skin_name.rect = (65, 230)
        self.rare_skin_name.rect = (240, 230)
        self.epic_skin_name.rect = (385, 230)
        self.legendary_skin_name.rect = (535, 230)
        self.skin_names = [self.common_skin_name, self.rare_skin_name, self.epic_skin_name, self.legendary_skin_name]
        # Skin costs
        if skins_owned[0] == 0:
            rare_cost = str(self.rare_skin.cost) + " Coins"
        else:
            rare_cost = "Owned"
        if skins_owned[1] == 0:
            epic_cost = str(self.epic_skin.cost) + " Coins"
        else:
            epic_cost = "Owned"
        if skins_owned[2] == 0:
            legendary_cost = str(self.legendary_skin.cost) + " Coins"
        else:
            legendary_cost = "Owned"
        self.common_skin_cost = gui_elements.Button(85, 340, 100, 50, WHITE, BLACK, "Default")
        self.rare_skin_cost = gui_elements.Button(245, 340, 100, 50, DARKBLUE, BLACK, rare_cost)
        self.epic_skin_cost = gui_elements.Button(395, 340, 100, 50, MAGENTA, BLACK, epic_cost)
        self.legendary_skin_cost = gui_elements.Button(595, 340, 100, 50, GOLD, BLACK,
                                                       legendary_cost)
        self.skin_costs = [self.common_skin_cost, self.rare_skin_cost, self.epic_skin_cost, self.legendary_skin_cost]

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(MenuScene())

    def update(self, pressed_keys):
        def button1_action():
            pass

        def button2_action():
            global total_coins
            #  If you have enough coins and you don't own the skin already
            if total_coins >= self.rare_skin.cost and skins_owned[0] == 0:
                purchase_sound.play()
                total_coins -= self.rare_skin.cost
                skins_owned[0] = 1
                save_data()
                pygame.time.wait(300)
                self.switch_to_scene(MenuShopScene())

        def button3_action():
            global total_coins
            if total_coins >= self.epic_skin.cost and skins_owned[1] == 0:
                purchase_sound.play()
                total_coins -= self.epic_skin.cost
                skins_owned[1] = 1
                save_data()
                pygame.time.wait(300)
                self.switch_to_scene(MenuShopScene())

        def button4_action():
            global total_coins
            if total_coins >= self.legendary_skin.cost and skins_owned[2] == 0:
                purchase_sound.play()
                total_coins -= self.legendary_skin.cost
                skins_owned[2] = 1
                save_data()
                pygame.time.wait(300)
                self.switch_to_scene(MenuShopScene())

        self.common_skin_cost.on_click_action(lambda: button1_action())
        self.rare_skin_cost.on_click_action(lambda: button2_action())
        self.epic_skin_cost.on_click_action(lambda: button3_action())
        self.legendary_skin_cost.on_click_action(lambda: button4_action())

        def back_button_action():
            self.switch_to_scene(MenuScene())

        self.back_button.on_click_action(lambda: back_button_action())

    def render(self):
        # menu background
        frame.blit(self.background_img, (0, 0))
        # coins preview
        self.coins_text.write(frame)
        frame.blit(self.coin_img, self.coin_img_rect)
        # write header text
        self.text.write(frame)
        # back button
        self.back_button.draw(frame)
        self.back_button.write(frame, self.back_button_font)
        # skins
        for skin in self.skins:
            frame.blit(skin.image, skin.rect)
        # skin names
        for name in self.skin_names:
            name.write(frame)
        # skin costs
        for cost in self.skin_costs:
            cost.draw(frame)
            cost.write(frame, self.font_medium)


class MenuSettingsScene(MenuScene):
    def __init__(self):
        super().__init__()
        # Font
        self.font = functions.get_font('fonts/Space_Galaxy.ttf', 40)
        self.font_big = functions.get_font('fonts/Space_Galaxy.ttf', 80)
        # Text
        self.text = gui_elements.Text("Game Settings", WHITE, self.font_big)
        self.text.rect.midtop = frame_rect.midtop
        self.text.rect.y += 40
        # Buttons
        self.button1 = gui_elements.Button(0, 0, 190, 45, WHITE, BLACK, "Display")
        self.button2 = gui_elements.Button(0, 0, 190, 45, WHITE, BLACK, "Audio")
        self.button3 = gui_elements.Button(0, 0, 190, 45, WHITE, BLACK, "Controls")
        self.buttons = [self.button1, self.button2, self.button3]
        self.button1.rect.center = frame_rect.center
        self.button2.rect.center = frame_rect.center
        self.button3.rect.center = frame_rect.center
        self.button1.rect.y -= 120
        self.button2.rect.y -= 40
        self.button3.rect.y += 40

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(MenuScene())

    def update(self, pressed_keys):
        def button1_action():
            self.switch_to_scene(MenuSettingsDisplayScene())

        def button2_action():
            self.switch_to_scene(MenuSettingsAudioScene())

        def button3_action():
            self.switch_to_scene(MenuSettingsControlsScene())

        self.button1.on_click_action(lambda: button1_action())
        self.button2.on_click_action(lambda: button2_action())
        self.button3.on_click_action(lambda: button3_action())

        def back_button_action():
            self.switch_to_scene(MenuScene())

        self.back_button.on_click_action(lambda: back_button_action())

    def render(self):
        # play background
        frame.blit(self.background_img, (0, 0))
        # text
        self.text.write(frame)
        # buttons
        for button in self.buttons:
            button.draw(frame)
            button.write(frame, self.font)
        # back button
        self.back_button.draw(frame)
        self.back_button.write(frame, self.back_button_font)


class MenuSettingsAudioScene(GameOptionsAudioScene):
    def __init__(self):
        super().__init__()
        # bg
        self.background_img = functions.get_image('img/menu_bg.jpg')
        # overriding boxes to set False for custom surface
        self.box1 = gui_elements.InputBox(0, 90, 120, 40, WHITE, BLACK, str(int(music_volume)))
        self.box2 = gui_elements.InputBox(0, 200, 120, 40, WHITE, BLACK, str(int(sounds_volume)))
        self.input_boxes = [self.box1, self.box2]
        self.box1.rect.center = frame_rect.center
        self.box2.rect.center = frame_rect.center
        self.box1.rect.y -= 90
        self.box2.rect.y += 40
        # also fixing texts place
        self.music_volume_text.rect.centerx = frame_rect.centerx
        self.music_volume_text.rect.y += 80
        self.sound_volume_text.rect.center = frame_rect.center
        self.sound_volume_text.rect.y -= 20
        self.percentage_text.rect = (470, 190)
        self.percentage_text2.rect = (470, 320)

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(MenuSettingsScene())
            for box in self.input_boxes:
                box.handle_input(event)

    def render(self):
        # background
        frame.blit(self.background_img, (0, 0))
        for text in self.texts:
            text.write(frame)
        for box in self.input_boxes:
            box.draw(frame)
            box.write(frame, self.menu_font)
            box.check_if_active()


class MenuSettingsDisplayScene(MenuScene):
    def __init__(self):
        super().__init__()

        # Font
        self.settings_font = functions.get_font('fonts/Space_Galaxy.ttf', 40)
        # Text
        self.text = gui_elements.Text("Fullscreen Mode", WHITE, self.settings_font)
        self.text.rect.center = frame_rect.center
        self.text.rect.x -= 80
        # Button
        self.button = gui_elements.Button(0, 0, 80, 40, WHITE, BLACK, is_fullscreen())
        self.button.rect.center = frame_rect.center
        self.button.rect.x += 100

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(MenuSettingsScene())

    def update(self, pressed_keys):
        def button_action():
            global frame, display_mode
            if display_mode == 0:
                frame = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                display_mode = 1
            else:
                frame = pygame.display.set_mode((WIDTH, HEIGHT))
                display_mode = 0
            save_data()
            self.switch_to_scene(MenuSettingsDisplayScene())

        self.button.on_click_action(lambda: button_action())

        def back_button_action():
            pygame.time.wait(150)
            self.switch_to_scene(MenuSettingsScene())

        self.back_button.on_click_action(lambda: back_button_action())

    def render(self):
        # settings background
        frame.blit(self.background_img, (0, 0))
        # text
        self.text.write(frame)
        # button
        self.button.draw(frame)
        self.button.write(frame, self.settings_font)
        self.button.draw_border(frame, WHITE)
        # back button
        self.back_button.draw(frame)
        self.back_button.write(frame, self.back_button_font)


class MenuSettingsControlsScene(MenuSettingsDisplayScene):
    def __init__(self):
        super().__init__()
        self.text.text = "Player movement"
        self.button.text = get_current_controls()
        self.button.rect.width = 110
        self.button.rect.height = 70
        self.button.rect.y -= 20

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(MenuSettingsScene())

    def update(self, pressed_keys):
        def button_action():
            global controls, current_controls
            if current_controls == 0:
                controls = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_x, pygame.K_c,
                            pygame.K_z]
                current_controls = 1
            else:
                controls = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE,
                            pygame.K_c, pygame.K_LSHIFT]  # default controls W A S D
                current_controls = 0
            save_data()
            pygame.time.wait(150)
            self.switch_to_scene(MenuSettingsControlsScene())

        self.button.on_click_action(lambda: button_action())

        def back_button_action():
            pygame.time.wait(150)
            self.switch_to_scene(MenuSettingsScene())

        self.back_button.on_click_action(lambda: back_button_action())


class MenuPlayScene(MenuScene):
    def __init__(self):
        super().__init__()
        # Font
        self.font = functions.get_font('fonts/Space_Galaxy.ttf', 40)
        # Text
        self.text = gui_elements.Text("Select game mode", WHITE, self.font)
        self.text.rect.center = frame_rect.center
        self.text.rect.y -= 80
        # Buttons
        self.button1 = gui_elements.Button(0, 0, 190, 45, WHITE, BLACK, "Story mode")
        self.button2 = gui_elements.Button(0, 0, 190, 45, WHITE, BLACK, "Endless mode")
        self.buttons = [self.button1, self.button2]
        self.button1.rect.center = frame_rect.center
        self.button2.rect.center = frame_rect.center
        self.button2.rect.y += 80

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(MenuScene())

    def update(self, pressed_keys):
        def button2_action():
            self.switch_to_scene(MenuPlayEndlessScene())

        self.button2.on_click_action(lambda: button2_action())

        def back_button_action():
            self.switch_to_scene(MenuScene())

        self.back_button.on_click_action(lambda: back_button_action())

    def render(self):
        # play background
        frame.blit(self.background_img, (0, 0))
        frame.blit(self.logo, self.logo_rect)
        # text
        self.text.write(frame)
        # buttons
        for button in self.buttons:
            button.draw(frame)
            button.write(frame, self.font)
            button.draw_border(frame, WHITE)
        # back button
        self.back_button.draw(frame)
        self.back_button.write(frame, self.back_button_font)


class MenuPlayEndlessScene(MenuScene):
    def __init__(self):
        super().__init__()

        # fonts
        self.font = functions.get_font('fonts/Space_Galaxy.ttf', 40)
        self.font_big = functions.get_font('fonts/Space_Galaxy.ttf', 54)
        self.font2 = functions.get_font('fonts/Steronite.ttf', 40)

        # button
        self.button = gui_elements.Button(0, 0, 190, 45, WHITE, BLACK, "Jump in")
        self.button.rect.center = frame_rect.center
        self.button.rect.y += 140

        # texts
        self.text = gui_elements.Text("Current rank", WHITE, self.font_big)
        self.text.rect.center = frame_rect.center
        self.text.rect.x -= 200
        self.text.rect.y -= 120
        self.text2 = gui_elements.Text("Highest score", WHITE, self.font_big)
        self.text2.rect.center = frame_rect.center
        self.text2.rect.x += 200
        self.text2.rect.y -= 120
        self.text3 = gui_elements.Text(str(top_score), WHITE, self.font_big)
        self.text3.rect.center = frame_rect.center
        self.text3.rect.x += 130
        self.text3.rect.y -= 60
        self.text4 = gui_elements.Text("EXP", WHITE, self.font2)
        self.text4.rect.bottomright = frame_rect.bottomright
        self.text4.rect.y -= 50
        self.text5 = gui_elements.Text(str(current_exp) + " / " + str(exp_required_total), WHITE,
                                       self.font2)
        self.text5.rect.bottomright = frame_rect.bottomright
        self.text6 = gui_elements.Text("Endless mode", BLACK, self.font_big)
        self.text6.rect.midtop = frame_rect.midtop
        self.text6.rect.y += 20
        self.texts = [self.text, self.text2, self.text3, self.text4, self.text5, self.text6]

        # rank img
        self.rank_img = get_current_rank()
        self.rank_img_rect = self.rank_img.get_rect()
        self.rank_img_rect.center = frame_rect.center
        self.rank_img_rect.x -= 230
        self.rank_img_rect.y -= 60

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_to_scene(MenuPlayScene())

    def update(self, pressed_keys):
        def button_action():
            self.switch_to_scene(GameScene())
            game_erase()
            game_restart()

        self.button.on_click_action(lambda: button_action())

        def back_button_action():
            pygame.time.wait(150)
            self.switch_to_scene(MenuPlayScene())

        self.back_button.on_click_action(lambda: back_button_action())

    def render(self):
        # play background
        frame.blit(self.background_img, (0, 0))
        # rank
        frame.blit(self.rank_img, self.rank_img_rect)
        # texts
        for text in self.texts:
            text.write(frame)
        # button
        self.button.draw(frame)
        self.button.write(frame, self.font)
        self.button.draw_border(frame, WHITE)
        # back button
        self.back_button.draw(frame)
        self.back_button.write(frame, self.back_button_font)


class GameFailScene(Scene):
    def __init__(self):
        super().__init__()
        # Fonts
        self.game_over_font = functions.get_font('fonts/Space_Galaxy.ttf', 90)
        self.try_again_font = functions.get_font('fonts/Space_Galaxy.ttf', 50)
        # Text
        self.game_over_text = gui_elements.Text("Game Over", WHITE, self.game_over_font, BLACK)
        self.game_over_text.rect.centerx = frame_rect.centerx
        self.game_over_text.rect.y = 180
        self.promotion_text = gui_elements.Text("YOU GOT PROMOTED", ORANGE, self.game_over_font)
        self.promotion_text.rect.midtop = frame_rect.midtop
        self.promotion_text.rect.y += 40
        self.top_score_text = gui_elements.Text("NEW TOP SCORE", BLUE, self.game_over_font)
        self.top_score_text.rect.midbottom = frame_rect.midbottom
        self.top_score_text.rect.y -= 100
        self.coins_reward_text = gui_elements.Text("Reward  1 coin", GOLD, self.try_again_font)
        self.coins_reward_text.rect.center = frame_rect.center
        self.coins_reward_text.rect.y -= 165
        self.coins_collected_text = gui_elements.Text(str(current_coins) + " Coins Collected", WHITE,
                                                      self.try_again_font)
        self.coins_collected_text.rect.midbottom = frame_rect.midbottom
        self.texts = [self.game_over_text]
        # Button
        self.button = gui_elements.Button(0, 0, 180, 80, WHITE, BLACK, "Try Again")
        self.button2 = gui_elements.Button(0, 0, 220, 60, WHITE, BLACK, "Main Menu")
        self.button.rect.center = frame_rect.center
        self.button.rect.y += 20
        self.button2.rect.bottomright = frame_rect.bottomright
        self.buttons = [self.button, self.button2]

        got_top_score = update_top_score()  # update the top score if player hits the new record
        got_promoted = check_if_promotion()  # add exp and check if player is eligible for promotion
        got_coins = update_total_coins()  # add coins collected in this game to the total amount of coins

        # play sound according to player results and write appropriate text
        if got_top_score and got_promoted:
            promotion_and_score_sound.play()
            self.texts.append(self.promotion_text)
            self.texts.append(self.top_score_text)
            self.texts.append(self.coins_reward_text)
        elif got_top_score:
            top_score_sound.play()
            self.texts.append(self.top_score_text)
        elif got_promoted:
            promotion_sound.play()
            self.texts.append(self.promotion_text)
            self.texts.append(self.coins_reward_text)
        else:
            fail_sound.play()
        if got_coins:
            self.texts.append(self.coins_collected_text)

    def event_handling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                game_erase()
                game_restart()
                self.switch_to_scene(GameScene())

    def update(self, pressed_keys):
        def button_action():
            game_erase()
            game_restart()
            self.switch_to_scene(GameScene())

        def button2_action():
            pygame.mixer.music.load('audio/menu_music.mp3')
            pygame.mixer.music.play(-1)
            self.switch_to_scene(MenuScene())

        self.button.on_click_action(lambda: button_action())
        self.button2.on_click_action(lambda: button2_action())

    def render(self):
        for text in self.texts:
            text.write(frame)
        for button in self.buttons:
            button.draw(frame)
            button.write(frame, self.try_again_font)
            button.draw_border(frame, WHITE)


# return a string saying if the fullscreen mode is on
def is_fullscreen():
    if display_mode == 0:
        return "NO"
    else:
        return "YES"


#  return current controls as a string
def get_current_controls():
    if controls[0] == pygame.K_w:
        return "WSAD"
    else:
        return "Arrows"


def get_current_rank():
    global current_rank
    if current_rank == 1:
        return functions.get_image('img/ranks/rank1.png').convert_alpha()
    elif current_rank == 2:
        return functions.get_image('img/ranks/rank2.png').convert_alpha()
    elif current_rank == 3:
        return functions.get_image('img/ranks/rank3.png').convert_alpha()
    elif current_rank == 4:
        return functions.get_image('img/ranks/rank4.png').convert_alpha()
    elif current_rank == 5:
        return functions.get_image('img/ranks/rank5.png').convert_alpha()
    elif current_rank == 6:
        return functions.get_image('img/ranks/rank6.png').convert_alpha()
    elif current_rank == 7:
        return functions.get_image('img/ranks/rank7.png').convert_alpha()
    elif current_rank == 8:
        return functions.get_image('img/ranks/rank8.png').convert_alpha()
    else:
        return functions.get_image('img/alien_cow.png').convert_alpha()


def update_top_score():
    global top_score, current_score
    if current_score > top_score:
        top_score = current_score
        save_data()
        return True


def update_total_coins():
    global total_coins, current_coins
    if current_coins > 0:
        total_coins += current_coins
        save_data()
        return True


# save all data to the file, save/backup progress
def save_data():
    global data, file
    data = [str(current_rank) + '\n', str(top_score) + '\n', str(current_exp) + '\n', str(current_controls) + '\n',
            str(music_volume) + '\n', str(sounds_volume) + '\n', str(display_mode) + '\n', str(total_coins) + '\n',
            "".join([str(x) for x in skins_owned])]
    # write everything
    with open('fonts/font_size.txt', 'w') as file:
        file.writelines(data)


# add gained exp to the current exp and save it, if player is up to promotion, promote
def check_if_promotion():
    global current_exp, current_score, exp_required_total, current_rank
    current_exp += current_score
    save_data()
    if current_exp >= exp_required_total:
        promote()
        return True


def promote():
    global current_exp, exp_required_total, current_rank, exp_required_total, total_coins
    current_exp -= exp_required_total
    current_rank += 1
    exp_required_total = int(999 * math.sqrt(math.pow(2, current_rank)))
    total_coins += 1
    save_data()


# game functions
def update_score_label(x, y):
    if not GameScene.player.has_shield:
        score_text = GameScene.score_font.render("Score: " + str(current_score), True, WHITE, BLACK)
    else:
        score_text = GameScene.score_font.render("Score: " + str(current_score), True, WHITE,
                                                 (65, 105, 225))
    frame.blit(score_text, (x, y))


def update_bullets_label(x, y):
    if not GameScene.player.has_laser:
        num_of_bullets_text = GameScene.score_font.render(
            "Bullets: " + str(GameScene.player.num_of_bullets), True,
            WHITE, BLACK)
    else:
        num_of_bullets_text = GameScene.score_font.render(
            "Bullets: " + str(GameScene.player.num_of_bullets), True,
            WHITE, (0, 150, 0))
    if 100 > GameScene.player.num_of_bullets > 9:
        frame.blit(num_of_bullets_text, (x - 10, y))
    elif 1000 > GameScene.player.num_of_bullets > 99:
        frame.blit(num_of_bullets_text, (x - 20, y))
    elif 10000 > GameScene.player.num_of_bullets > 999:
        frame.blit(num_of_bullets_text, (x - 30, y))
    else:
        frame.blit(num_of_bullets_text, (x, y))


def alert_wave_coming(seconds_left):
    if GameScene.is_alien_phase:
        wave_alert_text = GameScene.score_font.render(
            "Alien wall coming in " + str(seconds_left) + " seconds. Prepare yourself",
            True, WHITE,
            BLACK)
        frame.blit(wave_alert_text, (200, 570))
    else:
        wave_alert_text = GameScene.score_font.render(
            str(seconds_left) + " seconds left till end of the wave",
            True,
            WHITE,
            BLACK)
        frame.blit(wave_alert_text, (220, 570))


def game_over_label():
    game_over_text = GameScene.game_over_font.render("Game over!", True, WHITE, BLACK)
    frame.blit(game_over_text, (230, 260))


def game_erase():
    # remove characters and objects
    GameScene.player_sprite.empty()
    GameScene.aliens.empty()
    GameScene.collectables.empty()
    GameScene.bullets.empty()
    GameScene.enemy_bullets.empty()
    pygame.mixer.music.stop()
    # disable timers
    pygame.time.set_timer(GameScene.ALIEN_LVL2_RESPAWN, 0)
    pygame.time.set_timer(GameScene.ALIEN_LVL2_STOP, 0)
    # disable modes
    Alien.angry_mode = False
    GameScene.player.weapon_damaged = False


def game_restart():
    global current_score, map_score, current_coins
    current_score = 0
    current_coins = 0
    map_score = 0
    GameScene.player = Player([functions.get_image('img/spaceship.png').convert_alpha()], 370, 480, 3)
    GameScene.player_sprite.add(GameScene.player)
    GameScene.start_time = functions.get_current_time()
    GameScene.pause = True
    # reset timers
    pygame.time.set_timer(GameScene.ALIEN_LVL1_STOP, random.randint(40000, 60000))
    pygame.time.set_timer(GameScene.ALIEN_LVL1_RESPAWN, random.randint(200, 250))
    pygame.time.set_timer(GameScene.ALIEN_LVL3_RESPAWN, random.randint(4000, 10000))
    pygame.time.set_timer(GameScene.ALIEN_LVL4_RESPAWN, random.randint(10000, 20000))
    pygame.time.set_timer(GameScene.COLLECTABLE_AMMO_RESPAWN, random.randint(25000, 35000))
    pygame.time.set_timer(GameScene.COLLECTABLE_SHIELD_RESPAWN, random.randint(60000, 80000))
    pygame.time.set_timer(GameScene.COLLECTABLE_LASER_RESPAWN, random.randint(90000, 110000))
    pygame.time.set_timer(GameScene.COLLECTABLE_IMMUNITY_RESPAWN, random.randint(100000, 130000))
    pygame.time.set_timer(GameScene.COLLECTABLE_ANGRY_RESPAWN, random.randint(50000, 100000))
    pygame.time.set_timer(GameScene.COLLECTABLE_WEAPON_DAMAGED, random.randint(70000, 120000))
    functions.load_music('audio/soundtrack.mp3')
    pygame.mixer.music.play(-1)
    GameScene.game_is_active = True
    # place for testing static aliens


def get_ready():  # count 3 seconds before resuming the game, blit the counter
    counter = functions.get_current_time() - GameScene.start_time
    if counter >= pause_time:
        GameScene.pause = False
        pygame.mixer.music.unpause()
    else:
        counter_text = GameScene.counter_font.render(str((counter - pause_time) * -1), True, WHITE)
        frame.blit(counter_text, (370, 210))
        pygame.mixer.music.pause()


# count x seconds and then take off the immunity buff
def immunity_timer():
    counter = functions.get_current_time() - GameScene.start_time_immunity
    if counter >= immunity_time:
        GameScene.player.is_immune = False
    else:
        immunity_text = GameScene.game_over_font.render(
            "Immune for " + (str((counter - immunity_time) * -1) + " seconds"), True,
            WHITE)
        frame.blit(immunity_text, (frame_rect.left + 60, frame_rect.bottom - 150))


# count x seconds and then switch off the angry mode debuff
def angry_mode_timer():
    counter = functions.get_current_time() - GameScene.start_time_angry_mode
    if counter >= angry_mode_time:
        Alien.angry_mode = False
    else:
        angry_mode_text = GameScene.game_over_font.render(
            "Aliens are faster...  " + (str((counter - angry_mode_time) * -1)), True, RED)
        frame.blit(angry_mode_text, (frame_rect.left + 90, frame_rect.bottom - 80))


def weapon_damaged_timer():
    counter = functions.get_current_time() - GameScene.start_time_weapon_damaged
    if counter >= weapon_damaged_time:
        GameScene.player.weapon_damaged = False
    else:
        weapon_damaged_text = functions.get_font('fonts/Space_Galaxy.ttf', 40).render(
            "Fixing damaged weapon... " + (str((counter - weapon_damaged_time) * -1)), True, TOMATO)
        frame.blit(weapon_damaged_text, (frame_rect.centerx - 170, frame_rect.centery - 20))


def fix_alien_overlapping(alien):
    if any(alien.rect.colliderect(alien2.rect) for alien2 in GameScene.aliens if
           alien2 is not alien) or \
            any(alien.rect.colliderect(collectable.rect) for collectable in
                GameScene.collectables):
        if alien.level == 1:
            alien.health = 0


def check_if_alien_collide():
    alien_bullet_collision = pygame.sprite.groupcollide(GameScene.aliens,
                                                        GameScene.bullets, False, True,
                                                        pygame.sprite.collide_mask)
    for alien in alien_bullet_collision:
        explosion_sound.play()
        alien.health -= 1  # reduce alien's health by 1 if it collides with bullet

    if GameScene.laser.state == "moving":
        alien_laser_collision = pygame.sprite.spritecollide(GameScene.laser,
                                                            GameScene.aliens, False,
                                                            pygame.sprite.collide_mask)
        for alien in alien_laser_collision:
            explosion_sound.play()
            if (alien.health > 0):
                alien.health -= 1

    alien_player_collision = pygame.sprite.spritecollide(GameScene.player,
                                                         GameScene.aliens, True,
                                                         pygame.sprite.collide_mask)

    bullet_player_collision = pygame.sprite.spritecollide(GameScene.player, GameScene.enemy_bullets, True,
                                                          pygame.sprite.collide_mask)
    if (alien_player_collision or bullet_player_collision) and GameScene.player.has_shield:
        shield_broke_sound.play()
        GameScene.player.num_of_shields -= 1
        if GameScene.player.num_of_shields == 0:
            GameScene.player.has_shield = False
    else:
        if alien_player_collision or bullet_player_collision:
            GameScene.game_is_active = False
            game_erase()


def check_if_collectable_collide():
    collectable_player_collision = pygame.sprite.spritecollide(GameScene.player,
                                                               GameScene.collectables,
                                                               True,
                                                               pygame.sprite.collide_mask)
    if collectable_player_collision:
        collectable_collection_sound.play()
        for item in collectable_player_collision:
            if item.category == "ammo":  # get 1 ammo, you can shoot with ammo
                GameScene.player.num_of_bullets += 1
            elif item.category == "shield":  # get shield, it protects you from 1 hit
                GameScene.player.has_shield = True
                if GameScene.player.num_of_shields < 4:
                    GameScene.player.num_of_shields += 1
                    shield_collection_sound.play()
            elif item.category == "laser":  # get 1 laser, it destroys aliens in front of you
                GameScene.player.has_laser = True
                laser_collection_sound.play()
            elif item.category == "immunity":  # get immunity, you don't take damage for x seconds
                GameScene.player.is_immune = True
                GameScene.start_time_immunity = functions.get_current_time()
                immunity_collection_sound.play()
            elif item.category == "angry_mode":  # activate angry mode, all aliens move faster
                Alien.angry_mode = True
                GameScene.start_time_angry_mode = functions.get_current_time()
                angry_mode_collection_sound.play()
            elif item.category == "weapon_damaged":
                GameScene.player.weapon_damaged = True
                GameScene.start_time_weapon_damaged = functions.get_current_time()
                weapon_damaged_collection_sound.play()
            elif item.category == "coin":
                global current_coins
                current_coins += 1
                coin_collection_sound.play()


def show_collectables():
    if GameScene.player.has_shield:
        for i in range(GameScene.player.num_of_shields):
            frame.blit(functions.get_image('img/shield.png'), (34 * i + 10, 45))
    if GameScene.player.has_laser:
        frame.blit(functions.get_image('img/laser_gun.png'), (frame_rect.right - 95, 45))
    if GameScene.player.weapon_damaged:
        frame.blit(functions.get_image('img/weapon_damaged.png'), (frame_rect.right - 45, 45))
    if GameScene.player.is_immune:
        frame.blit(functions.get_image('img/immune.png'), (10, 90))
    if Alien.angry_mode:
        frame.blit(functions.get_image('img/angry_mode.png'), (frame_rect.right - 45, 90))
    if current_coins > 0:
        for i in range(current_coins):
            frame.blit(functions.get_image('img/coin3.png'), (28 * i + 90, 7))
