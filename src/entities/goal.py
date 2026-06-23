from src.object import IObject

class Goal(IObject):
    def __init__(self, number: int, skin: int):
        super().__init__(f'goal{number}', f'goal{number}-{skin}')
    
    def move(self):
        pass