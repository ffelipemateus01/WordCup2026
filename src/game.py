import sys
import pygame
from src.menu import Menu
from src.constants.window import WIN_WIDTH, WIN_HEIGHT
from src.constants.menu import OPTIONS as menuOptions
from src.match import Match, MatchMode

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        '''Looping principal do game'''
        while True:
            menu = Menu(self.window)
            choice = menu.show()
            if choice in (0, 1):
                mode = MatchMode(choice)
                match = Match(self.window, mode)
                result = match.run()
            elif choice == 3:
                pygame.quit()
                quit()
            else:
                pygame.quit()
                sys.exit()