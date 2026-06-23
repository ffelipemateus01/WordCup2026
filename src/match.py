import pygame
from enum import Enum
from src.object import IObject
from src.factory import ElementFactory
from src.mediator import CollisionMediator
from src.entities.bot import Bot
from src.entities.player import Player
from src.constants.match import WIN_WIDTH

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
            
            userAction = self.getEvent()
            pygame.display.flip()

    def getEvent(self) -> bool:
        '''Processa a ação do usuário.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        return False