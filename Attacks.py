import pygame
import time

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, player_type, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10
        self.player_type = player_type
        self.group = pygame.sprite.Group()
        self.group.add(self)
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


class Special_Attack(pygame.sprite.Sprite):
    def __init__(self, x, y, player_type, sp_IMG, sp_snd):
        pygame.sprite.Sprite.__init__(self)
        self.image = sp_IMG[0]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.midright = y
        self.rect.centerx = x
        self.speedy = -10
        self.snd = sp_snd
        self.sp_img = sp_IMG
        # pygame.mixer.set_num_channels(8)
     # time.sleep(3)
        # screen = pygame.display.set_mode((1000, 800))
        # pygame.display.flip()


        # self.image = sp_img[1]
        # #set background black
        # self.image.set_colorkey((0,0,0))
        self.voice = pygame.mixer.Channel(5)
        self.voice.play(self.snd)





                # self.holdPosition(x, y)

        if player_type == 1:
            self.speedx = +10
        else:
            self.speedx = -10



    def playSound(self):
        self.snd.play()

    def holdPosition(self, x ,y):
        self.rect.midright = y
        self.rect.centerx = x

    def update(self):

        self.rect.x += self.speedx
        # kill if it moves off the top of the screen
        while self.voice.get_busy():
            print("playing")
            self.image = self.sp_img[0]
            self.image.set_colorkey((0,0,0))

            print("playing")
            self.image = self.sp_img[2]
            print("playing")
            self.image = self.sp_img[3]
            print("playing")
            self.image = self.sp_img[4]
            print("playing")
            self.image = self.sp_img[4]
            print("playing")
            self.image = self.sp_img[4]
        if self.rect.bottom < 0:
            self.kill()


