import pygame
import time


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, isFlipped, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10
        self.isFlipped = isFlipped
        self.group = pygame.sprite.Group()
        self.group.add(self)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        if isFlipped == True:
            self.speedx = +10  # move right
        else:
            self.speedx = -10  # move left

    def update(self):
        self.rect.x += self.speedx
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Special_Attack(pygame.sprite.Sprite):
    def __init__(self, x, y, player_type, sp_IMG, player_imgs, sp_snd):
        pygame.sprite.Sprite.__init__(self)
        self.image = sp_IMG[0]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speedy = -10
        self.snd = sp_snd
        self.sp_img = sp_IMG
        self.player_imgs = player_imgs

        # pygame.mixer.set_num_channels(8)
        # time.sleep(3)
        # screen = pygame.display.set_mode((1000, 800))
        # pygame.display.flip()

        # self.image = sp_img[1]
        # #set background black
        # self.image.set_colorkey((0,0,0))
        self.voice = pygame.mixer.Channel(5)
        # self.voice.play(self.snd)

        # self.holdPosition(x, y)


        if player_type == 1:
            self.speedx = +10
        else:



            self.speedx = -10

    def playSound(self):
        self.snd.play()

    def holdPosition(self, x, y):
        self.rect.centery = y
        self.rect.centerx = x

    def update(self):
        #if it touches opponent, kill it



        self.rect.x += self.speedx
        # kill if it moves off the top of the screen
        while self.voice.get_busy():
            #loop through player images

                # self.rect = self.image.get_rect()
                # self.rect.midright = y
                # self.rect.centerx = x
                # self.speedy = -10
                # self.snd.play()
                # if self.speedx == +10:
                #     self.speedx = -10
                # else:
                #     self.speedx = +10
                # self.rect.x += self.speedx
                # # kill if it moves off the top of the screen
                # if self.rect.bottom < 0:
                #     self.kill()

            self.image = self.sp_img[0]
            self.image.set_colorkey((0, 0, 0))




        if self.rect.bottom < 0:
            self.kill()
