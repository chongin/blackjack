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


def atest_add_jobs():
    mock_obj = MockShareObj('bet_started_data')
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    job_mgr = SingletonManager.instance().job_mgr
    # job_mgr.start_timer()
    bet_started_data = round.notify_info()
    bet_started_data.update({
        'bet_started_at': Util.current_utc_time()
    })
    job_mgr.add_notify_bet_started_job(bet_started_data)
    job = job_mgr.jobs[0]
    assert type(job) is NotifyBetStartedJob, "CreateJobe type error"

    job_mgr.add_notify_bet_ended_job(round.notify_info())
    job = job_mgr.jobs[1]
    assert type(job) is NotifyBetEndedJob, "CreateJobe type error"

    job_mgr.add_notify_deal_started_job(round.notify_info())
    job = job_mgr.jobs[2]
    assert type(job) is NotifyDealStartedJob, "CreateJobe type error"

    job_mgr.add_notify_deal_ended_job(round.notify_info())
    job = job_mgr.jobs[3]
    assert type(job) is NotifyDealEndedJob, "CreateJobe type error"


def atest_retrive_timeout_jobs():
    mock_obj = MockShareObj('bet_started_data')
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()
    job_mgr.add_notify_deal_started_job(round.notify_info())

    time.sleep(0.5)
    jobs = job_mgr.retrieve_timeout_jobs()
    assert len(jobs) == 1, "Job Should timeout"
    for job in jobs:
        print(f"Timeout job: {job.to_dict()} ")
    
    assert len(job_mgr.jobs) == 0, "Jobs in job manager should be zero"

    job_mgr.clear_jobs()
    time.sleep(0.5)
    job_mgr.add_notify_bet_ended_job(round.notify_info())
    jobs = job_mgr.retrieve_timeout_jobs()
    assert len(jobs) == 0, "Job Should not timeout"

def atest_handle_bet_started_timeout_job():
    mock_obj = MockShareObj('bet_started_data')
    mock_obj.save_to_firebase() # save to database first
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyBetStartedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 1, "Jobs should have one job inside it"
    assert job_mgr.jobs[0].job_name == 'NotifyBetEndedJob', "Job name is wrong"
    print(job_mgr.jobs[0].to_dict())

def atest_handle_bet_ended_timeout_job():
    mock_obj = MockShareObj('bet_ended_data')
    mock_obj.save_to_firebase()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyBetEndedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 1, "Jobs should have one job inside it"
    assert job_mgr.jobs[0].job_name == 'NotifyDealStartedJob', "Job name is wrong"
    print(job_mgr.jobs[0].to_dict())

def atest_handle_deal_started_timeout_job_for_player_first_card():
    mock_obj = MockShareObj('deal_started_player_first_card_data')
    mock_obj.save_to_firebase()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyDealStartedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 1, "Jobs should have one job inside it"
    assert job_mgr.jobs[0].job_name == 'NotifyDealStartedJob', "Job name is wrong"

    shoe_db = mock_obj.retrieve_shoe_from_firebase()
    current_round = shoe_db.current_deck.current_round

    assert current_round.state == 'deal_started', "Round state is wrong"
    assert len(current_round.player_game_infos[0].first_two_cards) == 1, "Should draw one card to player"
    assert len(current_round.deal_card_sequences) == 3, "Should pop up player id"

def atest_handle_deal_started_timeout_job_for_banker_first_card():
    mock_obj = MockShareObj('deal_started_banker_first_card_data')
    mock_obj.save_to_firebase()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyDealStartedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 1, "Jobs should have one job inside it"
    assert job_mgr.jobs[0].job_name == 'NotifyDealStartedJob', "Job name is wrong"

    shoe_db = mock_obj.retrieve_shoe_from_firebase()
    current_round = shoe_db.current_deck.current_round

    assert current_round.state == 'deal_started', "Round state is wrong"
    assert len(current_round.banker_game_info.first_two_cards) == 1, "Should draw one card to banker"
    assert len(current_round.deal_card_sequences) == 2, "Should pop up banker id"

def atest_handle_deal_started_timeout_job_for_player_second_card():
    mock_obj = MockShareObj('deal_started_player_second_card_data')
    mock_obj.save_to_firebase()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyDealStartedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 1, "Jobs should have one job inside it"
    assert job_mgr.jobs[0].job_name == 'NotifyDealStartedJob', "Job name is wrong"

    shoe_db = mock_obj.retrieve_shoe_from_firebase()
    current_round = shoe_db.current_deck.current_round

    assert current_round.state == 'deal_started', "Round state is wrong"
    assert len(current_round.player_game_infos[0].first_two_cards) == 2, "Should draw one card to player"
    assert len(current_round.deal_card_sequences) == 1, "Should pop up player id"

def atest_handle_deal_started_timeout_job_for_banker_second_card():
    mock_obj = MockShareObj('deal_started_banker_second_card_data')
    mock_obj.save_to_firebase()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyDealStartedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 1, "Jobs should have one job inside it"
    assert job_mgr.jobs[0].job_name == 'NotifyDealEndedJob', "Job name is wrong"

    shoe_db = mock_obj.retrieve_shoe_from_firebase()
    current_round = shoe_db.current_deck.current_round

    assert current_round.state == 'deal_ended', "Round state is wrong"
    assert len(current_round.banker_game_info.first_two_cards) == 2, "Should draw one card to banker"
    assert len(current_round.deal_card_sequences) == 0, "Should pop up banker id"

def atest_handle_deal_ended_player_hit_card():
    mock_obj = MockShareObj('deal_ended_player_hit_card_data')
    mock_obj.save_to_firebase()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyDealEndedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 0, "Jobs not have one job inside it, system is waitting player operation"
    
    shoe_db = mock_obj.retrieve_shoe_from_firebase()
    current_round = shoe_db.current_deck.current_round

    assert current_round.state == 'deal_ended', "Round state is wrong"
    assert len(current_round.hit_card_sequences) == 2, "Should have 2 inside the hit card sequences"

def atest_handle_deal_ended_banker_hit_card():
    mock_obj = MockShareObj('deal_ended_banker_hit_card_data')
    mock_obj.save_to_firebase()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyDealEndedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 1, "Jobs not have one job inside it, resulted job"
    assert job_mgr.jobs[0].job_name == 'NotifyResultedJob', "Job name is wrong"

    shoe_db = mock_obj.retrieve_shoe_from_firebase()
    current_round = shoe_db.current_deck.current_round

    assert current_round.banker_game_info.is_stand is True, "Banker should be stand"
    assert current_round.state == 'deal_ended', "Round state is wrong"
    assert len(current_round.hit_card_sequences) == 0, "Should have 0 inside the hit card sequences"


def atest_handle_deal_ended_banker_hit_card():
    mock_obj = MockShareObj('result_data')
    mock_obj.save_to_firebase()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyResultedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 1, "Jobs not have one job inside it, resulted job"
    assert job_mgr.jobs[0].job_name == 'NotifyClosedJob', "Job name is wrong"

    shoe_db = mock_obj.retrieve_shoe_from_firebase()
    current_round = shoe_db.current_deck.current_round

    assert current_round.banker_game_info.is_stand is True, "Banker should be stand"
    assert current_round.state == 'resulted', "Round state is wrong"
    assert len(current_round.hit_card_sequences) == 0, "Should have 0 inside the hit card sequences"


def test_handle_closed():
    mock_obj = MockShareObj('closed_data')
    mock_obj.save_to_firebase()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    notify_info = round.notify_info()
    job = NotifyClosedJob(notify_info)
    job_mgr = SingletonManager.instance().job_mgr
    job_mgr.clear_jobs()

    job_mgr.handle_timeout_job(job)
    assert len(job_mgr.jobs) == 0, "Jobs not have no job inside it"

    shoe_db = mock_obj.retrieve_shoe_from_firebase()
    current_round = shoe_db.current_deck.current_round

    assert current_round.state == 'opened', "Round state should be opened"
    assert current_round.round_id != round.round_id, "Round id should not be same"
    assert current_round.hand == round.hand + 1, "Round hand should be plus 1 than prev round"