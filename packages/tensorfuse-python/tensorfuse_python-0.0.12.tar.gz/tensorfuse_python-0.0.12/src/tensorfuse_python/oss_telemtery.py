import json

import requests


def track_event(event_name: str):
    tracking_url = 'https://api.tensorfuse.io/tensorfuse/track/oss-event/'
    data = {'eventName': event_name}
    headers = {'Content-Type': 'application/json'}
    try:
        res = requests.post(tracking_url, data=json.dumps(data), headers=headers)
    except Exception as e:
        res = e
        pass
