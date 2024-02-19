import pprint

import requests


class Processor:
    def preprocess(self, data):
        raise NotImplementedError


class WebhookProcessor(Processor):
    def __init__(self, url):
        self.url = url

    def process(self, data):
        output = requests.post(self.url, json=data)
        pprint.pprint(output)
        return output.json()


def get_processor(processor_type, config):
    if processor_type == 'webhook':
        if 'url' in config:
            url = config['url']
        else:
            raise ValueError('url is required for webhook preprocessor')
        return WebhookProcessor(url)
    else:
        raise NotImplementedError
