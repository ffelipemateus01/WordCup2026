from abc import ABC, abstractmethod
import pygame

class IObject(ABC):
    def __init__(self, name: str, position: tuple, speed: float = 0, skinPath: str | None = None):
        path = skinPath if skinPath is not None else name
        self.surf = pygame.image.load(f'assets/{path}.png').convert_alpha()
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.name = name
        self.speed = speed

    @abstractmethod
    def gravity(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def jump(self):
        pass