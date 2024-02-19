import json
import requests
from tensorfuse_python.constants import BASE_URL


class MessagesCompletionsPair:
    def __init__(self, messages, completions):
        self.messages = messages
        self.completions = completions


def log_openai_event_base(endpoint: str, token: str, requestDetails, messages, completions, baseUrl:str):
    url = baseUrl + endpoint

    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer {}".format(token)
    }
    requestDetails.update({
                    'messages' : messages, 
                    'completions': completions
                }) 
    payload=json.dumps(requestDetails)

    response = requests.request('POST', url, headers=headers, data=payload, verify=False)
    return response.status_code



def log_openai_event_using_ids(token: str, teamId: str, projectId: str, datasourceId: str, 
                               messages: list[str], completions: list[str], baseUrl=BASE_URL):
    
    endpoint = 'tensorfuse/datasource/log-openai-completion/'
    requestDetails = {
        'teamId' : teamId,
        'projectId' : projectId,
        'datasourceId': datasourceId
    }
    return log_openai_event_base(
                endpoint=endpoint, token=token, 
                requestDetails=requestDetails, 
                messages=messages, completions=completions, 
                baseUrl=baseUrl
            )


def log_openai_events_using_ids_bulk(token: str, teamId: str, projectId: str, datasourceId: str, 
                               messagesCompletionsPairs: list[MessagesCompletionsPair], baseUrl=BASE_URL):
    
    for messagesCompletionsPair in messagesCompletionsPairs:
        log_openai_event_using_ids(token=token, teamId=teamId, projectId=projectId, datasourceId=datasourceId,
                                   messages=messagesCompletionsPair.messages, completions=messagesCompletionsPair.completions,
                                   baseUrl=baseUrl
                                   )

