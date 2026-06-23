from src.object import IObject

class FieldElement(IObject):
    def __init__(self, skin: int, imageNumber: int):
        super().__init__('field', f'field{skin}/{imageNumber}')

    def move(self):
        pass