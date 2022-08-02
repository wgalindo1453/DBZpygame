# This Class defines a sprite object that can be moved around on the screen.
# It derives from the pygame.sprite.Sprite class.
# The class defines the following methods:
# __init__(self, image, x, y)
# update(self) #overrides the Sprite class update method
# playSound(self) #plays the sound associated with the sprite
# holdPosition(self, x, y)  #holds the sprite in a fixed position
import pygame


class ObjectSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, object_img, snd_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = object_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = 0
        self.direction = direction
        self.snd = pygame.mixer.Sound(snd_path)
        self.voice = pygame.mixer.Channel(5)
        self.voice.play(self.snd)
        self.sp_img = object_img
        self.voice = pygame.mixer.Channel(5)
        self.voice.play(self.snd)

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
