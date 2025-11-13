import pygame, state
from settings import *
from utility import load_vertical_animation_sheet
from entity import Entity
from random import choice

class Player(Entity):
    def __init__(self, type, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        #stats from settings
        self.type = type
        self.stats = character_data[self.type]
        self.stats = {k : v for k, v in self.stats.items() if k != 'graphic'}
        self.max_stats = max_stats[self.type]
        self.upgrade_cost = upgrade_cost
        self.growth_rate = growth_rates[self.type]
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.damage = self.stats['attack']
        self.magic = self.stats['magic']
        self.exp = 100
                
        self.import_assets()
        self.image = self.animations['down'][0]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-10, HITBOX_OFFSET['player'])
        self.obstacle_sprites = obstacle_sprites
        self.state = 'down'

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon_switch_time = 0
        self.weapon_switch_cooldown = 0.1*1000
        self.is_switching_weapon = False
        self.current_weapon = list(weapon_data[self.type].keys())[self.weapon_index]

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.current_magic = list(magic_data[self.type].keys())[self.magic_index]
        self.is_switching_magic = False
        self.magic_switch_time = 0
        self.magic_switch_cooldown = 0.1*1000
        
        #attack timer
        self.is_attacking = False
        self.can_attack = True
        self.attack_anim_cooldown = weapon_data[self.type][self.current_weapon]['attack_time']
        self.attack_cooldown = weapon_data[self.type][self.current_weapon]['cooldown']
        self.attack_time = 0
        self.time_from_last_attack = 0
        #magic timer
        self.is_casting_magic = False
        self.magic_cooldown = 1*1000
        self.magic_time = 0
        self.time_from_last_magic = 0
        self.energy_recovery_timer = pygame.USEREVENT + 1
        self.magic_duration = 0
        self.affected_by_boost = False
        self.boost_value = None

        #damage timer
        self.vulnerable = True
        self.hit_time = 0
        self.invulnerablitity_duration = 0.5*1000

        

    def import_assets(self):
        move_animations = load_vertical_animation_sheet(f'./graphics/player/{self.type}/walk.png', TILE_SIZE, TILE_SIZE)
        idle_animations = load_vertical_animation_sheet(f'./graphics/player/{self.type}/idle.png', TILE_SIZE, TILE_SIZE)
        attack_animations = load_vertical_animation_sheet(f'./graphics/player/{self.type}/attack.png', TILE_SIZE, TILE_SIZE)
        self.animations = {
            'down' : move_animations[0],
            'up' : move_animations[1],
            'left' : move_animations[2],
            'right' : move_animations[3],
            'down_idle' : idle_animations[0],
            'up_idle' : idle_animations[1],
            'left_idle' : idle_animations[2],
            'right_idle' : idle_animations[3],
            'down_attack' : attack_animations[0],
            'up_attack' : attack_animations[1],
            'left_attack' : attack_animations[2],
            'right_attack' : attack_animations[3],
        }

        self.weapon_attack_sounds = (
            pygame.mixer.Sound('audio/slash.wav'),
            pygame.mixer.Sound('audio/slash2.wav'),
            pygame.mixer.Sound('audio/slash3.wav'),
            pygame.mixer.Sound('audio/slash4.wav'),
            pygame.mixer.Sound('audio/slash5.wav')
            )
        for sound in self.weapon_attack_sounds:
            sound.set_volume(0.4)
        self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
        self.hit_sound.set_volume(0.4)

    def input(self):
        if not self.is_casting_magic: 
            keys = pygame.key.get_pressed()
            #movement input
            if keys[pygame.K_a]:
                self.direction.x = -1
                if not self.is_attacking: self.state = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                if not self.is_attacking: self.state = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_w]:
                self.direction.y = -1
                if not self.is_attacking: self.state = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                if not self.is_attacking: self.state = 'down'
            else:
                self.direction.y = 0    

            #weapon switching
            if keys[pygame.K_SEMICOLON]:
                if not self.is_switching_weapon:
                    if self.weapon_index > 0:
                        self.weapon_index -= 1
                    else:
                        self.weapon_index = len(list(weapon_data[self.type].keys())) - 1
                    self.weapon_switch_time = pygame.time.get_ticks()
                    self.is_switching_weapon = True
            if keys[pygame.K_QUOTE] :
                if not self.is_switching_weapon:
                    if self.weapon_index < len(list(weapon_data[self.type].keys())) - 1:
                        self.weapon_index += 1
                    else:
                        self.weapon_index = 0
                    self.weapon_switch_time = pygame.time.get_ticks()
                    self.is_switching_weapon = True
            
            #magic switching
            if keys[pygame.K_l] :
                if not self.is_switching_magic:
                    if self.magic_index < len(list(magic_data[self.type].keys())) - 1:
                        self.magic_index += 1
                    else:
                        self.magic_index = 0
                    self.magic_switch_time = pygame.time.get_ticks()
                    self.is_switching_magic = True

            #attack input
            if keys[pygame.K_SLASH] and self.can_attack:
                self.is_attacking = True
                self.can_attack = False
                self.attack_time = pygame.time.get_ticks()
                self.frame_index = 0

                self.create_attack(self.current_weapon)
                choice(self.weapon_attack_sounds).play()
            #magic input
            if keys[pygame.K_PERIOD] and not self.is_attacking:
                cost = magic_data[self.type][self.current_magic]['cost']
                if cost <= self.energy:
                    self.is_casting_magic = True
                    self.magic_time = pygame.time.get_ticks()
                    self.frame_index = 0

                    style = self.current_magic
                    strength = magic_data[self.type][self.current_magic]['strength']                    
                    self.create_magic(style, strength, cost)

    def handle_events(self, event):
        if event.type == self.energy_recovery_timer and self.energy < self.stats['energy']:
            self.energy += 0.5*self.magic

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        #timers
        delta_attack = current_time - self.attack_time
        delta_magic = current_time - self.magic_time
        delta_switch_weapon = current_time - self.weapon_switch_time
        delta_switch_magic = current_time - self.magic_switch_time
        delta_hit = current_time - self.hit_time

        #to be used later for UI
        self.time_from_last_attack = 100*delta_attack // self.attack_cooldown if delta_attack <= self.attack_cooldown else 100
        self.time_from_last_magic = 100*delta_magic // self.magic_cooldown if delta_magic <= self.magic_cooldown else 100    

        if self.is_attacking:
            if delta_attack >= self.attack_anim_cooldown:
                self.is_attacking = False
                self.destroy_attack()
        if not self.can_attack:
            if delta_attack >= self.attack_cooldown:
                self.can_attack = True
        if self.is_casting_magic:
            if delta_magic >= self.magic_cooldown:
                self.is_casting_magic = False
        if self.is_switching_weapon:
            if delta_switch_weapon >= self.weapon_switch_cooldown:
                self.is_switching_weapon = False
        if self.is_switching_magic:
            if delta_switch_magic >= self.magic_switch_cooldown:
                self.is_switching_magic = False
        if not self.vulnerable:
            if delta_hit >= self.invulnerablitity_duration:
                self.vulnerable = True
        if self.affected_by_boost:
            if delta_magic >= self.magic_duration:
                self.affected_by_boost = False

        #remove when implementing UI
        #print(str(self.time_from_last_attack) + str(self.time_from_last_magic))
    
    def get_state(self):

        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.state and not 'attack' in self.state:
                self.state = self.state + '_idle'

        if self.is_attacking:
            if not 'attack' in self.state:
                if 'idle' in self.state:
                    self.state = self.state.replace('idle', 'attack')
                else:    
                    self.state = self.state + '_attack'
        else:
            if 'attack' in self.state:
                self.state = self.state.replace('_attack', '')

        if self.is_casting_magic:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.state:
                if 'idle' in self.state:
                    self.state = self.state.replace('idle', 'attack')
                else:    
                    self.state = self.state + '_attack'
        elif not self.is_attacking:
            if 'attack' in self.state:
                self.state = self.state.replace('_attack', '')

        if self.health <= 0:
            state.GAME_STATE = state.GameState.DEATH
            state.MENU_STATE = state.MenuState.DEATH

    def refresh_weapon_and_magic(self):
        self.current_weapon = list(weapon_data[self.type].keys())[self.weapon_index]
        self.attack_cooldown = weapon_data[self.type][self.current_weapon]['cooldown']
        self.attack_anim_cooldown = weapon_data[self.type][self.current_weapon]['attack_time']
        
        self.current_magic = list(magic_data[self.type].keys())[self.magic_index]
        self.magic_duration = magic_data[self.type][self.current_magic]['duration']

        if self.affected_by_boost:
            self.damage = self.stats['attack'] + self.boost_value
        else:
            self.damage = self.stats['attack']

    def animate(self):
        animation = self.animations[self.state]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            self.image.set_alpha(self.wave_value())
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.damage
        weapon_damage = weapon_data[self.type][self.current_weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        magic_damage = magic_data[self.type][self.current_magic]['strength']
        return base_damage + magic_damage
    
    def get_stat_by_index(self, index):
        return list(self.stats.values())[index]
    
    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def update(self):
        self.input()
        self.refresh_weapon_and_magic()
        self.get_state()
        self.move(self.stats['speed'])
        self.cooldowns()
        self.animate()
        
        

