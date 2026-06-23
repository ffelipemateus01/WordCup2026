from src.object import IObject
from src.constants.match import WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT, JUMP_FORCE
import pygame

class Player(IObject):
    def __init__(self, name: str, skin: int):
        super().__init__(name, f'{name}-{skin}')
        self.score = 0

    def __jump(self):
        if self.isOnGround():
            self.velocityY = -JUMP_FORCE

    def move(self):
        super().move()
        pressed = pygame.key.get_pressed()
        if pressed[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.__jump()
        if pressed[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= self.speed
            self._transformSurf(True)
        if pressed[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += self.speed
            self._transformSurf(False)