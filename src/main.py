import pygame, sys
from settings import *
from debug import debug
from level import LevelManager
from menu import MenuManager
import state

class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        pygame.display.set_caption("PythonGame")
        self.clock = pygame.time.Clock()
        pygame.event.set_grab(True)

        self.energy_recovery_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.energy_recovery_timer, 2000)
        
        self.current_manager = None
        self.current_state = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if self.current_manager:
                    self.current_manager.handle_events(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if self.current_state != state.GAME_STATE:
                self.current_manager = self.create_manager(state.GAME_STATE)
                self.current_state = state.GAME_STATE
            if state.GAME_STATE == state.GameState.EXIT:
                sys.exit(0)
            else:
                if self.current_manager:
                    self.screen.fill(WATER_COLOR)
                    self.current_manager.update()
                
            pygame.display.update()
            self.clock.tick(FPS)
    
    def create_manager(self, game_state):
        if game_state == state.GameState.MENU or game_state == state.GameState.DEATH:
            return MenuManager()
        if game_state == state.GameState.PLAY:
            return LevelManager()

if __name__ == "__main__":
    game = Game()
    game.run()