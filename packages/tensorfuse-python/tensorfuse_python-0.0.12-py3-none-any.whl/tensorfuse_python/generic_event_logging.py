import json
from typing import Optional, Dict

import requests
import csv
from tensorfuse_python.constants import BASE_URL


def log_generic_event_base(endpoint:str, token: str, requestDetails, log, baseUrl: str, staticEvaluations:Optional[Dict] = None):
    url = baseUrl + endpoint

    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer {}".format(token)
    }
    #TODO!: confirm implementation. current assumes that user makes log JSON serialisable.
    requestDetails.update({'completionProperties' : log})
    if staticEvaluations:
        requestDetails.update({'staticEvaluations': staticEvaluations})
    payload=json.dumps(requestDetails)

    response = requests.request('POST', url, headers=headers, data=payload, verify=False)
    return response.status_code



def log_generic_event(token: str, log, baseUrl=BASE_URL, staticEvaluations:Optional[Dict] = None):
    endpoint = 'tensorfuse/datasource/log-completion-default/'
    return log_generic_event_base(endpoint=endpoint, token=token, log=log, requestDetails={}, baseUrl=baseUrl,
                                  staticEvaluations=staticEvaluations)



def log_generic_event_using_ids(token: str, teamId: str, projectId: str, datasourceId: str,  log, baseUrl=BASE_URL):
    endpoint = 'tensorfuse/datasource/log-completion/'
    requestDetails = {
        'teamId': teamId,
        'projectId': projectId,
        'datasourceId': datasourceId,
    }
    return log_generic_event_base(endpoint=endpoint, token=token, requestDetails=requestDetails, log=log, baseUrl=baseUrl)
    


def log_generic_event_using_names(token: str, teamName: str, projectName: str, datasourceName: str,  log, baseUrl=BASE_URL):
    endpoint = 'tensorfuse/datasource/log-completion-using-names/'
    requestDetails = {
        'teamName': teamName,
        'projectName': projectName,
        'datasourceName': datasourceName,
    }
    return log_generic_event_base(endpoint=endpoint, token=token, requestDetails=requestDetails, log=log, baseUrl=baseUrl)



def log_generic_events_bulk(token: str, filename=None, headers=[], logs=[], baseUrl=BASE_URL):
    if len(logs) > 0:
        for log in logs:
            log_generic_event(token=token, log=log, baseUrl=baseUrl)


    elif filename:
        if not headers:
            raise Exception("Headers Not Provided")
        
        #TODO!: conf implementation. curr assumes that file will not have headers and they will be provided separately
        with open(filename, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                # if len(headers) != len(line): #TODO: figure out implementation
                #     raise Exception("Number of columns do not match")
                # else:
                log = {}
                for i in range(len(headers)):
                    log[headers[i]] = line[i]
                log_generic_event(token=token, log=log, baseUrl=baseUrl)
