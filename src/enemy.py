import pygame
from settings import*
from entity import Entity
from utility import load_horizontal_animation_sheet

class Enemy(Entity):
    def __init__(self, name, type, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        super().__init__(groups)

        self.sprite_type = 'enemy'
        self.type = type
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        
        #graphics
        self.icon = pygame.image.load(f'graphics/enemies/{name}/icon.png')
        self.import_assets(name)
        self.state = 'idle'
        self.image = self.animations[self.state][self.frame_index]
        
        #movement
        if self.type == 'small':
            self.rect = self.image.get_rect(topleft = pos)
            self.hitbox = self.rect.inflate(0, -10)
        elif self.type == 'big':
            self.rect = self.image.get_rect(center = pos)
            self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.name = name
        self.stats = monster_data[name]
        self.health = self.stats['health']
        self.speed = self.stats['speed']
        self.damage = self.stats['damage']
        self.exp = self.stats['exp']
        self.resistance = self.stats['resistance']
        self.notice_radius = self.stats['notice_radius']
        self.attack_radius = self.stats['attack_radius']
        self.attack_type = self.stats['attack_type']
        self.attack_sound = pygame.mixer.Sound(self.stats['attack_sound'])
        self.attack_sound.set_volume(0.4)
        self.death_sound = pygame.mixer.Sound(self.stats['death_sound'])
        self.death_sound.set_volume(0.4)

        #player interaction
        self.can_attack = True
        self.attack_cooldown = 0.5*1000
        self.attack_time = 0
        self.vulnerable = True
        self.hit_time = 0
        self.invulnerablitity_duration = 0.5*1000

    def import_assets(self, name):
        width = self.icon.get_width()
        height = self.icon.get_height()
        move_animation = load_horizontal_animation_sheet(f'graphics/enemies/{name}/walk_sheet.png', width, height)
        idle_animation = load_horizontal_animation_sheet(f'graphics/enemies/{name}/idle_sheet.png', width, height)
        charge_animation = load_horizontal_animation_sheet(f'graphics/enemies/{name}/charge_sheet.png', width, height)
        attack_animation = load_horizontal_animation_sheet(f'graphics/enemies/{name}/attack_sheet.png', width, height)
        self.animations = {
            'move' : move_animation,
            'idle' : idle_animation,
            'charge' : charge_animation,        
            'attack' : attack_animation,       
        }

    def get_player_distance_direction(self, player):
        player_vec = pygame.math.Vector2(player.rect.center)
        enemy_vec = pygame.math.Vector2(self.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack and self.vulnerable:
            if self.state != 'attack':
                self.frame_index = 0
            self.state = 'attack'
        elif distance <= self.notice_radius:
            self.state = 'move'
        else:
            self.state = 'idle'
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        #timers
        delta_attack = current_time - self.attack_time
        delta_hit = current_time - self.hit_time
        if not self.can_attack:
            if delta_attack >= self.attack_cooldown:
                self.can_attack = True 
        if not self.vulnerable:
            if delta_hit >= self.invulnerablitity_duration:
                self.vulnerable = True
    
    def actions(self, player):
        if self.state == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.damage, self.attack_type, self.attack_sound)
        elif self.state == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
   
    def animate(self):
        animation = self.animations[self.state]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.state == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        if not self.vulnerable:
            self.image.set_alpha(self.wave_value())
        else:
            self.image.set_alpha(255)

    def take_damage(self, player, attack):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack.sprite_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
                player.hit_sound.play()
            elif attack.sprite_type == 'magic':
                self.health -= player.get_full_magic_damage()
                player.hit_sound.play()
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
    
    def check_death(self):
        if self.health <= 0:
            self.trigger_death_particles(self.rect.center, self.name)
            self.death_sound.play()
            self.add_exp(self.exp)
            self.kill()

    def update(self):
        self.animate()
        self.hit_reaction()
        self.move(self.speed)
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.actions(player)
        self.get_status(player)

        