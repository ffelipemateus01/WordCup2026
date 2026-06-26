import pygame
from pygame import Surface, Rect
from pygame.font import Font
from src.database import DBProxy
from src.constants.window import WIN_WIDTH, WIN_HEIGHT
from src.constants.match import NAME_LABELS
from src.constants.menu import TITLE_COLOR, SELECTED_ITEM_COLOR, ITEM_COLOR


class Ranking:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('assets/menuBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def show(self):
        db = DBProxy()
        ranking = db.retrieve_ranking()
        db.close()

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.drawText('VITÓRIAS', (WIN_WIDTH / 2, 35), color=TITLE_COLOR, size=40, bold=True, shadow=True)
            
            if not ranking:
                self.drawText('Nenhuma partida registrada', (WIN_WIDTH / 2, WIN_HEIGHT / 2), size=20)
            else:
                for i, (name, wins) in enumerate(ranking):
                    label = NAME_LABELS.get(name)
                    txt = f'{i + 1}. {label} - {wins}'
                    color = SELECTED_ITEM_COLOR if i == 0 else ITEM_COLOR
                    self.drawText(txt, (WIN_WIDTH / 2, 90 + i * 24), color=color, size=22)
            
            self.drawText('ENTER / ESC para voltar', (WIN_WIDTH / 2, WIN_HEIGHT - 25), size=16)
            pygame.display.flip()

    def drawText(self, text, center: tuple, size: int = 22, color: tuple = ITEM_COLOR, bold: bool = False, shadow: bool = False):
        font: Font = pygame.font.SysFont(name="Arial", size=size, bold=bold)
        if shadow:
            shadowSurf = font.render(text, True, (0, 0, 0)).convert_alpha()
            shadowSurf.set_alpha(200)
            shadowRect = shadowSurf.get_rect(center = (center[0] + 3, center[1] + 3))
            self.window.blit(shadowSurf, shadowRect)
        surf: Surface = font.render(text, True, color).convert_alpha()
        rect: Rect = surf.get_rect(center=center)
        self.window.blit(source=surf, dest=rect)

    def processAction(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                return True
        return False