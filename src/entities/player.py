from src.object import IObject
from src.constants.match import PLAYER_SIZE, PLAYER_SPEED, PLAYER1_POSITION, PLAYER2_POSITION, GROUND_HEIGHT, PLAYER_GRAVITY_FORCE, GOAL1_POSITION, GOAL2_POSITION, GOAL_SIZE
from src.constants.match import PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT, PLAYER_KEY_UP, PLAYER_KEY_SHOOT
import pygame

class Player(IObject):
    def __init__(self, name: str, skinPath: str):
        position = PLAYER1_POSITION if 'p1' in name else PLAYER2_POSITION
        super().__init__(name, position, PLAYER_SPEED, skinPath)

    def gravity(self):
        displacement = PLAYER_GRAVITY_FORCE
        newPositionY = self.rect.bottom + displacement
        finalPositionY = newPositionY if newPositionY < GROUND_HEIGHT else GROUND_HEIGHT
        self.rect.bottomleft = (self.rect.top, finalPositionY)

    def jump(self):
        if self.rect.bottom == GROUND_HEIGHT:
            displacement = 2 * PLAYER_GRAVITY_FORCE
            newPositionY = self.rect.bottom - displacement
            self.rect.bottomleft = (self.rect.left, newPositionY)

    def move(self):
        pressed = pygame.key.get_pressed()
        # if pressed[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
        #     self.rect.centery -= ENTITY_SPEED[self.name]
        # if pressed[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
        #     self.rect.centery += ENTITY_SPEED[self.name]
        # if pressed[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
        #     self.rect.centerx -= ENTITY_SPEED[self.name]
        # if pressed[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
        #     self.rect.centerx += ENTITY_SPEED[self.name]