from data_models.card import Cards
from data_models.bet_option import BetOption, BetOptions


class PlayerGameInfo:
    @classmethod
    def generate_default_ins(cls, player_id: str) -> 'PlayerGameInfo':
        return cls({
            'player_id': player_id,
            'first_two_cards': [],
            'hit_cards': [],
            'is_stand': False
        })
    
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
            'total_point': self.total_point(),
            'is_stand': self.is_stand,
            'result': self.result
        }

    def total_point(self) -> int:
        sum = 0
        ace_sum = 0
        for card in self.first_two_cards:
            sum += card.point()
            ace_sum += card.ace_point()
        
        for card in self.hit_cards:
            sum += card.point()
            ace_sum += card.ace_point()

        if sum < ace_sum:
            if ace_sum <= 21:
                return ace_sum
            else:
                return sum
        else:
            if sum <= 21:
                return sum
            else:
                return ace_sum

    def is_bust(self) -> bool:
        return self.total_point() > 21


class PlayerGameInfos(list):
    def __init__(self, datalist: list):
        for data in datalist:
            self.append(PlayerGameInfo(data))
    
    def to_list(self) -> list:
        return [item.to_dict() for item in self]


#  Banker only have one
class BankerGameInfo(PlayerGameInfo):
    BANKER_ID = 'banker'
    
    @classmethod
    def generate_default_ins(cls) -> 'BankerGameInfo':
        return cls({
            'first_two_cards': [],
            'hit_cards': [],
            'is_stand': False
        })

    def __init__(self, data: dict) -> None:
        data.update({
            'player_id': self.BANKER_ID,
            'bet_options': None
        })

        super().__init__(data)

    def to_dict(self) -> dict:
        hash = super().to_dict()
        del hash['player_id']
        del hash['bet_options']
        return hash
