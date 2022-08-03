import pygame
import random
from PlayerSprite import PlayerSpr
from dimmer import Dimmer
import threading
import time
import spritesheet
from moviepy.editor import *
from os import path
from ObjectSprite import Rock

# show vegeta transform image on flip with a black background
# ss = SpriteSheet('img/vegeta/vegetaspritesheet.png')

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'Sound')
vid_dir = path.join(path.dirname(__file__), 'vid')
mus_dir = path.join(path.dirname(__file__), 'Music')
# create vegeta_dir under img_dir
vegeta_dir = path.join(img_dir, 'vegeta')
# create goku_dir under img_dir
goku_dir = path.join(img_dir, 'goku')
WIDTH = 1000
HEIGHT = 800
FPS = 80

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)  # (frequency, size, channels, buffer)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DBZ")
clock = pygame.time.Clock()

vegeta_ss = spritesheet.SpriteSheet('img/vegeta/vegetaspritesheet.png')
vegeta_super_ss = spritesheet.SpriteSheet('img/vegeta/ss_vegeta_spritesheet.png')



# create a class for lightning bolt
class Lightning_Bolt(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = lightning_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speedy = 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, player_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        if player_type == 1:
            self.speedx = +10
        else:
            self.speedx = -10

    def update(self):
        self.rect.x += self.speedx
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


# create a Kamehameha class
class Kamehameha(pygame.sprite.Sprite):
    def __init__(self, x, y, player_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = kamehameha_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        if player_type == 1:
            self.speedx = +10
        else:
            self.speedx = -10

    def update(self):
        self.rect.x += self.speedx
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


# create a function that will return a return random rock image
def get_random_rock_img():
    rock_img = random.choice(rock_images)
    return rock_img


# Load all game graphics
background = pygame.image.load(path.join(img_dir, "namek.png")).convert()
background_rect = background.get_rect()
player1_img = pygame.image.load(path.join(goku_dir, "goku_base.png")).convert()
player2_img = pygame.image.load(path.join(vegeta_dir, "vegeta_normal.png")).convert()
rain_img = pygame.image.load(path.join(img_dir, "rain.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()

kamehameha_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball.png")).convert()
kamehameha2_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball2.png")).convert()
kamehameha3_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball3.png")).convert()
kamehameha4_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball4.png")).convert()
kamehameha5_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball5.png")).convert()

KAMEHAMEHA_FIREBALLS = [kamehameha_img, kamehameha2_img, kamehameha3_img, kamehameha4_img, kamehameha5_img]

vegeta_fly_up = pygame.image.load(path.join(vegeta_dir, "vegeta_fly_up.png")).convert()
vegeta_block = pygame.image.load(path.join(vegeta_dir, "vegeta_block.png")).convert()
vegeta_dmg = pygame.image.load(path.join(vegeta_dir, "vegeta_damage.png")).convert()
vegeta_fly_down = pygame.image.load(path.join(vegeta_dir, "vegeta_fly_down.png")).convert()
vegeta_fwd = pygame.image.load(path.join(vegeta_dir, "vegeta_forward.png")).convert()
vegeta_fly_bk = pygame.image.load(path.join(vegeta_dir, "vegeta_fly_back.png")).convert()
vegeta_ki = pygame.image.load(path.join(vegeta_dir, "vegeta_ki.png")).convert()
vegeta_transform1 = pygame.image.load(path.join(vegeta_dir, "vegeta_trans1.png")).convert()
lightning_img = pygame.image.load(path.join(img_dir, "lightning.png")).convert()
rock_img = pygame.image.load(path.join(img_dir, "rock1.png")).convert()
rock2_img = pygame.image.load(path.join(img_dir, "rock2.png")).convert()
rock3_img = pygame.image.load(path.join(img_dir, "rock3.png")).convert()
vegeta_tf1 = vegeta_ss.image_at((457, 1745, 89, 144))
vegeta_tf2 = vegeta_ss.image_at((366, 1745, 89, 144))
vegeta_tf3 = vegeta_ss.image_at((275, 1745, 89, 144))
vegeta_tf4 = vegeta_ss.image_at((184, 1745, 89, 144))
vegeta_tf5 = vegeta_ss.image_at((93, 1745, 89, 144))
vegeta_tf6 = vegeta_ss.image_at((0, 1745, 89, 144))
vegeta_tf7 = vegeta_ss.image_at((102, 7179, 98, 141))
vegeta_tf8 = vegeta_ss.image_at((204, 7179, 98, 141))
vegeta_tf9 = vegeta_ss.image_at((306, 7179, 98, 141))
vegeta_tf10 = vegeta_ss.image_at((408, 7179, 98, 141))
vegeta_tf11 = vegeta_ss.image_at((510, 7179, 98, 141))
vegeta_tf12 = vegeta_ss.image_at((612, 7179, 98, 141))
vegeta_tf13 = vegeta_ss.image_at((714, 7179, 98, 141))
vegeta_tf14 = vegeta_ss.image_at((816, 7179, 98, 141))
vegeta_tf15 = vegeta_super_ss.image_at((875, 8263, 80, 140))
vegeta_ss_shoot = vegeta_ss.image_at((328, 5934, 102, 137))
vegeta_bg = pygame.image.load(path.join(vegeta_dir, "vegeta_bg.png")).convert()
goku_block = pygame.image.load(path.join(goku_dir, "goku_block.png")).convert()
goku_dmg = pygame.image.load(path.join(goku_dir, "goku_dmg.png")).convert()
goku_fly_fwd = pygame.image.load(path.join(goku_dir, "goku_fly_fwd.png")).convert()
goku_fly_bk = pygame.image.load(path.join(goku_dir, "goku_fly_back.png")).convert()
goku_fly_up = pygame.image.load(path.join(goku_dir, "goku_fly_up.png")).convert()
goku_fly_down = pygame.image.load(path.join(goku_dir, "goku_fly_down.png")).convert()
goku_ki = pygame.image.load(path.join(goku_dir, "goku_ki.png")).convert()
goku_sp1 = pygame.image.load(path.join(goku_dir, "gokusp1.png")).convert()
goku_sp2 = pygame.image.load(path.join(goku_dir, "gokusp2.png")).convert()

vegeta_tfimgs = [vegeta_tf1,vegeta_tf10, vegeta_tf12,vegeta_tf13, vegeta_tf15]

# Load all videos
goku_SP_MP4 = VideoFileClip(vid_dir + '/gokuSP.mp4')

# create a dictionary of VIDEOS
VIDEOS = {'gokuSP': goku_SP_MP4}
rock_images = [rock_img, rock2_img, rock3_img]
# create a dictionary of IMAGES for goku
IMAGES_G = {
    "BSE_IMG": player1_img,
    "KAMEHAMEHA": kamehameha_img,
    "BULLET_IMG": bullet_img,
    "SHOOT_IMG": goku_ki,
    "BLOCK": goku_block,
    "DMG_IMAGE": goku_dmg,
    "FLYFWD": goku_fly_bk,
    "FLYBACK": goku_fly_fwd,
    "FLYUP": goku_fly_up,
    "FLYDOWN": goku_fly_down,
    "BG": vegeta_bg,
    "TF_IMGS": vegeta_tfimgs,
    "LIGHTNING": lightning_img,
    "ROCK": rock_images,
    "SP_ATTACK": KAMEHAMEHA_FIREBALLS,

}

# create a list of rock images

# create a dictionary for player1
IMAGES_P2 = {
    "BSE_IMG": player2_img,
    "rain": rain_img,
    "BULLET_IMG": bullet_img,
    "FLYUP": vegeta_fly_up,
    "FLYBACK": vegeta_fly_bk,
    "DMG_IMAGE": vegeta_dmg,
    "FLYDOWN": vegeta_fly_down,
    "FLYFWD": vegeta_fwd,
    "SHOOT_IMG": vegeta_ki,
    "BLOCK": vegeta_block,
    "BG": vegeta_bg,
    "TF_IMGS": vegeta_tfimgs,
    "LIGHTNING": lightning_img,
    "ROCK": rock_images,
    "SP_ATTACK": goku_sp1,

}
# create a dictionary for VIDS


# Load all videos

# Load all game sounds
kamehameha_sound = pygame.mixer.Sound(path.join(snd_dir, 'kamehameha.mp3'))
ki_sound = pygame.mixer.Sound(path.join(snd_dir, 'ki_blast3.mp3'))
landing_sound = pygame.mixer.Sound(path.join(snd_dir, 'landing.mp3'))
vegeta_trans_sound = pygame.mixer.Sound(path.join(snd_dir, 'vegeta_transform.mp3'))
flying_sound = pygame.mixer.music.load(path.join(snd_dir, "jump.mp3"))

# load background music
bg_music = pygame.mixer.music.load(path.join(mus_dir, "bgmusic.mp3"))

SOUNDS = {
    "KI": ki_sound,
    "LNDSND": landing_sound,
    "TSND": vegeta_trans_sound,
    "FLYSND": flying_sound,
    "SPSND": kamehameha_sound,
}
# create all groups


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
kamehamehas = pygame.sprite.Group()
lightnings = pygame.sprite.Group()

GROUPS = {
    "ALL_SPRITES": all_sprites,
    "ROCKS": rocks,
    "BULLETS": bullets,
    "SPECIALS": kamehamehas,
}

# add
player1 = PlayerSpr("Player1", screen, HEIGHT, WIDTH, IMAGES_G, SOUNDS, VIDEOS, WIDTH - 1000, HEIGHT, GROUPS)

player2 = PlayerSpr("Player2", screen, HEIGHT, WIDTH, IMAGES_P2, SOUNDS, VIDEOS, WIDTH, HEIGHT, GROUPS)
all_sprites.add(player1)
all_sprites.add(player2)

# for i in range(8):
#     enemy = Rain()
#     all_sprites.add(enemy)
#     enemies.add(enemy)

# Game Loop
running = True
P1_TF = false
P2_TF = false
# start background music
pygame.mixer.music.play(-1)
while running:

    # keep loop running at the right speed
    clock.tick(FPS)
    player1.basic_health()
    player2.basic_health()

    #    previous_time = pygame.time.get_ticks()
    # process input (events )
    for event in pygame.event.get():
        # check for closing window [X]
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # if the k key is pressed, then kamehameha blast
            if event.key == pygame.K_k:
                player1.Special_Blast()

            if event.key == pygame.K_SPACE:
                player1.shoot()

            # if the l key is held down, then block
            keys = pygame.key.get_pressed()
            if keys[pygame.K_l]:
                player2.block()
            if keys[pygame.K_r]:
                player1.block()
            # if l key is released, then unblock
            if not keys[pygame.K_l]:
                player2.unblock()
            if not keys[pygame.K_r]:
                player1.unblock()
            if event.key == pygame.K_p:
                dim = Dimmer(keepalive=1)
                dim.dim(darken_factor=64, color_filter=(0, 0, 0))
                time.sleep(2)
                player2.transform()
                #TODO:
                # call reset_player_ss() to set all sprites to next level

                #while rockcount is less than 10, transform player
            if event.key == pygame.K_RETURN:
                player2.shoot()
            if event.key == pygame.K_ESCAPE:
                running = False

    # update game
    all_sprites.update()
    # check to see if a bullet hit an enemy
    # hitList = pygame.sprite.groupcollide(player, bullets, True, True)
    # for kill in hitList:
    #     enemy = Rain()
    #     all_sprites.add(enemy)
    #     enemies.add(enemy)

    # check to see if a enemy hit the player
    hits = pygame.sprite.spritecollide(player1, bullets, False)
    if player1.target_health == 0:
        player1.kill()
        print("Player 1  has died")
    if player2.target_health == 0:
        player2.kill()
        print("Player 2 has died")
    if hits:
        if player1.blocking:
            player1.block()
        else:
            player1.get_damage(5)

    hits2 = pygame.sprite.spritecollide(player2, bullets, False)
    if hits2:
        if player2.blocking:
            player2.block()

        else:
            player2.get_damage(5)

    # Draw /render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()
# stop background music
pygame.mixer.music.stop()
pygame.quit()
