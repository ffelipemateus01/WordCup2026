import pygame
from src.object import IObject
from src.factory import ElementFactory
from enum import Enum

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
        self.objects.append(ElementFactory.getNewPlayer('p1'))
        self.objects.append(ElementFactory.getNewPlayer('bot') if mode == MatchMode.SINGLE else ElementFactory.getNewPlayer('p2'))
        self.objects.append(ElementFactory.getRandomBall())

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for obj in self.objects:
                self.window.blit(source=obj.surf, dest=obj.rect)
                obj.gravity()
                obj.move()
            userAction = self.getEvent()
            pygame.display.flip()

    def getEvent(self) -> bool:
        '''Processa a ação do usuário.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        return False