import pygame, state
from settings import *
from tile import Tile
from player import Player
from utility import *
from debug import debug
from random import choice
from weapon import Weapon
from enemy import Enemy
from ui import UI
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from sound import SoundPlayer
class LevelManager:
    def __init__(self):
        self.current_level = None
        self.current_level_state = None

    def create_level(self, level_state):
        level_name = 'map_' + str(level_state.value)
        return Level(level_name, state.CHARACTER)
    
    def handle_events(self, event):
        if self.current_level:
            self.current_level.handle_events(event)

    def update(self):
        if self.current_level_state != state.LEVEL_STATE:
            self.current_level = self.create_level(state.LEVEL_STATE)
            self.current_level_state = state.LEVEL_STATE

        if self.current_level:
            self.current_level.run()

class Level:
    def __init__(self, level_name, player_character):
        #display surface
        self.display_surface = pygame.display.get_surface()
        self.level_name = level_name
        self.player_character = player_character
        self.game_paused = False

        #sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #sprites
        self.create_map()
        
        #ui
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        #SFX
        self.sound_player = SoundPlayer()

        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layouts = {
            'floorblocks' : import_csv_layout(f'graphics/maps/{self.level_name}/map_data/{self.level_name}_floorblocks.csv'),
            'grass' : import_csv_layout(f'graphics/maps/{self.level_name}/map_data/{self.level_name}_grass.csv'),
            'objects' : import_csv_layout(f'graphics/maps/{self.level_name}/map_data/{self.level_name}_objects.csv'),
            'entities' : import_csv_layout(f'graphics/maps/{self.level_name}/map_data/{self.level_name}_entities.csv')
        }
        graphics = {
            'grass' : import_image_from_folder('graphics/maps/'+self.level_name+'/grass'),
            'objects' : import_image_from_folder('graphics/maps/'+self.level_name+'/objects'),
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index*TILE_SIZE
                        y = row_index*TILE_SIZE
                        if style == 'floorblocks':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            grass_surf = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'grass',grass_surf)
                        if style == 'objects':
                            object_surf = graphics['objects'][int(val)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_surf)
                        if style == 'entities':
                            if val == '394':
                                self.player = Player(
                                self.player_character,
                                (x, y),
                                [self.visible_sprites],
                                self.obstacle_sprites,
                                self.create_attack,
                                self.destroy_attack,
                                self.create_magic)
                            else:
                                if val == '390': monster_name = 'slime'; type = 'small'
                                elif val == '391': monster_name = 'bamboo'; type = 'small'
                                elif val == '392': monster_name = 'raccoon'; type = 'big'
                                else : monster_name = 'bamboo'; type = 'small'
                                Enemy(
                                    monster_name,
                                    type,
                                    (x,y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)
            
    def create_attack(self, type):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites], type)
    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'fire':
            self.magic_player.fire(self.player, strength, cost, [self.visible_sprites, self.attack_sprites])
        if style == 'boost':
            self.magic_player.boost(self.player, strength, cost, [self.visible_sprites])
        if style == 'holy':
            self.magic_player.holy(self.player, strength, cost, [self.visible_sprites, self.attack_sprites])
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collided_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collided_sprites:
                    for target_sprite in collided_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            self.animation_player.create_grass_particles('effect', pos, [self.visible_sprites])
                            self.sound_player.play_SFX('grass')
                            target_sprite.kill()
                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.take_damage(self.player ,attack_sprite)

    def damage_player(self, amount, attack_type, attack_sound):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
            pos = self.player.rect.center
            self.animation_player.create_particles('effect', attack_type, pos, [self.visible_sprites])
            attack_sound.play()

    def trigger_death_particles(self, pos, entity_type):
        self.animation_player.create_particles('effect', entity_type, pos, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def handle_events(self, event):
        self.player.handle_events(event)
        self.visible_sprites.handle_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.toggle_menu()

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        if self.game_paused:
            self.upgrade.display()
        else:
            self.sound_player.play_music('main')
            self.visible_sprites.enemy_update(self.player)
            self.visible_sprites.update()
            debug(self.visible_sprites.zoom_scale)
            self.player_attack_logic()
            self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # center camera
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # box camera
        self.camera_borders = {'left' : 200, 'right' : 200, 'top' : 100, 'bottom' : 100}
        left = self.camera_borders['left']
        top = self.camera_borders['top']
        width = self.display_surface.get_size()[0] - self.camera_borders['right'] - left
        height = self.display_surface.get_size()[1] - self.camera_borders['bottom'] - top
        self.camera_rect = pygame.Rect(left, top, width, height)

        # camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.4

        #zoom
        self.zoom_scale = 1
        self.internal_surf_area = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_area, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_width, self.half_height))
        self.internal_surf_area_vect = pygame.math.Vector2(self.internal_surf_area)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_area[0]//2 - self.half_width
        self.internal_offset.y = self.internal_surf_area[1]//2 - self.half_height

        self.floor_surf = pygame.image.load('graphics\maps\map_0\map_data\map_0_floor.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    
    def center_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def box_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def keybaord_control_camera(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_u]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_j]: self.camera_rect.y += self.keyboard_speed
        if keys[pygame.K_h]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_k]: self.camera_rect.x += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']
    
    def mouse_control_camera(self):
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vec = pygame.math.Vector2()

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

        if top_border < mouse_pos.y < bottom_border:
            if mouse_pos.x < left_border:
                mouse_offset_vec.x = mouse_pos.x - left_border
                pygame.mouse.set_pos((left_border, mouse_pos.y))
            if mouse_pos.x > right_border:
                mouse_offset_vec.x = mouse_pos.x - right_border
                pygame.mouse.set_pos((right_border, mouse_pos.y))
        elif mouse_pos.y < top_border:
            if mouse_pos.x < left_border:
                mouse_offset_vec = mouse_pos - pygame.math.Vector2(left_border, top_border)
                pygame.mouse.set_pos((left_border, top_border))
            if mouse_pos.x > right_border:
                mouse_offset_vec = mouse_pos - pygame.math.Vector2(right_border, top_border)
                pygame.mouse.set_pos((right_border, top_border))
        elif mouse_pos.y > bottom_border:
            if mouse_pos.x < left_border:
                mouse_offset_vec = mouse_pos - pygame.math.Vector2(left_border, bottom_border)
                pygame.mouse.set_pos((left_border, bottom_border))
            if mouse_pos.x > right_border:
                mouse_offset_vec = mouse_pos - pygame.math.Vector2(right_border, bottom_border)
                pygame.mouse.set_pos((right_border, bottom_border))

        if left_border < mouse_pos.x < right_border:
            if mouse_pos.y < top_border:
                mouse_offset_vec.y = mouse_pos.y - top_border
                pygame.mouse.set_pos((mouse_pos.x , top_border))
            if mouse_pos.y > bottom_border:
                mouse_offset_vec.y = mouse_pos.y - bottom_border
                pygame.mouse.set_pos((mouse_pos.x, bottom_border))

        self.offset.x += mouse_offset_vec.x
        self.offset.y += mouse_offset_vec.y

    def keyboard_zoom_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:
            if self.zoom_scale < 1.25:
                self.zoom_scale += 0.1
        if keys[pygame.K_g]:
            if self.zoom_scale > 0.52:
                self.zoom_scale -= 0.1
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEWHEEL:
            if event.y < 0:
                if self.zoom_scale > 0.52:
                    self.zoom_scale += event.y * 0.03
            if event.y >= 1:
                if self.zoom_scale < 1.25:
                    self.zoom_scale += event.y * 0.03

    def custom_draw(self, player):

        self.center_camera(player)
        #self.box_camera(player)
        #self.keybaord_control_camera()
        #self.mouse_control_camera()
        
        self.keyboard_zoom_control()

        self.internal_surf.fill(WATER_COLOR)

        offset_pos = self.floor_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.floor_surf, offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)
        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_area_vect*self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_width, self.half_height))
        self.display_surface.blit(scaled_surf, scaled_rect)
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)