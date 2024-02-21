from logging_increff.function import *
from .mse_helper import create_events_for_next_blocks,mark_dependant_as_failed
from .constants import *
import requests
import json
from .db_service import update_job

def send_success_callback(url, output, error_data, job):
    if error_data != {}:
        send_failure_callback(url, "Script Failed", output, error_data, job)
        return
    output["caas_job_id"] = job["id"]
    add_info_logs(job["id"], "Hitting Success Callback")
    body = {
        "StatusCode": "200",
        "Output": {"output_data": output, "error_data": error_data},
    }
    add_info_logs(job["id"], f"Success message -> {str(body)}")
    job["callback_status"] = "200"
    update_job(job)
    response = requests.post(url, data=json.dumps(body))

def send_success_webhook(url,master_url, output, error_data, job):
    if error_data != {}:
        send_failure_webhook(master_url,job["data"]["task_id"],error_data,job)
        return
    
    output["caas_job_id"] = job["id"]
    add_info_logs(job["id"], "Hitting Success WebHook Callback")
    create_events_for_next_blocks(url,master_url, output, error_data, job)

def send_failure_callback(url, error, output_data, error_data, job):
    add_info_logs(job["id"], "Hitting Failure Callback")
    output_data["caas_job_id"] = job["id"]
    body = {
        "Output": {"output_data": output_data, "error_data": error_data},
        "Error": {"ErrorCode": "400", "Message": str(error)},
        "StatusCode": "400",
    }
    add_info_logs(job["id"], f" failure message -> {str(body)}")
    job["callback_status"] = 400
    update_job(job)
    response = requests.post(url, data=json.dumps(body))

def send_failure_webhook(url,task_id,error,job):
    data = {
        'task_id':task_id,
        'status':'FAILED',
        'reason':error,
        'subtask':job['data']['algo_name']
    }
    add_info_logs(job["id"], f" failure message -> {str(data)}")
    job["webhook_status"] = 400
    update_job(job)
    mark_dependant_as_failed(INTERIM_TASK_TABLE,task_id)
    response = requests.post(url, data=json.dumps(data))
