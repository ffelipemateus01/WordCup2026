from src.object import IObject
from src.constants.match import GOAL1_POSITION, GOAL2_POSITION

class Goal(IObject):
    def __init__(self, name: str, number: int):
        super().__init__(name, GOAL1_POSITION if number == 1 else GOAL2_POSITION)
    
    def gravity(self):
        pass
    
    def move(self):
        pass

    def jump(self):
        pass