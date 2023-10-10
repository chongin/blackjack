class MetaData:
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__init_manual__()
        return cls._instance

    def __init_manual__(self) -> None:
        self.currency = 'CAD'
        self.number_of_decks = 8
        self.bet_option_names = ['base_win', 'pair']
        self.odds = {'base_game': 1, 'blackjack': 2, 'pair': 3}

            