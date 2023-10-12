class SystemConfig:
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
        # game config
        self.number_of_decks = 8
        self.number_of_top_winners = 5
        self.bet_option_names = ['base_win', 'pair', 'insurence']
        self.odds = {'base_game': 1, 'blackjack': 2, 'pair': 3}

        # system internal config
        self.support_game_mode = ['single_player', 'multi_player']
        self.check_job_timeout_interval_in_seconds = 1
        self.currency = 'CAD'
   
    def job_timeout_in_seconds_config(self) -> None:
        self.job_timeouts = {
            'NotifyBetEndedJob': 1,
            'NotifyClosedJob': 3,
            'NotifyNextRoundStartedJob': 1,
            'NotifyDealStartedJob': 1,
        }

    def get_job_timeout_in_seconds(self, job_name: str) -> int:
        return self.job_timeouts['job_name']
