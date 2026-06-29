import pygame
from pygame import Surface, Rect
from pygame.font import Font
from src.constants.window import WIN_WIDTH, WIN_HEIGHT
from src.constants.menu import OPTIONS as menuOptions
from src.constants.menu import ITEM_COLOR, SELECTED_ITEM_COLOR, TITLE_COLOR, GAP_MENU

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('assets/menuBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.userOption = 0

    def show(self) -> int:
        '''Mostra o menu e retorna a opção do usuário.'''
        self.userOption = 0
        pygame.mixer_music.load(f'./assets/songs/menu.mp3')
        pygame.mixer_music.set_volume(0.4)
        pygame.mixer_music.play(-1)
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.drawText('Copa do Mundo', (WIN_WIDTH / 2, WIN_HEIGHT / 4.5), color=TITLE_COLOR, size=60, bold=True, shadow=True)
            self.drawText('2026', (WIN_WIDTH / 2, WIN_HEIGHT / 4.5 + GAP_MENU * 1.5), color=TITLE_COLOR, size=60, bold=True, shadow=True)
            overlay = pygame.Surface((320, 140))
            overlay.set_alpha(140)
            overlay.fill((255, 255, 255))
            self.window.blit(overlay, (128, 160))
            for option, label in menuOptions.items():
                self.drawText(label, (WIN_WIDTH / 2, (WIN_HEIGHT / 2) + (1 + option) * GAP_MENU), color=SELECTED_ITEM_COLOR if option == self.userOption else ITEM_COLOR)
            self.drawLegend()
            pygame.display.flip()
            enter = self.processAction()
            if enter:
                return self.userOption
            
    def drawLegend(self):
        overlay = pygame.Surface((170, 40))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))
        self.window.blit(overlay, (10, 5))
        font: Font = pygame.font.SysFont(name="Arial", size=14, bold=True)
        legend = '↑ ↓         - NAVEGAR'
        legendSurf = font.render(legend, True, TITLE_COLOR).convert_alpha()
        legendRect = legendSurf.get_rect(topleft=(20, 10))
        self.window.blit(legendSurf, legendRect)
        legend = 'ENTER - CONFIRMAR'
        legendSurf = font.render(legend, True, TITLE_COLOR).convert_alpha()
        legendRect = legendSurf.get_rect(topleft=(20, 26))
        self.window.blit(legendSurf, legendRect)

    def drawText(self, text, center: tuple, size: int = 48, color: tuple = ITEM_COLOR, bold: bool = False, shadow: bool = False):
        '''Desenha um texto na tela.'''
        font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=size, bold=bold)
        if shadow:
            shadowSurf = font.render(text, True, (0, 0, 0)).convert_alpha()
            shadowSurf.set_alpha(200)
            shadowRect = shadowSurf.get_rect(center=(center[0] + 1.5, center[1] + 1.5))
            self.window.blit(shadowSurf, shadowRect)
        surf: Surface = font.render(text, True, color).convert_alpha()
        rect: Rect = surf.get_rect(center=center)
        self.window.blit(source=surf, dest=rect)

    def processAction(self) -> bool:
        '''Processa a ação do usuário.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.userOption >= len(menuOptions.keys()) - 1:
                        self.userOption = 0
                        continue
                    self.userOption += 1
                if event.key == pygame.K_UP:
                    if self.userOption <= 0:
                        self.userOption = len(menuOptions.keys()) - 1
                        continue
                    self.userOption -= 1
                if event.key == pygame.K_RETURN:
                    return True
        return False

