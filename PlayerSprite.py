import pygame
import random
import threading
import time
from Attacks import Bullet, Special_Attack
from moviepy.editor import *
from os import path
import spritesheet
from dimmer import Dimmer
from ObjectSprite import ObjectSprite2, Rock
from PIL import Image, ImageChops

# this is a class for player sprite object.
# IMAGES AND SOUNDS are dictionaries
# IMAGES= { "BSE_IMG" : vegeta_img ,...
# SOUNDS = { "KI" : ki_sound,...
# from mainDBZ import Lightning_Bolt, lightnings


vid_dir = path.join(path.dirname(__file__), 'vid')
channel1 = pygame.mixer.Channel(1)
channel2 = pygame.mixer.Channel(2)
channel3 = pygame.mixer.Channel(3)

channel1.set_volume(0.5)
channel2.set_volume(0.5)
channel3.set_volume(0.5)


def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()


# movie = pygame.movie.Movie('MELT.MPG')
# screen = pygame.display.set_mode(movie.get_size())
# movie_screen = pygame.Surface(movie.get_size()).convert()


class PlayerSpr(pygame.sprite.Sprite):
    BLACK = (0, 0, 0)

    def __init__(self, PLAYER, CHAR_NAME, SCREEN, HEIGHT, WIDTH, IMAGES, SOUNDS, VIDS, X_COR, Y_COR, GROUPS):
        pygame.sprite.Sprite.__init__(self)
        self.deflecting = False
        self.character_name = CHAR_NAME
        self.player = PLAYER
        self.base_img = IMAGES["BSE_IMG"]
        self.image = IMAGES["BSE_IMG"]
        self.shooting_img = IMAGES["SHOOT_IMG"]
        self.dmg_img = IMAGES["DMG_IMAGE"]
        self.fly_up_img = IMAGES["FLYUP"]
        self.fly_down_img = IMAGES["FLYDOWN"]
        self.fly_bck_img = IMAGES["FLYBACK"]
        self.fly_fwd_img = IMAGES["FLYFWD"]
        self.block_img = IMAGES["BLOCK"]
        self.bullet_img = IMAGES["BULLET_IMG"]
        self.transform_bg = IMAGES["BG"]
        self.SPattacks_img = IMAGES['SP_ATTACK']
        self.rock_imgs = IMAGES["ROCK"]
        self.lightning_img = IMAGES["LIGHTNING"]
        self.player_attack_imgs = IMAGES["PLAYER_ATTACK_IMGS"]
        self.image.set_colorkey(self.BLACK)  # black background
        self.rect = self.image.get_rect()
        self.rect.centerx = X_COR
        self.rect.bottom = Y_COR - 10
        self.speedx = 0
        self.current_health = 200
        self.current_power = 200
        self.target_health = 500
        self.target_power = 500
        self.health_bar_length = 300
        self.power_level_bar_length = 300
        self.maximum_power = 1000
        self.maximum_health = 1000
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.power_ratio = self.maximum_power / self.power_level_bar_length
        self.health_change_speed = 5
        self.power_change_speed = 5
        self.blocking = False
        self.screen = SCREEN
        self.height = HEIGHT
        self.width = WIDTH
        self.ki_sound = SOUNDS["KI"]
        self.trans_sound = SOUNDS["TSND"]
        self.landing_sound = SOUNDS["LNDSND"]
        self.flying_sound = SOUNDS["FLYSND"]
        self.special_sound = SOUNDS["SPSND"]
        self.allsprGRP = GROUPS["ALL_SPRITES"]
        self.bulletGRP = GROUPS["BULLETS"]
        self.specialsGRP = GROUPS["SPECIALS"]
        self.TFIMGS = IMAGES["TF_IMGS"]
        self.new_ss = IMAGES["TF_SS"]
        self.death_imgs = IMAGES["DEATH_IMGS"]
        self.death_snd = SOUNDS["DEATH_SND"]
        self.trans_vid = VIDS["TRANS_VID"]
        self.death_count = 0
        self.isFlipped = False
        if self.player == "Player1":
            self.isFlipped = True

    def set_isFlipped(self, isFlipped):
        self.isFlipped = isFlipped

    def get_damage(self, amount):
        # change image to vegeta_damage if he is not blocking
        if self.blocking == False:
            self.image = self.dmg_img

        self.image = self.dmg_img
        self.image.set_colorkey((0, 0, 0))

        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0
            return False
        return True

    def get_health(self, amount):
        if self.target_health > self.maximum_health:
            self.target_health -= amount
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health

    def power_bar(self):
        if self.player == "Player1":
            pygame.draw.rect(self.screen, (255, 0, 0), (10, 40, self.current_power / self.maximum_power, 25))
            pygame.draw.rect(self.screen, (255, 255, 255), (10, 40, self.power_level_bar_length, 25), 4)
        elif self.player == "Player2":
            pygame.draw.rect(self.screen, (255, 0, 0), (700, 40, self.current_power / self.maximum_power, 25))
            pygame.draw.rect(self.screen, (255, 255, 255), (700, 40, self.power_level_bar_length, 25), 4)

        pygame.display.flip()

    def basic_health(self):
        if self.player == "Player1":
            pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, self.target_health / self.health_ratio, 25))
            pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, self.health_bar_length, 25), 4)
        elif self.player == "Player2":
            pygame.draw.rect(self.screen, (255, 0, 0), (700, 10, self.target_health / self.health_ratio, 25))
            pygame.draw.rect(self.screen, (255, 255, 255), (700, 10, self.health_bar_length, 25), 4)
        # update screen
        pygame.display.flip()

    def update(self):
        self.advance_health()
        self.advance_power()
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        # if player is on the floor change image to base image
        self.image.set_colorkey((0, 0, 0))
        if self.rect.bottom >= self.height:
            self.image = self.base_img
            self.image.set_colorkey((0, 0, 0))

        if self.player == "Player1":
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_a]:
                self.fly_backward()
            if keystate[pygame.K_d]:
                self.fly_forward()
            # make player fly up and down8
            if keystate[pygame.K_w]:
                self.fly_up()
            if keystate[pygame.K_s]:
                self.fly_down()
            if keystate[pygame.K_r]:
                self.block()

        elif self.player == "Player2":
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.fly_backward()
            if keystate[pygame.K_RIGHT]:
                self.fly_forward()
            if keystate[pygame.K_UP]:
                self.fly_up()
            if keystate[pygame.K_DOWN]:
                self.fly_down()

        self.rect.x += self.speedx
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height

    def advance_health(self):
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0, 255, 0)
        if self.current_health < self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        health_bar_rect = pygame.Rect(10, 45, self.current_health / self.health_ratio, 25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 45, transition_width, 25)

        pygame.draw.rect(self.screen, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(self.screen, transition_color, transition_bar_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 45, self.health_bar_length, 25), 4)

    def advance_power(self):
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_power < self.target_power:
            self.current_power += self.power_change_speed
            transition_width = int((self.target_power - self.current_power) / self.power_ratio)
            transition_color = (0, 255, 0)
        if self.current_power < self.target_power:
            self.current_power -= self.power_change_speed
            transition_width = int((self.target_power - self.current_power) / self.power_ratio)
            transition_color = (255, 255, 0)

        power_bar_rect = pygame.Rect(10, 45, self.current_power / self.power_ratio, 25)
        transition_bar_rect = pygame.Rect(power_bar_rect.right, 45, transition_width, 25)

        pygame.draw.rect(self.screen, (255, 0, 0), power_bar_rect)
        pygame.draw.rect(self.screen, transition_color, transition_bar_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 45, self.power_level_bar_length, 25), 4)

    def shoot(self):
        self.shooting_img.set_colorkey((0, 0, 0))
        self.image = self.shooting_img
        self.image.set_colorkey((0, 0, 0))
        # play ki_sound
        self.ki_sound.play()
        # wait 2 seconds before creating bullet

        bullet = Bullet(self.rect.centerx, self.rect.top, self.isFlipped, self.bullet_img)

        self.allsprGRP.add(bullet)
        self.bulletGRP.add(bullet)
        # wait 1 second before returning to base image

    # def deflect(self):quit
    #     self.deflecting = True
    #     self.image = self.deflect_img
    #     self.image.set_colorkey((0, 0, 0))
    #     self.deflect_sound.play()
    #     self.deflect_timer = time.time()

    def flip_images(self):

        if self.isFlipped:
            self.isFlipped = False
        elif not self.isFlipped:
            self.isFlipped = True

        self.image = pygame.transform.flip(self.image, True, False)
        self.shooting_img = pygame.transform.flip(self.shooting_img, True, False)
        self.base_img = pygame.transform.flip(self.base_img, True, False)
        self.block_img = pygame.transform.flip(self.block_img, True, False)
        self.fly_fwd_img = pygame.transform.flip(self.fly_fwd_img, True, False)
        self.fly_bck_img = pygame.transform.flip(self.fly_bck_img, True, False)
        self.fly_up_img = pygame.transform.flip(self.fly_up_img, True, False)
        self.fly_down_img = pygame.transform.flip(self.fly_down_img, True, False)
        self.dmg_img = pygame.transform.flip(self.dmg_img, True, False)
        self.player_attack_imgs = [pygame.transform.flip(img, True, False) for img in self.player_attack_imgs]

    # create a function to fly up
    def fly_up(self):

        # play flying_sound by using the playmusic function

        # change image to vegeta_fly_up
        self.image = self.fly_up_img
        # remove black background on image
        self.image.set_colorkey(self.BLACK)
        self.rect.y -= 5
        if self.rect.y < 0:
            self.rect.y = 0

    # create a function to fly down
    def fly_down(self):
        # play flying_sound

        # change image to vegeta_fly_down only if player2 is not on the floor
        if self.rect.bottom != self.height - 10:
            self.image = self.fly_down_img
            self.image.set_colorkey(self.BLACK)
            self.rect.y += 5
            if self.rect.y > self.height:
                self.rect.y = self.height

        # else if player2 is on the floor, play landing sound
        else:
            # stop flying_sound
            # self.flying_sound.stop()
            self.landing_sound.play()
            self.image = self.base_img

    def fly_forward(self):
        self.image = self.fly_bck_img
        self.image.set_colorkey(self.BLACK)
        self.rect.x += 5
        if self.rect.x > self.width:
            self.rect.x = self.width

    def fly_backward(self):
        self.image = self.fly_fwd_img
        self.image.set_colorkey(self.BLACK)
        self.rect.x -= 5
        if self.rect.x < 0:
            self.rect.x = 0

    def walk_forward(self):
        self.image = self.fly_fwd_img
        self.image.set_colorkey(self.BLACK)
        self.rect.x += 5
        if self.rect.x > self.width:
            self.rect.x = self.width

    # create a function to block
    def block(self):
        self.blocking = True
        self.image = self.block_img
        self.image.set_colorkey(self.BLACK)

    def unblock(self):
        self.blocking = False
        self.image = self.image

    def vidPlayer(self, screen):
        self.vid_player.play()
        self.vid_player.set_display(screen)

    def videoClipPlayer(self, vid):
        vid.preview()

    # create a funtion to transform super saiyen into vegeta
    def transform(self):
        lightningSprite1 = ObjectSprite2(self.width - 400, self.height, 1, self.lightning_img)

        dim = Dimmer(keepalive=1)
        dim.dim(darken_factor=64, color_filter=(0, 0, 0))
        # self.videoClipPlayer(self.trans_vid)

        for i in range(0, 10):
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            time.sleep(0.1)
            self.screen.fill((100, 100, 100))
            pygame.display.flip()
            time.sleep(0.1)
        # loop through TFIMGS LIST
        center_x = self.width / 2
        center_y = self.height / 2
        channel1.play(self.trans_sound[0])
        count = 0
        # check if any sounds playi
        for img in self.TFIMGS:
            if channel1.get_busy() != True and count < 1:
                channel1.play(self.trans_sound[1])
                count = count + 1
            randomX = random.randint(1, 1000)
            img.set_colorkey(self.BLACK)
            self.screen.set_colorkey((0, 0, 0))
            self.screen.blit(self.transform_bg, (0, 0))
            self.screen.blit(self.transform_bg, (0, 0))
            self.screen.blit(img, (center_x, center_y))
            img.set_colorkey(self.BLACK)
            self.screen.blit(lightningSprite1.image, (randomX, 0))
            pygame.display.flip()  # flip screen 1
            time.sleep(2)
            for i in range(0, 10):
                self.screen.fill((0, 0, 0))
                pygame.display.flip()
                time.sleep(0.1)
                # fill gold color
                self.screen.fill((255, 255, 0))
                # invert the screen background image
                self.screen.set_colorkey((0, 0, 0))
                self.screen.blit(img, (center_x, center_y))
                pygame.display.flip()
                time.sleep(0.1)

            self.screen.fill((0, 0, 0))

    # loading new sprite sheet to be used for character transformation
    def reset_sprites(self, new_ss):

        if self.character_name == "Vegeta":
            self.base_img = new_ss.image_at((10, 2163, 83, 138))
            self.image = new_ss.image_at((107, 498, 70, 141))
            self.shooting_img = new_ss.image_at((450, 5935, 102, 136))
            self.dmg_img = new_ss.image_at((192, 6091, 73, 129))
            self.fly_up_img = new_ss.image_at((104, 1443, 62, 147))
            self.fly_down_img = new_ss.image_at((451, 1451, 58, 139))
            self.fly_bck_img = new_ss.image_at((10, 1879, 74, 118))
            self.fly_fwd_img = new_ss.image_at((103, 1775, 120, 77))
            self.block_img = new_ss.image_at((111, 1035, 81, 117))
        elif self.character_name == "Goku":
            self.base_img = new_ss.image_at((341, 189, 69, 162))
            self.image = new_ss.image_at((430, 188, 67, 163))
            self.shooting_img = new_ss.image_at((220, 3808, 102, 144))
            self.dmg_img = new_ss.image_at((10, 6490, 91, 139))
            self.fly_up_img = new_ss.image_at((129, 1144, 69, 154))
            self.fly_down_img = new_ss.image_at((514, 1141, 60, 157))
            self.fly_bck_img = new_ss.image_at((131, 1615, 106, 128))
            self.fly_fwd_img = new_ss.image_at((120, 1495, 136, 83))
            self.block_img = new_ss.image_at((100, 976, 63, 141))

    def death(self):
        self.death_snd.play()
        # loop through death images
        for img in self.death_imgs:
            self.screen.fill((0, 0, 0))
            self.screen.blit(img, (self.width / 2, self.height / 2))
            pygame.display.flip()
            time.sleep(0.1)
        # wait 3 seconds
        time.sleep(3)
        # play death sound

    def Special_Blast(self):


        if self.character_name == "Vegeta":
            pygame.display.flip()
            time.sleep(0.1)
            sp_attack = Special_Attack(self.rect.centerx, self.rect.midright, 1, self.SPattacks_img, self.player_attack_imgs, self.special_sound)
            self.allsprGRP.add(sp_attack)
            self.specialsGRP.add(sp_attack)
        elif self.character_name == "Goku":
            # time.sleep(5)
            # goku_SP_MP4 = VideoFileClip(vid_dir + '/gokuSP.mp4')
            # goku_SP_MP4.preview()
            self.special_sound.play()
            for i in range(len(self.player_attack_imgs)):
                self.screen.fill((0, 0, 0))

                self.image = self.player_attack_imgs[i]
                self.image.set_colorkey((0, 0, 0))
                self.screen.blit(self.image, (self.rect.x, self.rect.y))
                pygame.display.flip()
                time.sleep(0.6)


            sp_attack = Special_Attack(self.rect.centerx, self.rect.centery, 1, self.SPattacks_img,self.player_attack_imgs, self.special_sound)

            self.allsprGRP.add(sp_attack)
            self.specialsGRP.add(sp_attack)
        #
        # dim the screen


        # set screen to original size

        # time.sleep(5)
        # wait 30 seconds before playing the sound again




    def Special_Blast2(self):
        if self.character_name == "Goku":
            # dim the screen
            dim = Dimmer(keepalive=1)
            dim.dim(darken_factor=64, color_filter=(0, 0, 0))
            #

# create a function that plays music files
