import sys
import os

# Add the parent directory (src) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import json
import unittest
from unittest.mock import Mock
from logger import Logger
from job_system.job_manager import JobManager
from mock_share_obj import MockShareObj
from utils.util import Util
from job_system.jobs.notify_job import *


def test_add_jobs():
    mock_obj = MockShareObj()
    shoe = mock_obj.shoe
    round = shoe.current_deck.current_round

    job_mgr = JobManager.instance()
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

    print(job_mgr)