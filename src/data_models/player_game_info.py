from data_models.card import Cards
from data_models.bet_option import BetOption, BetOptions


class PlayerGameInfo:
    def __init__(self, data: dict) -> None:
        self.player_id = data['player_id']
        self.first_two_cards = Cards(data['first_two_cards']) if data.get('first_two_cards') else Cards([])
        self.hit_cards = Cards(data['hit_cards']) if data.get('hit_cards') else Cards([])
        self.is_stand = data['is_stand']
        self.result = data.get('result')
        self.bet_options = BetOptions(data['bet_options']) if data.get('bet_options') else BetOptions([])

    def to_dict(self) -> dict:
        return {
            'player_id': self.player_id,
            'first_two_cards': self.first_two_cards.to_list(),
            'hit_cards': self.hit_cards.to_list(),
            'bet_options': self.bet_options.to_list(),
            'is_stand': self.is_stand,
            'result': self.result
        }


class PlayerGameInfos(list):
    def __init__(self, datalist: list):
        for data in datalist:
            self.append(PlayerGameInfo(data))
    
    def to_list(self) -> list:
        return [item.to_dict() for item in self]


class PlayerGameInfos(PlayerGameInfos):
    pass

#Banker only have one
class BankerGameInfo:
    def __init__(self, data: dict) -> None:
        self.first_two_cards = Cards(data['first_two_cards']) if data.get('first_two_cards') else Cards([])
        self.hit_cards = Cards(data['hit_cards']) if data.get('hit_cards') else Cards([])
        self.is_stand = data['is_stand']
        self.result = data.get('result')
        
    def to_dict(self) -> dict:
        return {
            'first_two_cards': self.first_two_cards.to_list(),
            'hit_cards': self.hit_cards.to_list(),
            'is_stand': self.is_stand,
            'result': self.result
        }
