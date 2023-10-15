from data_models.round import Round, RoundHistories
from data_models.db_conn.firebase_client import FirebaseClient
from logger import Logger


class RoundHistoriesRepository:
    def __init__(self) -> None:
        pass

    def retrieve_round_histories(self, round: Round) -> RoundHistories:
        path = self._construct_path(round)
        round_histories = FirebaseClient.instance().get_value(path)
        if round_histories is None:
            round_histories = []

        return RoundHistories(round_histories)
    
    def save_round(self, round: Round) -> bool:
        path = self._construct_path(round)
        round_histories = self.retrieve_round_histories(round)
        round_histories.append(round)
        count = len(round_histories)
        FirebaseClient.instance().set_value(path, round_histories.to_list())
        Logger.debug(f"save round success, round_id:{round.round_id}. now have rounds: {count}")
        return True
    
    def _construct_path(self, round: Round) -> str:
        shoe_name = round.deck.shoe.shoe_name
        deck_name = f"{round.deck.deck_api_id}_{round.deck_index}"
        return f"round_histories/{shoe_name}/{deck_name}"