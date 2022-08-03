# This Class defines a sprite object that can be moved around on the screen.
# It derives from the pygame.sprite.Sprite class.
# The class defines the following methods:
# __init__(self, image, x, y)
# update(self) #overrides the Sprite class update method
# playSound(self) #plays the sound associated with the sprite
# holdPosition(self, x, y)  #holds the sprite in a fixed position
import pygame
import random
WIDTH = 1000
HEIGHT = 800

class ObjectSprite2(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, object_img, snd_path=""):
        pygame.sprite.Sprite.__init__(self)
        self.image = object_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = 0
        self.direction = direction
        # if snd_path is not none then no sound
        if snd_path is not "":
            self.snd = pygame.mixer.Sound(snd_path)
            self.voice = pygame.mixer.Channel(5)
            self.voice.play(self.snd)

        self.voice = pygame.mixer.Channel(5)
        self.sp_img = object_img

    def playSound(self):
        self.snd.play()

    def holdPosition(self, x, y):
        self.rect.midright = y
        self.rect.centerx = x

    def update(self):
        self.rect.x += self.speedx
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

    def set_position(self, x, y):
        self.rect.bottom = y
        self.rect.centerx = x


class Rock(pygame.sprite.Sprite):
    def __init__(self, img_rck):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_rck
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        # positon the rock at the bottom of the screen
        self.rect.y = HEIGHT - self.rect.height

        self.speedy = random.randrange(1, 5)
        # self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        # move the rock up the screen
        self.rect.y -= self.speedy
        # if the rock is off the top of the screen
        if self.rect.bottom < 0:
            # reset the rock to the bottom of the screen
            self.rect.y = HEIGHT - self.rect.height
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.speedy = random.randrange(1, 8)

        # if self.rect.top > HEIGHT + 10:
        #     self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        #     self.rect.y = random.randrange(-100, -40)
        #     self.speedy = random.randrange(1, 8)
