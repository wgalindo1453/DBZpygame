import pygame
import random
import threading
import time
from Attacks import Bullet, Special_Attack
from moviepy.editor import *
from os import path


# this is a class for player sprite object.
# IMAGES AND SOUNDS are dictionaries
# IMAGES= { "BSE_IMG" : vegeta_img ,...
# SOUNDS = { "KI" : ki_sound,...


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
        self.SP1_img = IMAGES["SP_1"]
        self.SP2_img = IMAGES["SP_2"]
        self.SP3_img = IMAGES["SP_3"]
        self.SP4_img = IMAGES["SP_4"]
        self.SP5_img = IMAGES["SP_5"]
        self.SP6_img = IMAGES["SP_6"]
        self.SPattacks_img = IMAGES['SP_ATTACK']
        self.rock_imgs = IMAGES["ROCK"]
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

    # create a function to fly up
    def fly_up(self):
        # play flying_sound
        self.flying_sound.play()
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
        self.flying_sound.play()
        # change image to vegeta_fly_down only if player2 is not on the floor
        if self.rect.bottom != self.height - 10:
            self.image = self.fly_down_img
            self.image.set_colorkey(self.BLACK)
            self.rect.y += 5
            if self.rect.y > self.height:
                self.rect.y = self.height

        # else if player2 is on the floor, play landing sound
        else:
            #stop flying_sound
            self.flying_sound.stop()
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


        self.trans_sound.play()
        # make background  flicker while transforming
        center_x = self.width / 2
        center_y = self.height / 2
        # blit a black screen over the background to make it look like the background is fading out
        self.screen.blit(self.transform_bg, (0, 0))

        # for i in range(0, 10):
        #     screen.fill(BLACK)
        #     pygame.display.flip()
        #     time.sleep(0.1)
        #     screen.fill(WHITE)
        #     pygame.display.flip()
        #     time.sleep(0.1)

        # draw tj
        # set background to black
        self.screen.fill(self.BLACK)

        # show vegeta transform image on flip
        self.screen.blit(self.SP1_img, (center_x, center_y))
        # remove black background on image
        self.screen.set_colorkey(self.BLACK)
        # create lightning_bolt

        # draw lightning bolt on blits top center

        # remove black background on image
        self.screen.set_colorkey(self.BLACK)

        # update screen
        pygame.display.flip()
        # self.image.set_alpha(50)  <-- sets image to 50% transparent
        pygame.display.flip()
        time.sleep(2)
        self.screen.blit(self.SP2_img, (center_x, center_y))
        self.screen.set_colorkey((0, 0, 0))
        pygame.display.flip()
        time.sleep(2)
        self.screen.blit(self.SP2_img, (center_x, center_y))
        self.screen.set_colorkey(self.BLACK)
        pygame.display.flip()
        time.sleep(2)
        self.screen.blit(self.SP4_img, (center_x, center_y))
        self.screen.set_colorkey(self.BLACK)
        pygame.display.flip()
        time.sleep(2)
        self.screen.blit(self.SP5_img, (center_x, center_y))
        self.screen.set_colorkey(self.BLACK)
        pygame.display.flip()
        time.sleep(2)
        self.screen.blit(self.SP6_img, (center_x, center_y))
        self.screen.set_colorkey(self.BLACK)
        pygame.display.flip()
        time.sleep(2)

        # draw lightning bolt
        # lightning_bolt = Lightning_Bolt(WIDTH - 400, HEIGHT, 1)
        # all_sprites.add(lightning_bolt)
        # lightnings.add(lightning_bolt)

        # change images to vegeta_ssj1 through vegeta_ssj6

        # self.image = vegeta_transform1
        # self.image.set_colorkey(BLACK)
        # remove black background on image

        # wait 2 seconds before creating bullet
        time.sleep(2)
        # play transform_sound

    def Special_Blast(self):
        #
        # dim the screen


        # time.sleep(5)
        # play goku_SP_MP4
        #goku_SP_MP4 = VideoFileClip(vid_dir + '/gokuSP.mp4')
        #goku_SP_MP4.preview()
        # set screen to original size


        # time.sleep(5)
        # wait 30 seconds before playing the sound again

        sp_attack = Special_Attack(self.rect.centerx, self.rect.midright, 1, self.SPattacks_img, self.special_sound)

        self.allsprGRP.add(sp_attack)
        self.specialsGRP.add(sp_attack)

