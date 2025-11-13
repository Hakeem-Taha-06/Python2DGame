import pygame
from settings import *
from utility import direction_to_vector
from random import randint, choice

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal' : pygame.mixer.Sound('audio/heal.wav'),
            'holy' : pygame.mixer.Sound('audio/holy.wav'),
            'fire' : (pygame.mixer.Sound('audio/fire.wav'),pygame.mixer.Sound('audio/fire2.wav'),pygame.mixer.Sound('audio/fire3.wav')),
            'boost' : pygame.mixer.Sound('audio/boost.wav'),
        }

    def heal(self, player, strength, cost, groups):
        strength += player.magic
        player.health += strength
        print(f'healed by {strength}')
        pos = player.rect.center
        self.animation_player.create_particles('effect', 'heal', pos, groups)
        self.animation_player.create_particles('effect', 'heal_aura', pos, groups)
        self.sounds['heal'].play()
        player.energy -= cost
        if player.health >= player.stats['health']:
            player.health = player.stats['health']

    def holy(self, player, strength, cost, groups):
        strength += player.magic
        pos = player.rect.center
        self.animation_player.create_particles('magic', 'holy', pos, groups)
        player.energy -= cost
        self.sounds['holy'].play()
    
    def fire(self, player, strength, cost, groups):
        strength += player.magic
        direction = direction_to_vector(player.state.split('_')[0])
        pos = player.rect.center
        for i in range(1,8):
            x_offset = i*direction.x*TILE_SIZE/2 + randint(-16, 16)
            y_offset = i*direction.y*TILE_SIZE/2 + randint(-16, 16)
            offset = pygame.math.Vector2(x_offset, y_offset)
            self.animation_player.create_particles('magic', 'fire', pos + offset, groups)    
        player.energy -= cost
        choice(self.sounds['fire']).play()
        
    def boost(self, player, strength, cost, groups):
        strength += player.magic
        player.affected_by_boost = True
        player.boost_value = strength
        pos = player.rect.center
        self.animation_player.create_particles('effect', 'boost', pos, groups)
        player.energy -= cost
        self.sounds['boost'].play()