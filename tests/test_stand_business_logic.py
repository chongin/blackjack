import sys
import os
import time
# Add the parent directory (src) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import json
import unittest
from unittest.mock import Mock
from logger import Logger
from singleton_manger import SingletonManager
from mock_share_obj import MockShareObj
from utils.util import Util
from job_system.jobs.notify_job import *
from business_logic.stand_business_logic import StandBusinessLogic


def test_player_can_stand_card():
    mock_obj = MockShareObj('player_can_hit_card_data')
    mock_obj.save_to_firebase() # save to database first
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round
    player = mock_obj.player

    stand_ins = StandBusinessLogic()
    stand_ins.handle_stand(shoe.shoe_name, player.player_name, round.round_id)
    
    shoe_db = mock_obj.retrieve_shoe_from_firebase()
    current_round = shoe_db.current_deck.current_round
    player_game_info = current_round.find_player_game_info_by_player_id(player.player_id)
    assert player_game_info.is_stand == True, "Player should be hit more card"
    assert len(player_game_info.hit_cards) == 0, "Player should have one hit card"
    assert len(current_round.hit_card_sequences) == 1, "Player hit card should have 1"
