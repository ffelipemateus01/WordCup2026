from src.entities.field import FieldElement
from src.entities.goal import Goal
from src.entities.player import Player
from src.entities.ball import Ball
from random import randint
from src.constants.skins import MAX_FIELDS_SKINS, MAX_BALLS_SKINS, MAX_PLAYERS_SKINS, MAX_GOALS_SKINS

class ElementFactory:
    @staticmethod
    def getRandomField() -> list[FieldElement]:
        random = randint(1, MAX_FIELDS_SKINS)
        return [FieldElement(random, 1), 
                FieldElement(random, 2),
                FieldElement(random, 3),
                FieldElement(random, 4)]

    @staticmethod
    def getGoal(number: int) -> Goal:
        random = randint(1, MAX_GOALS_SKINS)
        return Goal(f'goal{number}-{random}', number)

    @staticmethod
    def getNewPlayer(name: str) -> Player:
        random = randint(1, MAX_PLAYERS_SKINS)
        return Player(name, f'{name}-{random}')
    
    @staticmethod
    def getRandomBall() -> Ball:
        random = randint(1, MAX_BALLS_SKINS)
        return Ball(random)