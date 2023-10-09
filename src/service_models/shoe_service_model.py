
class ShoeServiceModel:
    @classmethod
    def retrieve_shoe(self, name):
        return ''.join(word.capitalize() for word in name.split('_'))
    
    def __init__(self) -> None:
        pass