from src.object import IObject

class FieldElement(IObject):
    def __init__(self, skin: int, imageNumber: int):
        super().__init__(f'field{skin}/{imageNumber}', (0,0))

    def gravity(self):
        pass

    def move(self):
        pass

    def jump(self):
        pass