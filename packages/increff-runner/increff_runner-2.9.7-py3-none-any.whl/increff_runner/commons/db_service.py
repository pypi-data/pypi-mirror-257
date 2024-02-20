from commons.db_helper import *
import datetime
from commons.constants import * 
from logging_increff.function import *
import requests
from commons.event_helper import *

def change_job_to_processing_state(job):
    job["start_time"] = str(datetime.datetime.now())
    job["status"] = PROCESSING
    persist_value(JOBS_TABLE, job["id"], job)
    persist_value(INTERIM_JOBS, job["id"],{'id':job["id"]})


def change_job_to_success_state(job):
    job["status"] = SUCCESS
    job["end_time"] = str(datetime.datetime.now())
    persist_value(JOBS_TABLE, job["id"], job)
    delete_table_values(INTERIM_JOBS, job["id"])


def change_job_to_failure_state(job, reason):
    job["status"] = FAILED
    job["end_time"] = str(datetime.datetime.now())
    job["reason"] = str(reason)
    persist_value(JOBS_TABLE, job["id"], job)
    delete_table_values(INTERIM_JOBS, job["id"])


def update_job(job):
    persist_value(JOBS_TABLE, job["id"], job)
