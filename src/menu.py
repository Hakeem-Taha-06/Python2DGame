import pygame
from settings import *
import state
from utility import load_horizontal_animation_sheet
class MenuManager:
    def __init__(self):
        self.current_menu = None
        self.current_menu_state = None
    
    def create_menu(self, menu_state):
        if menu_state == state.MenuState.MAIN:
            return MainMenu(state.MenuState.MAIN)
        if menu_state == state.MenuState.CHARACTER_SELECTION:
            return CharacterMenu(state.MenuState.CHARACTER_SELECTION)
        if menu_state == state.MenuState.DEATH:
            return DeathMenu(state.MenuState.DEATH)
        return None
    
    def handle_events(self, event):
        pass

    def update(self):
        if self.current_menu_state != state.MENU_STATE:
            self.current_menu = self.create_menu(state.MENU_STATE)
            self.current_menu_state = state.MENU_STATE

        if self.current_menu:
            self.current_menu.update()

class Menu:
    def __init__(self, index):
        self.display_surface = pygame.display.get_surface()
        self.index = index
        self.screen_width = self.display_surface.get_size()[0]
        self.screen_height = self.display_surface.get_size()[1]
        
        self.buttons = self.create_buttons()
        self.button_index = 0
        self.selection_index = 0

        self.can_press = False
        self.press_time = pygame.time.get_ticks()
        self.press_cooldown = 0.3*1000

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                self.button_index = button.index
                if mouse[0] and self.can_press:
                    self.can_press = False
                    self.press_time = pygame.time.get_ticks()
                    self.selection_index = self.buttons[self.button_index].press(self.selection_index, 0, len(character_data.keys()) - 1)
        
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        delta_press = current_time - self.press_time
        if not self.can_press:
            if delta_press >= self.press_cooldown:
                self.can_press = True

    def update(self):
        self.display_surface.fill('green')
        for button in self.buttons:
            button.display(self.display_surface, self.button_index)
        self.cooldown()
        self.input()

class CharacterMenu(Menu):
    def __init__(self, index):
        super().__init__(index)
        self.character_animations = []
        for character in character_data:
            frames = load_horizontal_animation_sheet(character_data[character]['graphic'], TILE_SIZE, TILE_SIZE)
            new_frames = []
            for image in frames:
                new_frames.append(pygame.transform.scale(image, (4*TILE_SIZE, 4*TILE_SIZE))) 
            self.character_animations.append({'name':character, 'frames':new_frames})
        self.current_character = self.character_animations[self.selection_index + 1]
        self.frame_index = 0
        self.font = pygame.font.Font('graphics/fonts/X12Y16PXMARUMONICA.TTF', 25)
        self.boxes = None
        
    def create_buttons(self):
        buttons = []
        half_width = self.screen_width//2
        half_height = self.screen_height//2
        buttons.append(SelectorButton(0, '<', 350, half_height - 200, 50, 100, -1))
        buttons.append(SelectorButton(1, '>', self.screen_width - 400, half_height - 200, 50, 100, 1))
        buttons.append(Button(2, 'START', half_width + 250, half_height + 200, 300, 100, target_game_state = state.GameState.PLAY))
        buttons.append(Button(3, 'BACK', half_width - 550, half_height + 200, 300, 100, target_menu_state = state.MenuState.MAIN))
        return buttons
    
    def update_character_data(self):
        self.current_character = self.character_animations[self.selection_index]
        state.CHARACTER = self.current_character['name']
        

    def animate_character(self):
        frames = self.current_character['frames']
        self.frame_index += 0.025
        if self.frame_index >= len(frames):
            self.frame_index = 0
        image = frames[int(self.frame_index)]
        rect = image.get_rect(center = (self.screen_width//2, self.screen_height//2 - 3*TILE_SIZE))

        self.display_surface.blit(image, rect)
        print(self.current_character['name'])
        print(list(character_data.keys())[self.selection_index])
    
    @staticmethod
    def get_highest_stats(stats):
        stat_list = {}
        for character in stats:
            for stat_name, value in stats[character].items():
                if stat_name not in stat_list:
                    stat_list[stat_name] = []
                stat_list[stat_name].append(value)
        highest_stats = []
        for list in stat_list.values():
            highest_stats.append(max(list))
        return highest_stats
                
    def create_stat_boxes(self):
        boxes = []
        title_font = pygame.font.Font('graphics/fonts/X12Y16PXMARUMONICA.TTF', 40)
        boxes.append(Box(self.screen_width//2 - 100, self.screen_height//2 - 50, 200, 100, title_font, self.current_character['name'].upper()))
        current_character_stats = character_data[self.current_character['name']].copy()
        current_character_stats.pop('graphic')
        character_max_stats = self.get_highest_stats(max_stats)
        for i in range(len(current_character_stats)):
            name = list(current_character_stats.keys())[i].upper()
            value = list(current_character_stats.values())[i]
            max_value = character_max_stats[i]
            boxes.append(StatBox(self.screen_width//2 - 200, self.screen_height//2 + 50 + 50*i, 400, 50, self.font, name, value, max_value))
        return boxes

    def update(self):
        self.display_surface.fill('green')
        for button in self.buttons:
            button.display(self.display_surface, self.button_index)
        if self.boxes:
            for box in self.boxes:
                box.display(self.display_surface)
        if self.current_character['name'] != list(character_data.keys())[self.selection_index]:
            self.update_character_data()
            self.boxes = self.create_stat_boxes()
            print('creating new boxes...')
        self.animate_character()
        self.cooldown()
        self.input()
        
class MainMenu(Menu):
    def __init__(self, index):
        super().__init__(index)

    def create_buttons(self):
        buttons = []
        half_width = self.screen_width//2
        half_height = self.screen_height//2
        buttons.append(Button(0, 'PLAY', half_width - 150, half_height + 50, 300, 100, target_menu_state = state.MenuState.CHARACTER_SELECTION))
        buttons.append(Button(1, 'EXIT', half_width - 150, half_height + 200, 300, 100, target_game_state = state.GameState.EXIT))
        return buttons

class DeathMenu(Menu):
    def __init__(self, index):
        super().__init__(index)

    def create_buttons(self):
        buttons = []
        half_width = self.screen_width//2
        half_height = self.screen_height//2
        buttons.append(Button(0, 'RETRY', half_width - 150, half_height + 50, 300, 100, target_game_state = state.GameState.PLAY))
        buttons.append(Button(1, 'RETURN TO MENU', half_width - 150, half_height + 200, 300, 100, target_menu_state = state.MenuState.MAIN))
        return buttons
           
class Button:
    def __init__(self, index, text, left, top, width, height, target_game_state = None, target_menu_state = None, image = None):
        if image:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect(topleft = (left, top))
        else:
            self.image = None
            self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.text = str(text)
        self.font = pygame.font.Font('graphics/fonts/X12Y16PXMARUMONICA.TTF', 36)
        self.target_game_state = target_game_state
        self.target_menu_state = target_menu_state

    def press(self, selection_index, min_index, max_index): #unused arguments to match with SelectorButton
        if self.target_game_state:
            state.GAME_STATE = self.target_game_state
        if self.target_menu_state:
            state.MENU_STATE = self.target_menu_state

    def display(self, surface, menu_index):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            color = UI_BG_COLOR_ACTIVE if menu_index == self.index else UI_BG_COLOR
            pygame.draw.rect(surface, color, self.rect)

            text_surf = self.font.render(self.text, False, TEXT_COLOR)
            text_rect = text_surf.get_rect(center = self.rect.center)
            surface.blit(text_surf, text_rect)

class SelectorButton(Button):
    def __init__(self, index, text, left, top, width, height, increment, image = None):
        super().__init__(index, text, left, top, width, height, image)
        self.increment = increment

    def press(self, selection_index, min_index, max_index):
        if self.increment > 0:
            if selection_index < max_index:
                return selection_index + self.increment
            else :
                return 0
        else:
            if selection_index > min_index:
                return selection_index + self.increment
            else :
                return max_index

class Box:
    def __init__(self, left, top, width, height, font, text):
        self.rect = pygame.Rect(left, top, width, height)
        self.font = font
        self.text = text

    def display_names(self, surface):
        title_surf = self.font.render(self.text, False, TEXT_COLOR)
        title_rect = title_surf.get_rect(center = self.rect.center)
        
        surface.blit(title_surf, title_rect)    

    def display(self, surface):
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        self.display_names(surface)
        
class StatBox(Box):
    def __init__(self, left, top, width, height, font, text, value, max_value):
        super().__init__(left, top, width, height, font, text)
        self.value = value
        self.max_value = max_value

    def display_names(self, surface):
        title_surf = self.font.render(self.text, False, TEXT_COLOR)
        title_rect = title_surf.get_rect(midleft = self.rect.midleft + pygame.math.Vector2(20, 0))
        
        surface.blit(title_surf, title_rect)

    def display_bar(self, surface):
        left = self.rect.midleft + pygame.math.Vector2(125, 0)
        right = self.rect.midright + pygame.math.Vector2(-25, 0)

        full_width = right[0] - left[0]
        if self.max_value == 0:
            width = full_width
        else:
            width = (self.value/self.max_value)*full_width

        value_surf = self.font.render(str(int(self.value)), False, TEXT_COLOR)
        x = left[0] + width
        y = right[1]
        value_rect = value_surf.get_rect(center = (x, y))

        pygame.draw.line(surface, BAR_COLOR, left, right, 5)
        pygame.draw.rect(surface, BAR_COLOR, value_rect)
        surface.blit(value_surf, value_rect)

    def display(self, surface):
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        self.display_names(surface)
        self.display_bar(surface)