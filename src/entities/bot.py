from src.object import IObject
import pygame

class Bot(IObject):
    def __init__(self, name: str, skin: int):
        super().__init__(name, f'{name}-{skin}')
        self.score = 0

    def move(self):
        pass