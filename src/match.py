import pygame
from enum import Enum
from src.object import IObject
from src.factory import ElementFactory
from src.mediator import CollisionMediator

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
        self.collisionMediator = CollisionMediator(self.objects)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for obj in self.objects:
                self.window.blit(source=obj.surf, dest=obj.rect)
                obj.move()
            self.collisionMediator.verify_collision()
            userAction = self.getEvent()
            pygame.display.flip()

    def getEvent(self) -> bool:
        '''Processa a ação do usuário.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        return False