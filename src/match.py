import pygame
from pygame.font import Font
from pygame import Surface
from enum import Enum
from src.object import IObject
from src.factory import ElementFactory
from src.mediator import CollisionMediator
from src.entities.bot import Bot
from src.entities.player import Player
from src.constants.match import WIN_WIDTH, WIN_HEIGHT, WIN_SCORE, NAME_LABELS
from src.constants.menu import TITLE_COLOR
from src.database import DBProxy

class MatchMode(Enum):
    SINGLE = 0
    VERSUS = 1

class Match:
    def __init__(self, window, mode: MatchMode):
        self.window = window
        self.mode = mode
        self.objects: list[IObject] = []
        self.objects.extend(ElementFactory.getRandomField())
        self.objects.append(ElementFactory.getNewPlayer('player1'))
        self.objects.append(ElementFactory.getNewPlayer('bot') if mode == MatchMode.SINGLE else ElementFactory.getNewPlayer('player2'))
        self.objects.append(ElementFactory.getRandomBall())
        self.objects.append(ElementFactory.getGoal(1))
        self.objects.append(ElementFactory.getGoal(2))
        self.player1: Player = next(obj for obj in self.objects if obj.name == 'player1')
        self.player2: Player | Bot = next(obj for obj in self.objects if obj.name == 'player2' or obj.name == 'bot')
        self.collisionMediator = CollisionMediator(self.objects)
        self.font = pygame.font.SysFont('Arial', 48, bold=True)
        self.db = DBProxy()

    def run(self):
        clock = pygame.time.Clock()
        pygame.mixer_music.load(f'./assets/songs/stadium.mp3')
        pygame.mixer_music.set_volume(0.4)
        pygame.mixer_music.play(-1)
        while True:
            clock.tick(60)
            for obj in self.objects:
                self.window.blit(source=obj.surf, dest=obj.rect)
                obj.move()
            scorer = self.collisionMediator.verify_collision()
            self.drawLegend()
            score = f'{self.player1.score}x{self.player2.score}'
            scoreSurf = self.font.render(score, True, TITLE_COLOR).convert_alpha()
            scoreShadowSurf = self.font.render(score, True, (0, 0, 0)).convert_alpha()
            self.window.blit(scoreShadowSurf, (WIN_WIDTH / 2 - scoreSurf.get_width() / 2 + 3, 10 + 3))
            self.window.blit(scoreSurf, (WIN_WIDTH / 2 - scoreSurf.get_width() / 2, 10))
            winner = self.getWinner()
            if winner:
                self.showWinner(winner)
                return
            if scorer:
                self.showGoalOverlay(scorer)
            self.getEvent()
            pygame.display.flip()

    def showGoalOverlay(self, name: str):
        font = pygame.font.SysFont('Arial', 72, bold=True)
        txt = 'GOOOLLL!!!'
        goalSurf = font.render(txt, True, TITLE_COLOR).convert_alpha()
        goalShadowSurf = font.render(txt, True, (0, 0, 0)).convert_alpha()
        goalShadowSurf.set_alpha(120)
        font = pygame.font.SysFont('Arial', 60, bold=True)
        txt = f'{self.player1.score} x {self.player2.score}'
        placarSurf = font.render(txt, True, (0, 0, 0)).convert_alpha()
        font = pygame.font.SysFont('Arial', 48, bold=True)
        txt = f'{NAME_LABELS.get(name, name)} marcou'
        playerSurf = font.render(txt, True, (0, 0, 0)).convert_alpha()
        overlay = pygame.Surface(self.window.get_size())
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))
        clock = pygame.time.Clock()
        TICK = 60
        TIME_SHOW = 1.65
        quitGoalScreen = TIME_SHOW * TICK
        cont = 0
        pygame.mixer_music.load(f'./assets/songs/goal.mp3')
        pygame.mixer_music.set_volume(0.8)
        pygame.mixer_music.play()
        while True:
            cont += 1
            clock.tick(TICK)
            self.window.blit(overlay, (0, 0))
            self.window.blit(goalSurf, (WIN_WIDTH / 2 - goalSurf.get_width() / 2, 40))
            self.window.blit(placarSurf, (WIN_WIDTH / 2 - placarSurf.get_width() / 2, 135))
            self.window.blit(playerSurf, (WIN_WIDTH / 2 - playerSurf.get_width() / 2, 225))
            pygame.display.flip()

            if cont >= quitGoalScreen:
                pygame.mixer_music.load(f'./assets/songs/stadium.mp3')
                pygame.mixer_music.set_volume(0.4)
                pygame.mixer_music.play(-1)
                return
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def getEvent(self):
        '''Processa a ação do usuário.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pause()

    def drawLegend(self):
        overlay = pygame.Surface((170, 60))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))
        self.window.blit(overlay, (10, 5))
        font: Font = pygame.font.SysFont(name="Arial", size=14, bold=True)
        legend = 'W    - PULA'
        legendSurf = font.render(legend, True, TITLE_COLOR).convert_alpha()
        legendRect = legendSurf.get_rect(topleft=(20, 10))
        self.window.blit(legendSurf, legendRect)
        legend = 'A D  - MOVIMENTO'
        legendSurf = font.render(legend, True, TITLE_COLOR).convert_alpha()
        legendRect = legendSurf.get_rect(topleft=(20, 26))
        self.window.blit(legendSurf, legendRect)
        legend = 'ESC - PAUSE'
        legendSurf = font.render(legend, True, TITLE_COLOR).convert_alpha()
        legendRect = legendSurf.get_rect(topleft=(20, 42))
        self.window.blit(legendSurf, legendRect)

        if isinstance(self.player2, Player):
            overlay = pygame.Surface((170, 40))
            overlay.set_alpha(180)
            overlay.fill((255, 255, 255))
            self.window.blit(overlay, (400, 5))
            font: Font = pygame.font.SysFont(name="Arial", size=14, bold=True)
            legend = '↑       - PULA'
            legendSurf = font.render(legend, True, TITLE_COLOR).convert_alpha()
            legendRect = legendSurf.get_rect(topleft=(400 + 10, 10))
            self.window.blit(legendSurf, legendRect)
            legend = '← → - MOVIMENTO'
            legendSurf = font.render(legend, True, TITLE_COLOR).convert_alpha()
            legendRect = legendSurf.get_rect(topleft=(400 + 10, 26))
            self.window.blit(legendSurf, legendRect)

    def pause(self):
        font = pygame.font.SysFont('Arial', 64, bold=True)
        pauseSurf = font.render('Pausado!', True, (255, 255, 255)).convert_alpha()
        font = pygame.font.SysFont('Arial', 42, bold=True)
        placarSurf = font.render(f'{self.player1.score} x {self.player2.score}', True, (255, 255, 255)).convert_alpha()
        font = pygame.font.SysFont('Arial', 24, bold=True)
        enterSurf = font.render('Pressione ENTER para voltar a partida', True, (255, 255, 255)).convert_alpha()

        overlay = pygame.Surface(self.window.get_size())
        overlay.set_alpha(90)
        overlay.fill((0, 0, 0))

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.window.blit(overlay, (0, 0))
            self.window.blit(pauseSurf, (WIN_WIDTH / 2 - pauseSurf.get_width() / 2, WIN_HEIGHT / 4))
            self.window.blit(placarSurf, (WIN_WIDTH / 2 - placarSurf.get_width() / 2, WIN_HEIGHT / 4 + pauseSurf.get_height() + 20))
            self.window.blit(enterSurf, (WIN_WIDTH / 2 - enterSurf.get_width() / 2, WIN_HEIGHT / 4 + pauseSurf.get_height() + enterSurf.get_height() + 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return
                
    def getWinner(self) -> Player | Bot | None:
        if self.player1.score >= WIN_SCORE:
            return self.player1
        if self.player2.score >= WIN_SCORE:
            return self.player2
        return None
    
    def showWinner(self, winner: Player | Bot):
        self.db.save_win(winner.name)
        self.db.close()
        font = pygame.font.SysFont('Arial', 64, bold=True)
        txt = f'{NAME_LABELS.get(winner.name, winner.name)} venceu!'
        winnerSurf = font.render(txt, True, TITLE_COLOR).convert_alpha()
        winnerShadowSurf = font.render(txt, True, (0, 0, 0)).convert_alpha()
        winnerShadowSurf.set_alpha(200)
        font = pygame.font.SysFont('Arial', 24, bold=True)
        txt = 'Pressione ENTER para voltar ao menu'
        enterSurf = font.render(txt, True, TITLE_COLOR).convert_alpha()
        enterShadowSurf = font.render(txt, True, (0, 0, 0)).convert_alpha()
        enterShadowSurf.set_alpha(200)

        clock = pygame.time.Clock()
        pygame.mixer_music.load(f'./assets/songs/victory.mp3')
        pygame.mixer_music.set_volume(0.8)
        pygame.mixer_music.play()
        while True:
            clock.tick(60)
            self.window.blit(winnerShadowSurf, (WIN_WIDTH / 2 - winnerSurf.get_width() / 2 + 3, WIN_HEIGHT / 4 + 3))
            self.window.blit(winnerSurf, (WIN_WIDTH / 2 - winnerSurf.get_width() / 2, WIN_HEIGHT / 4))
            self.window.blit(enterShadowSurf, (WIN_WIDTH / 2 - enterSurf.get_width() / 2 + 3, WIN_HEIGHT / 4 + winnerSurf.get_height() + enterSurf.get_height() + 50 + 3))
            self.window.blit(enterSurf, (WIN_WIDTH / 2 - enterSurf.get_width() / 2, WIN_HEIGHT / 4 + winnerSurf.get_height() + enterSurf.get_height() + 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                    return