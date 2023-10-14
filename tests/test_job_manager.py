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

def test_handle_bet_ended_timeout_job():
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