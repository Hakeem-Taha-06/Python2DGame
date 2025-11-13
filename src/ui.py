import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #bar image setup
        self.health_bar_bg = pygame.image.load('./graphics/ui/health_bar_bg.png').convert_alpha()
        self.health_bar = pygame.image.load('./graphics/ui/health_bar.png').convert()
        self.health_bar_bg_rect = self.health_bar_bg.get_rect(bottomleft = (10, MAP_HEIGHT-10))
        
        self.energy_bar_bg = pygame.image.load('./graphics/ui/energy_circle_bg.png').convert_alpha()
        self.energy_bar = pygame.image.load('./graphics/ui/energy_circle.png').convert_alpha()
        self.energy_bar_bg_rect = self.energy_bar_bg.get_rect(bottomleft = (160, MAP_HEIGHT-10))

        self.box = pygame.image.load('./graphics/ui/box.png').convert_alpha()
        #bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, BAR_HEIGHT + 15, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        #convert weapon dictionary
        self.weapon_icons = {}
        for type in weapon_data.keys(): #type = class name like 'knight' for example
            self.weapon_icons[type] = {} #create a dictionary inside with type as the key
            for weapon in weapon_data[type].keys(): #weapon = weapon name like 'lance' for example
                path = weapon_data[type][weapon]['graphic'] #get the image path from the originial dict
                weapon_icon = pygame.image.load(path).convert_alpha() #load image
                #create a key 'weapon' with the image as the value as the value for key 'type'
                self.weapon_icons[type][weapon] = weapon_icon 

        #convert magic dictionary
        self.magic_icons = {}   
        for type in magic_data.keys():
            self.magic_icons[type] = {}
            for style in magic_data[type].keys():
                path = magic_data[type][style]['graphic']
                magic_icon = pygame.image.load(path).convert_alpha()
                self.magic_icons[type][style] = magic_icon
                   
    def show_bar(self, current, max, bg_rect, color):
        rect_width = int(bg_rect.width*(current/max))
        bar_rect = pygame.Rect(bg_rect.x, bg_rect.y, rect_width, BAR_HEIGHT)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, color, bar_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,bg_rect, 4)

    def show_meter(self, current, max, bg_surf, bg_rect, bar_surf, x_offset, y_offset):
        #calculate the bar height based on the current
        if current < 0:
            current = 1
        if current > max:
            current = max
        if max == 0:
            bar_height = bar_surf.get_height()
        else:
            bar_height = int(bar_surf.get_height()*(current/max))
        y = bar_surf.get_height() - bar_height
        #get the bar surf based on the bar height and position it
        current_bar_surf = pygame.Surface.subsurface(bar_surf, pygame.Rect(0, y, bar_surf.get_width(), bar_height))
        offset = pygame.math.Vector2(x_offset, y_offset)
        current_bar_rect = current_bar_surf.get_rect(bottomleft = bg_rect.bottomleft + offset)
        #draw
        self.display_surface.blit(bg_surf, bg_rect)
        self.display_surface.blit(current_bar_surf, current_bar_rect)
    
    def show_exp(self, exp):
        text_surf = self.font.render(f'{int(exp)}', False, TEXT_COLOR)
        x = MAP_WIDTH - TILE_SIZE
        y = MAP_HEIGHT - TILE_SIZE
        text_rect = text_surf.get_rect(bottomright = (x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20), 4)

    def selection_box(self, left, bottom):
        box_image = pygame.transform.scale(self.box, (ITEM_BOX_SIZE, ITEM_BOX_SIZE))
        box_rect = box_image.get_rect(left = left, bottom = bottom)

        self.display_surface.blit(box_image, box_rect)
        return box_rect
    
    def weapon_overlay(self, type, weapon):
        box_rect = self.selection_box(300, MAP_HEIGHT - 10)
        weapon_surf = self.weapon_icons[type][weapon]
        weapon_rect = weapon_surf.get_rect(center = box_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)
    
    def magic_overlay(self, type, style):
        box_rect = self.selection_box(425, MAP_HEIGHT - 10)
        magic_surf = self.magic_icons[type][style]
        magic_rect = magic_surf.get_rect(center = box_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        #self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        #self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_meter(player.health, player.stats['health'], self.health_bar_bg, self.health_bar_bg_rect, self.health_bar, 24, -32)
        self.show_meter(player.energy, player.stats['energy'], self.energy_bar_bg, self.energy_bar_bg_rect, self.energy_bar, 20, -20)
        self.show_exp(player.exp)
        self.weapon_overlay(player.type, player.current_weapon)
        self.magic_overlay(player.type, player.current_magic)