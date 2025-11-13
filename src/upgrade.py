import pygame
from settings import *
class Upgrade:
    def __init__(self, player):

        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_num = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #box dimensions
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6

        self.menu_index = 0
        self.selection_time = 0
        self.selection_cooldown = 0.1*1000
        self.can_move = True
        self.upgrade_time = 0
        self.upgrade_cooldown = 0.2*1000
        self.can_upgrade = True

        self.create_boxes()

    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        if self.can_move:
            if keys[pygame.K_a] and self.menu_index >= 1:
                self.menu_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_d] and self.menu_index < self.attribute_num - 1:
                self.menu_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
        
        for box in self.boxes:
            if box.rect.collidepoint(mouse_pos):
                self.menu_index = box.index

        if (keys[pygame.K_SLASH] or mouse[0]) and self.can_upgrade:
            self.boxes[self.menu_index].trigger(self.player)
            self.upgrade_time = pygame.time.get_ticks()
            self.can_upgrade = False

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        delta_select = current_time - self.selection_time
        delta_upgrade = current_time - self.upgrade_time
        if not self.can_move:
            if delta_select >= self.selection_cooldown:
                self.can_move = True
        if not self.can_upgrade:
            if delta_upgrade >= self.upgrade_cooldown:
                self.can_upgrade = True

    def create_boxes(self):
        self.boxes = []

        for i in range(self.attribute_num):
            left = self.width*i + (i+1)*self.width//6
            top = self.display_surface.get_size()[1]*0.1

            box = UpgradeBox(i, left, top, self.width, self.height, self.font)
            self.boxes.append(box)
    
    def display_exp(self):
        exp_surf = self.font.render(str(int(self.player.exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0]//2
        y = self.display_surface.get_size()[1] - 10
        exp_rect = exp_surf.get_rect(midbottom = (x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, exp_rect.inflate(20,20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, exp_rect.inflate(20,20), 3)
        self.display_surface.blit(exp_surf, exp_rect)
        
    def display(self):
        self.input()
        self.cooldowns()
        for index ,box in enumerate(self.boxes):
            name = self.attribute_names[index].capitalize()
            value = self.player.get_stat_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            box.display(self.display_surface, self.menu_index, name, value, max_value, cost)
        self.display_exp()

class UpgradeBox:
    def __init__(self, index, left, top, width, height, font):
        self.index = index
        self.rect = pygame.Rect(left, top, width, height)
        self.font = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_ACTIVE if selected else TEXT_COLOR
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))
        cost_surf = self.font.render(f'COST: {str(int(cost))}', False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0, -20))

        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)
    
    def display_bar(self,surface, value, max_value, selected):
        top = self.rect.midtop + pygame.math.Vector2(0, 80)
        bottom = self.rect.midbottom + pygame.math.Vector2(0, -80)

        full_height = bottom[1] - top[1]
        if max_value == 0:
            height = full_height
        else:
            height = (value/max_value)*full_height

        value_surf = self.font.render(str(int(value)), False, TEXT_COLOR)
        x = top[0]
        y = bottom[1] - height
        value_rect = value_surf.get_rect(midtop = (x, y))
        bar_color = BAR_COLOR_ACTIVE if selected else BAR_COLOR

        pygame.draw.line(surface, bar_color, top, bottom, 5)
        pygame.draw.rect(surface, bar_color, value_rect)
        surface.blit(value_surf, value_rect)

    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] += player.growth_rate[upgrade_attribute]
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.upgrade_cost[upgrade_attribute] *= 1.2

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        selected = selection_num == self.index
        border_color = UI_BORDER_COLOR_ACTIVE if selected else UI_BORDER_COLOR
        bg_color = UI_BG_COLOR_ACTIVE if selected else UI_BG_COLOR
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 3)
        self.display_names(surface, name, cost, selected)
        self.display_bar(surface, value, max_value, selected)
        
