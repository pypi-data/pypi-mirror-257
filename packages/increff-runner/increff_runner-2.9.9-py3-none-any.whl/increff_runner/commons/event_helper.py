import json
import requests

def create_caas_job(url,data):
    data['subject'] = 'mse-runner'
    response = requests.post(url, data=json.dumps(data))
    return response.json()