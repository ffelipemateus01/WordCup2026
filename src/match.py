import pygame
from enum import Enum
from src.object import IObject
from src.factory import ElementFactory
from src.mediator import CollisionMediator
from src.entities.bot import Bot
from src.entities.player import Player
from src.constants.match import WIN_WIDTH, WIN_HEIGHT, WIN_SCORE
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
        self.objects.append(ElementFactory.getGoal(1))
        self.objects.append(ElementFactory.getGoal(2))
        self.objects.append(ElementFactory.getNewPlayer('player1'))
        self.objects.append(ElementFactory.getNewPlayer('bot') if mode == MatchMode.SINGLE else ElementFactory.getNewPlayer('player2'))
        self.objects.append(ElementFactory.getRandomBall())
        self.player1: Player = next(obj for obj in self.objects if obj.name == 'player1')
        self.player2: Player | Bot = next(obj for obj in self.objects if obj.name == 'player2' or obj.name == 'bot')
        self.collisionMediator = CollisionMediator(self.objects)
        self.font = pygame.font.SysFont('Arial', 48, bold=True)
        self.db = DBProxy()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for obj in self.objects:
                self.window.blit(source=obj.surf, dest=obj.rect)
                obj.move()
            self.collisionMediator.verify_collision()
            score = f'{self.player1.score}x{self.player2.score}'
            scoreSurf = self.font.render(score, True, (0, 0, 0)).convert_alpha()
            self.window.blit(scoreSurf, (WIN_WIDTH / 2 - scoreSurf.get_width() / 2, 10))

            winner = self.getWinner()
            if winner:
                self.showWinner(winner)
                return
            
            self.getEvent()
            pygame.display.flip()

    def getEvent(self):
        '''Processa a ação do usuário.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pause()

    def pause(self):
        font = pygame.font.SysFont('Arial', 64, bold=True)
        pauseSurf = font.render('Pausado!', True, (255, 255, 255)).convert_alpha()
        font = pygame.font.SysFont('Arial', 42, bold=True)
        placarSurf = font.render(f'{self.player1.score} x {self.player2.score}', True, (255, 255, 255)).convert_alpha()
        font = pygame.font.SysFont('Arial', 24, bold=True)
        enterSurf = font.render('Pressione ENTER para voltar a partida', True, (255, 255, 255)).convert_alpha()

        overlay = pygame.Surface(self.window.get_size())
        overlay.set_alpha(180)
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
        txt = f'{winner.name} venceu!'
        winnerSurf = font.render(txt, True, (255, 255, 255)).convert_alpha()
        font = pygame.font.SysFont('Arial', 42, bold=True)
        placarSurf = font.render(f'{self.player1.score} x {self.player2.score}', True, (255, 255, 255)).convert_alpha()
        font = pygame.font.SysFont('Arial', 24, bold=True)
        enterSurf = font.render('Pressione ENTER para voltar ao menu', True, (255, 255, 255)).convert_alpha()

        overlay = pygame.Surface(self.window.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.window.blit(overlay, (0, 0))
            self.window.blit(winnerSurf, (WIN_WIDTH / 2 - winnerSurf.get_width() / 2, WIN_HEIGHT / 4))
            self.window.blit(placarSurf, (WIN_WIDTH / 2 - placarSurf.get_width() / 2, WIN_HEIGHT / 4 + winnerSurf.get_height() + 20))
            self.window.blit(enterSurf, (WIN_WIDTH / 2 - enterSurf.get_width() / 2, WIN_HEIGHT / 4 + winnerSurf.get_height() + enterSurf.get_height() + 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return