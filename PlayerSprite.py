import pygame
import random
import threading
import time
from Attacks import Bullet, Special_Attack
from moviepy.editor import *
from os import path
from spritesheet import SpriteSheet
from dimmer import Dimmer
from ObjectSprite import ObjectSprite2, Rock


# this is a class for player sprite object.
# IMAGES AND SOUNDS are dictionaries
# IMAGES= { "BSE_IMG" : vegeta_img ,...
# SOUNDS = { "KI" : ki_sound,...
# from mainDBZ import Lightning_Bolt, lightnings

path = "Sound/jump.mp3"


def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()


class PlayerSpr(pygame.sprite.Sprite):
    BLACK = (0, 0, 0)

    def __init__(self, PLAYER, SCREEN, HEIGHT, WIDTH, IMAGES, SOUNDS, VIDS, X_COR, Y_COR, GROUPS):
        pygame.sprite.Sprite.__init__(self)
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
        self.image.set_colorkey(self.BLACK)  # black background
        self.rect = self.image.get_rect()
        self.rect.centerx = X_COR
        self.rect.bottom = Y_COR - 10
        self.speedx = 0
        self.current_health = 200
        self.target_health = 500
        self.maximum_health = 1000
        self.health_bar_length = 300
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 5
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

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        # if player is on the floor change image to base image
        if self.rect.bottom >= self.height:
            self.image = self.base_img

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

    def shoot(self):
        self.image = self.shooting_img
        self.image.set_colorkey(self.BLACK)
        # play ki_sound
        self.ki_sound.play()
        # wait 2 seconds before creating bullet
        if self.player == "Player1":
            bullet = Bullet(self.rect.centerx, self.rect.top, 1, self.bullet_img)

        elif self.player == "Player2":
            bullet = Bullet(self.rect.centerx, self.rect.top, 2, self.bullet_img)

        self.allsprGRP.add(bullet)
        self.bulletGRP.add(bullet)
        # wait 1 second before returning to base image

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


    # create a funtion to transform super saiyen into vegeta
    def transform(self):
        lightningSprite1 = ObjectSprite2(self.width - 400, self.height, 1, self.lightning_img)
        self.trans_sound.play()
        dim = Dimmer(keepalive=1)
        dim.dim(darken_factor=64, color_filter=(0,0,0))
        for i in range(0, 10):
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            time.sleep(0.1)
            self.screen.fill((100, 100, 100))
            pygame.display.flip()
            time.sleep(0.1)
        #loop through TFIMGS LIST
        center_x = self.width / 2
        center_y = self.height / 2
        for img in self.TFIMGS:
            randomX = random.randint(1, 1000)
            img.set_colorkey(self.BLACK)
            self.screen.set_colorkey((0, 0, 0))
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
                #fill gold color
                self.screen.fill((255, 255, 0))
                #invert the screen background image
                self.screen.set_colorkey((0, 0, 0))
                self.screen.blit(img, (center_x, center_y))
                pygame.display.flip()
                time.sleep(0.1)
            self.screen.fill((0, 0, 0))

        # blank_alpha = (0, 0, 0, 0)
        # self.SP1_img.set_colorkey(self.BLACK)
        # self.trans_sound.play()
        # # make background  flicker while transforming
        # center_x = self.width / 2
        # center_y = self.height / 2
        # # blit a black screen over the background to make it look like the background is fading out
        # self.screen.blit(self.transform_bg, (0, 0))
        #
        # for i in range(0, 10):
        #     self.screen.fill((0, 0, 0))
        #     pygame.display.flip()
        #     time.sleep(0.1)
        #     self.screen.fill((100, 100, 100))
        #     pygame.display.flip()
        #     time.sleep(0.1)
        # dim=Dimmer(keepalive=1)
        # dim.dim(darken_factor=64, color_filter=(0,0,0))
        # self.screen.blit(self.SP1_img, (center_x, center_y))
        # self.SP1_img.set_colorkey(self.BLACK)
        # # flip the screen
        # pygame.display.flip()
        # self.screen.fill((0, 0, 0, 0))
        # self.screen.blit(self.transform_bg, (0, 0))
        # self.screen.blit(self.SP1_img, (center_x, center_y))
        # #create Rock object and add to allsprGRP
        # #grab random rock from rock_imgs list
        #
        #
        # #blits rock to screen
        # #create a group for rocks
        # self.rocksGRP = pygame.sprite.Group()
        #
        # #show rocks on screen
        # self.rocksGRP.draw(self.screen)
        #
        #
        # # set lightning_bolt to be at top left of screen
        # self.screen.blit(lightningSprite0.image, (0, 0))
        # # update screen
        # pygame.display.flip()
        # # remove black background on image
        # self.screen.set_colorkey(self.BLACK)
        # # update screen
        # pygame.display.flip()  # screen flip 0
        # # self.image.set_alpha(50)  <-- sets image to 50% transparent
        # time.sleep(2)
        # self.screen.fill((0, 0, 0, 0))
        # #create Rock sprite
        # self.screen.blit(self.transform_bg, (0, 0))
        #
        #
        # self.SP2_img.set_colorkey(self.BLACK)
        # self.screen.blit(self.SP2_img, (center_x, center_y))
        # self.screen.set_colorkey((0, 0, 0))
        # self.screen.blit(lightningSprite1.image, (250, 0))
        # pygame.display.flip()  # flip screen 1
        # time.sleep(2)
        # self.screen.fill((0, 0, 0, 0))
        # self.screen.blit(self.transform_bg, (0, 0))
        # self.SP3_img.set_colorkey(self.BLACK)
        # self.screen.blit(self.SP3_img, (center_x, center_y))
        # self.screen.set_colorkey((0, 0, 0))
        # lightningSprite2.image.set_alpha(50)
        # self.screen.blit(lightningSprite2.image, (250, 0))
        # self.screen.blit(lightningSprite2.image, (450, 0))
        # self.screen.set_colorkey(self.BLACK)
        # pygame.display.flip()  # flip screen 0 and 2
        # time.sleep(2)
        # self.screen.fill((0, 0, 0, 0))
        # self.screen.blit(self.transform_bg, (0, 0))
        # self.SP4_img.set_colorkey(self.BLACK)
        # self.screen.blit(self.SP4_img, (center_x, center_y))
        # self.screen.set_colorkey((0, 0, 0))
        # lightningSprite3.image.set_alpha(50)
        # self.screen.blit(lightningSprite3.image, (460, 0))
        # self.screen.blit(lightningSprite3.image, (800, 0))
        # self.screen.set_colorkey(self.BLACK)
        # pygame.display.flip()  # flip screen 0 and 3
        # time.sleep(2)
        # self.screen.fill((0, 0, 0, 0))
        # self.screen.blit(self.transform_bg, (0, 0))
        # self.SP5_img.set_colorkey(self.BLACK)
        # self.screen.blit(self.SP5_img, (center_x, center_y))
        # self.screen.set_colorkey((0, 0, 0))
        # lightningSprite4.image.set_alpha(50)
        # self.screen.blit(lightningSprite4.image, (460, 0))
        # self.screen.blit(lightningSprite4.image, (800, 0))
        # self.screen.set_colorkey(self.BLACK)
        # pygame.display.flip()  # flip screen 0 and 4
        # time.sleep(2)
        # self.screen.fill((0, 0, 0, 0))
        # self.screen.blit(self.transform_bg, (0, 0))
        # self.SP6_img.set_colorkey(self.BLACK)
        # self.screen.blit(self.SP6_img, (center_x, center_y))
        # self.screen.set_colorkey((0, 0, 0))
        # lightningSprite5.image.set_alpha(50)
        # self.screen.blit(lightningSprite5.image, (160, 0))
        # self.screen.blit(lightningSprite5.image, (500, 0))
        # self.screen.set_colorkey(self.BLACK)
        # pygame.display.flip()  # flip screen 0 and 5
        # time.sleep(2)



    def Special_Blast(self):
        #
        # dim the screen

        # time.sleep(5)
        # play goku_SP_MP4
        # goku_SP_MP4 = VideoFileClip(vid_dir + '/gokuSP.mp4')
        # goku_SP_MP4.preview()
        # set screen to original size

        # time.sleep(5)
        # wait 30 seconds before playing the sound again

        sp_attack = Special_Attack(self.rect.centerx, self.rect.midright, 1, self.SPattacks_img, self.special_sound)

        self.allsprGRP.add(sp_attack)
        self.specialsGRP.add(sp_attack)

# create a function that plays music files
