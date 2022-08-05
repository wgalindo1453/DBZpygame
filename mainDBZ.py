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

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'Sound')
vid_dir = path.join(path.dirname(__file__), 'vid')
mus_dir = path.join(path.dirname(__file__), 'Music')
# create vegeta_dir under img_dir
vegeta_dir = path.join(img_dir, 'vegeta')
# create goku_dir under img_dir
goku_dir = path.join(img_dir, 'goku')
WIDTH = 1200
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
goku_ss = spritesheet.SpriteSheet('img/goku/gokuspritesheet.png')
goku_super_ss = spritesheet.SpriteSheet('img/goku/ss_goku_spritesheet.png')
channel0 = pygame.mixer.Channel(0)
game_state = 0


def show_splashscreen():
    """
    Show the splash screen.
    This is called once when the game is first started.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    splash_sound = pygame.mixer.Sound('Sound/takeeverythingback.mp3')
    channel0.play(splash_sound)
    pygame.mixer.music.set_volume(0.5)
    white = 250, 250, 250
    screen.fill(white)
    # Slowly fade the splash screen image from white to opaque.
    splash = pygame.image.load("img/splash.jpg").convert()
    for i in range(25):
        splash.set_alpha(i)
        screen.blit(splash, (90, 50))
        pygame.display.update()
        pygame.time.wait(100)

    pygame.mixer.fadeout(2000)
    screen.blit(splash, (90, 50))
    pygame.display.update()
    pygame.time.wait(1500)
    game_state = 0

    channel0.stop()


def open_menu():
    s0Option = range(5)
    is0 = 0
    game_state = 0
    """
    Main Menu
    """
    background_openning = pygame.image.load("img/splash.jpg").convert()
    black = 0, 0, 0
    screen.fill(black)
    screen.blit(background_openning, (-70, 0))
    my_font = pygame.font.SysFont("monospace", 65)
    bold_font = pygame.font.SysFont("monospace", 75, bold=True)
    player_vs_pc = my_font.render("Play Vs PC", 1, WHITE)
    player_vs_player = my_font.render("Play Vs Player2", 1, WHITE)
    options_word = my_font.render("Options", 1, WHITE)
    credits_word = my_font.render("Credits", 1, WHITE)
    quit_word = my_font.render("Quit", 1, WHITE)

    if s0Option[is0] == 0:
        player_vs_pc = bold_font.render("Play Vs Pc", 1, WHITE)
    if s0Option[is0] == 1:
        player_vs_player = bold_font.render("Play Vs Player2", 1, WHITE)
    if s0Option[is0] == 2:
        options_word = bold_font.render("Options", 1, WHITE)
    if s0Option[is0] == 3:
        credits_word = bold_font.render("Credits", 1, WHITE)
    if s0Option[is0] == 4:
        quit_word = bold_font.render("Quit", 1, WHITE)

    screen.blit(player_vs_pc, (310, 250))
    screen.blit(player_vs_player, (310, 320))
    screen.blit(options_word, (310, 390))
    screen.blit(credits_word, (310, 460))
    screen.blit(quit_word, (310, 530))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = previous_game_state
            if event.key == pygame.K_RETURN:
                if s0Option[is0] == 0:
                    player2.player_id = 2
                    game_state = 5
                    vs_pc = True
                    restart()
                if s0Option[is0] == 1:
                    game_state = 5
                    restart()
                    vs_pc = False
                    player2.player_id = 2
                if s0Option[is0] == 2:
                    previous_game_state = 0
                    game_state = 3
                if s0Option[is0] == 3:
                    previous_game_state = 0
                    game_state = 6
                if s0Option[is0] == 4:
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_DOWN:
                if s0Option[is0] < s0Option[-1]:
                    is0 += 1
            if event.key == pygame.K_UP:
                if s0Option[is0] > s0Option[0]:
                    is0 -= 1


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
player1_img = goku_ss.image_at((131, 271, 105, 109))
player2_img = pygame.image.load(path.join(vegeta_dir, "vegeta_normal.png")).convert()
rain_img = pygame.image.load(path.join(img_dir, "rain.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()

# VEGETA IMAGES
vegeta_fly_up = vegeta_ss.image_at((111, 1092, 62, 148))
vegeta_block = vegeta_ss.image_at((173, 965, 81, 102))
vegeta_dmg = vegeta_ss.image_at((5, 5927, 95, 114))
vegeta_fly_down = vegeta_ss.image_at((459, 1094, 58, 140))
vegeta_fwd = vegeta_ss.image_at((127, 1363, 120, 78))
vegeta_fly_bk = vegeta_ss.image_at((89, 1478, 80, 113))
vegeta_ki = vegeta_ss.image_at((437, 5222, 102, 136))

vegeta_transform1 = vegeta_ss.image_at((14, 4782, 65, 114))
vegeta_tf1 = vegeta_ss.image_at((457, 1745, 89, 144))
vegeta_tf10 = vegeta_ss.image_at((408, 7179, 98, 141))
vegeta_tf12 = vegeta_ss.image_at((612, 7179, 98, 141))
vegeta_tf13 = vegeta_ss.image_at((714, 7179, 98, 141))
vegeta_tf15 = vegeta_super_ss.image_at((875, 8263, 80, 140))
vegeta_tf_rects = [vegeta_tf1, vegeta_tf10, vegeta_tf12, vegeta_tf13, vegeta_tf15]
vegeta_ss_shoot = vegeta_ss.image_at((328, 5934, 102, 137))
vegeta_death1 = vegeta_ss.image_at((6, 6850, 97, 69))
vegeta_death2 = vegeta_ss.image_at((107, 6817, 74, 112))
vegeta_death3 = vegeta_ss.image_at((11, 6956, 131, 66))
vegeta_death4 = vegeta_ss.image_at((138, 6952, 88, 61))
vegeta_death5 = vegeta_ss.image_at((313, 6983, 129, 47))
vegeta_death_imgs = [vegeta_death1, vegeta_death2, vegeta_death3, vegeta_death4, vegeta_death5]
vegeta_tfimgs = [vegeta_tf1, vegeta_tf10, vegeta_tf12, vegeta_tf13, vegeta_tf15]
goku_bg = pygame.image.load(path.join(img_dir, "namek_bg_night.jpg")).convert()
vegeta_bg = pygame.image.load(path.join(vegeta_dir, "vegeta_bg.png")).convert()
lightning_img = pygame.image.load(path.join(img_dir, "lightning.png")).convert()
rock_img = pygame.image.load(path.join(img_dir, "rock1.png")).convert()
rock2_img = pygame.image.load(path.join(img_dir, "rock2.png")).convert()
rock3_img = pygame.image.load(path.join(img_dir, "rock3.png")).convert()
vegeta_bba_img1 = vegeta_ss.image_at((23, 4336, 65, 134))
vegeta_bba_img2 = vegeta_ss.image_at((144, 4339, 105, 131))
vegeta_bba_img3 = vegeta_ss.image_at((276, 4343, 98, 126))
vegeta_bba_img4 = vegeta_ss.image_at((388, 4336, 102, 131))
vegeta_bba_img5 = vegeta_ss.image_at((519, 4342, 69, 129))
vegeta_bba_img6 = vegeta_ss.image_at((1256, 4340, 80, 129))
vegeta_bba_imgs = [vegeta_bba_img1, vegeta_bba_img2, vegeta_bba_img3, vegeta_bba_img4, vegeta_bba_img5, vegeta_bba_img6]

# GOKU IMAGES
goku_fly_up = goku_ss.image_at((124, 837, 69, 154))
goku_fly_down = goku_ss.image_at((528, 842, 60, 149))
goku_fly_fwd = goku_ss.image_at((123, 1184, 143, 78))
goku_fly_bk = goku_ss.image_at((126, 1300, 106, 114))
goku_block = goku_ss.image_at((183, 679, 58, 125))
goku_dmg = goku_ss.image_at((0, 6688, 95, 137))
goku_ki = goku_ss.image_at((220, 3395, 102, 146))

goku_banner = goku_ss.image_at((868, 8815, 512, 64))
goku_splash = goku_ss.image_at((1124, 8883, 256, 256))
goku_tf1_kioten = goku_ss.image_at((1266, 8689, 105, 107))
goku_tf2_kioten = goku_ss.image_at((1136, 8689, 105, 107))
goku_tf3_kioten = goku_ss.image_at((1006, 8689, 105, 107))
goku_rush_kioten = goku_ss.image_at((1398, 8872, 136, 244))

goku_sp1 = goku_ss.image_at((406, 5759, 111, 108))
goku_sp2 = goku_ss.image_at((272, 5754, 109, 113))
goku_sp3 = goku_ss.image_at((141, 5746, 106, 121))
goku_sp4 = goku_ss.image_at((0, 5747, 116, 120))
goku_tf1 = goku_super_ss.image_at((10, 40, 80, 129))
goku_tf2 = goku_super_ss.image_at((100, 40, 87, 119))
goku_tf3 = goku_super_ss.image_at((217, 31, 73, 138))
goku_tf4 = goku_super_ss.image_at((310, 18, 92, 151))
goku_tf5 = goku_super_ss.image_at((422, 18, 92, 151))
goku_tf_rects = [goku_tf3, goku_tf4, goku_tf5]
goku_death1 = goku_ss.image_at((0, 7699, 117, 80))
goku_death2 = goku_ss.image_at((142, 7656, 92, 123))
goku_death3 = goku_ss.image_at((0, 7835, 138, 65))
goku_death4 = goku_ss.image_at((163, 7828, 118, 72))
goku_death5 = goku_ss.image_at((306, 7853, 151, 47))
goku_death_imgs = [goku_death1, goku_death2, goku_death3, goku_death4, goku_death5]
kamehameha_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball.png")).convert()
kamehameha2_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball2.png")).convert()
kamehameha3_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball3.png")).convert()
kamehameha4_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball4.png")).convert()
kamehameha5_img = pygame.image.load(path.join(goku_dir, "kamehamehafireball5.png")).convert()

goku_kmhma1_img = goku_ss.image_at((680, 5758, 113, 109))
goku_kmhma2_img = goku_ss.image_at((542, 5762, 113, 105))
goku_kmhma3_img = goku_ss.image_at((406, 5759, 111, 108))
goku_kmhma4_img = goku_ss.image_at((272, 5754, 109, 113))
goku_kmhma5_img = goku_ss.image_at((141, 5746, 106, 121))
goku_kmhma6_img = goku_ss.image_at((0, 5747, 116, 120))

goku_kmhma_imgs = [goku_kmhma1_img, goku_kmhma2_img, goku_kmhma3_img, goku_kmhma4_img, goku_kmhma5_img, goku_kmhma6_img]
KAMEHAMEHA_FIREBALLS = [kamehameha_img, kamehameha2_img, kamehameha3_img, kamehameha4_img, kamehameha5_img]

# Load all videos
goku_SP_MP4 = VideoFileClip(vid_dir + '/gokuSP.mp4')
vegeta_SP_MP4 = VideoFileClip(vid_dir + '/vegeta_trans.mp4')
vegeta_video = VideoFileClip(vid_dir + '/vegeta.mp4')

# create a dictionary of VIDEOS
G_VIDEOS = {'TRANS_VID': goku_SP_MP4}
V_VIDEOS = {'TRANS_VID': vegeta_video}

rock_images = [rock_img, rock2_img, rock3_img]
# create a dictionary of IMAGES for goku
IMAGES_G = {
    "BSE_IMG": player1_img,
    "PLAYER_ATTACK_IMGS": goku_kmhma_imgs,
    "KAMEHAMEHA": kamehameha_img,
    "BULLET_IMG": bullet_img,
    "SHOOT_IMG": goku_ki,
    "BLOCK": goku_block,
    "DMG_IMAGE": goku_dmg,
    "FLYFWD": goku_fly_bk,
    "FLYBACK": goku_fly_fwd,
    "FLYUP": goku_fly_up,
    "FLYDOWN": goku_fly_down,
    "BG": goku_bg,
    "TF_IMGS": goku_tf_rects,
    "TF_SS": goku_super_ss,
    "LIGHTNING": lightning_img,
    "ROCK": rock_images,
    "SP_ATTACK": KAMEHAMEHA_FIREBALLS,
    "DEATH_IMGS": goku_death_imgs,

}

# create a list of rock images

# create a dictionary for player1
IMAGES_P2 = {
    "BSE_IMG": player2_img,
    "rain": rain_img,
    "PLAYER_ATTACK_IMGS": vegeta_bba_imgs,
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
    "TF_SS": vegeta_super_ss,
    "LIGHTNING": lightning_img,
    "ROCK": rock_images,
    "SP_ATTACK": goku_sp1,
    "DEATH_IMGS": vegeta_death_imgs,

}
# create a dictionary for VIDS


# Load all game sounds
kamehameha_sound = pygame.mixer.Sound(path.join(snd_dir, 'kamehameha.mp3'))
ki_sound = pygame.mixer.Sound(path.join(snd_dir, 'ki_blast3.mp3'))
landing_sound = pygame.mixer.Sound(path.join(snd_dir, 'landing.mp3'))
vegeta_trans_sound = pygame.mixer.Sound(path.join(snd_dir, 'vegeta_transform.mp3'))
vegeta_trans_sound1 = pygame.mixer.Sound(path.join(snd_dir, 'Vegeta/trans.wav'))
vegeta_trans_sound2 = pygame.mixer.Sound(path.join(snd_dir, 'Vegeta/trans2.wav'))

vegeta_trans_sounds = [vegeta_trans_sound1, vegeta_trans_sound2]

flying_sound = pygame.mixer.music.load(path.join(snd_dir, "jump.mp3"))
goku_trans_sound = pygame.mixer.Sound(path.join(snd_dir, 'gokuyelling.mp3'))
vegeta_death_sound = pygame.mixer.Sound(path.join(snd_dir, "Vegeta/death.wav"))
goku_death_sound = pygame.mixer.Sound(path.join(snd_dir, "Goku/death.wav"))
goku_trans_sound1 = pygame.mixer.Sound(path.join(snd_dir, 'Goku/trans.wav'))
goku_trans_sound1 = pygame.mixer.Sound(path.join(snd_dir, 'Goku/trans2.wav'))
# Set total mixer channels to 4
goku_trans_sounds = [goku_trans_sound1, goku_trans_sound1]

bg_music = pygame.mixer.music.load(path.join(mus_dir, "bgmusic.mp3"))

VEGETA_SOUNDS = {
    "KI": ki_sound,
    "LNDSND": landing_sound,
    "TSND": vegeta_trans_sounds,
    "FLYSND": flying_sound,
    "SPSND": kamehameha_sound,
    "DEATH_SND": vegeta_death_sound,
}
GOKU_SOUNDS = {
    "KI": ki_sound,
    "LNDSND": landing_sound,
    "TSND": goku_trans_sounds,
    "FLYSND": flying_sound,
    "SPSND": kamehameha_sound,
    "DEATH_SND": goku_death_sound,
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
player1 = PlayerSpr("Player1", "Goku", screen, HEIGHT, WIDTH, IMAGES_G, GOKU_SOUNDS, G_VIDEOS, WIDTH - 1000, HEIGHT,
                    GROUPS)

player2 = PlayerSpr("Player2", "Vegeta", screen, HEIGHT, WIDTH, IMAGES_P2, VEGETA_SOUNDS, V_VIDEOS, WIDTH, HEIGHT,
                    GROUPS)
all_sprites.add(player1)
all_sprites.add(player2)
player1.flip_images()
player1.set_isFlipped(True)
show_splashscreen()
open_menu()

# for i in range(8):
#     enemy = Rain()
#     all_sprites.add(enemy)
#     enemies.add(enemy)

# Game Loop
running = True
P1_TF = False
P2_TF = False

pygame.mixer.music.play(-1)

while running:

    # keep player 1 facing right

    # keep loop running at the right speed
    clock.tick(FPS)
    player1.basic_health()
    player2.basic_health()
    player1.power_bar()
    player2.power_bar()
    # flipimages(player1) only at the start of the game

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
                player2.reset_sprites(vegeta_super_ss)
            # if t is pressed, then transform
            if event.key == pygame.K_t:
                player1.transform()
                player1.reset_sprites(goku_super_ss)
                player1.flip_images()
                player1.set_isFlipped(True)
                # if player 1 is on the left of player 2 then flipsprites

                # TODO:
                # call reset_player_ss() to set all sprites to next level

                # while rockcount is less than 10, transform player
            if event.key == pygame.K_RETURN:
                player2.shoot()
            if event.key == pygame.K_ESCAPE:
                running = False
        # if both players move across each other flip player images for both
        if player1.rect.x > player2.rect.x:
            # flip images only once per switch
            if not P1_TF:
                player1.flip_images()
                P1_TF = True  # set to true to prevent flipping again
            if not P2_TF:
                player2.flip_images()
                P2_TF = True  #
        else:
            if P1_TF:
                player1.flip_images()
                P1_TF = False
            if P2_TF:
                player2.flip_images()
                P2_TF = False

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

    if player2.target_health == 0:
        # only call death one time
        if player2.death_count == 0:
            player2.death()
            player2.death_count += 1

        player2.kill()

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
