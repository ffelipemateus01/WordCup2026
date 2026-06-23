from abc import ABC, abstractmethod
import pygame
from src.constants.match import GROUND_HEIGHT, ENTITIES_GRAVITY_FORCE, ENTITIES_SPEED, ENTITIES_START_POSITION

class IObject(ABC):
    def __init__(self, name: str, skinPath: str | None = None):
        path = skinPath if skinPath is not None else name
        self.surf = pygame.image.load(f'assets/{path}.png').convert_alpha()
        self.name = name
        self.rect = self.surf.get_rect(left=ENTITIES_START_POSITION[self.name][0], top=ENTITIES_START_POSITION[self.name][1])
        self.speed = ENTITIES_SPEED[name]
        self.gravityForce = ENTITIES_GRAVITY_FORCE[name]
        self.velocityY = 0
        self._originalSurf = self.surf
        self._facingLeft = False

    @abstractmethod
    def move(self):
        self.__gravityAction()

    def _transformSurf(self, goingLeft: bool):
        if goingLeft != self._facingLeft:
            if not goingLeft:
                self.surf = self._originalSurf
            else:
                self.surf = pygame.transform.flip(self.surf, True, False)
            self._facingLeft = goingLeft

    def __gravityAction(self):
        self.velocityY += self.gravityForce
        self.rect.y += self.velocityY
        if self.isOnGround():
            self.rect.bottom = GROUND_HEIGHT
            self.velocityY = 0

    def isOnGround(self):
        return self.rect.bottom >= GROUND_HEIGHT