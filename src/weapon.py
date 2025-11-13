import pygame
from settings import TILE_SIZE
from utility import import_image_from_folder

class Weapon(pygame.sprite.Sprite):
    def __init__(self, owner, groups, type):
        super().__init__(groups)
        self.owner = owner
        self.direction = self.owner.state.split('_')[0]
        self.sprite_type = 'weapon'
        
        #graphic
        image_path = f'./graphics/weapons/{type}/{self.direction}.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        
        #placement
        if self.direction == 'right':
            self.rect = self.image.get_rect(midleft = self.owner.rect.midright+pygame.Vector2(0,16))
        elif self.direction == 'left':
            self.rect = self.image.get_rect(midright = self.owner.rect.midleft+pygame.Vector2(0,16))
        elif self.direction == 'up':
            self.rect = self.image.get_rect(midbottom = self.owner.rect.midtop+pygame.Vector2(-12,0))
        elif self.direction == 'down':
            self.rect = self.image.get_rect(midtop = self.owner.rect.midbottom+pygame.Vector2(-8,0))

    def update(self):
        if self.direction == 'right':
            self.rect.midleft = self.owner.rect.midright+pygame.math.Vector2(0,16)
        elif self.direction == 'left':
            self.rect.midright = self.owner.rect.midleft+pygame.math.Vector2(0,16)
        elif self.direction == 'up':
            self.rect.midbottom = self.owner.rect.midtop+pygame.math.Vector2(-12,0)
        elif self.direction == 'down':
            self.rect.midtop = self.owner.rect.midbottom+pygame.math.Vector2(-8,0)


