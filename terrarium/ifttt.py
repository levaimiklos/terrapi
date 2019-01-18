#!/usr/bin/env python3

import requests

class IFTTT(object):

    def __init__(self, webhooks_key):
        self.webhooks_key = webhooks_key
        self.webhooks_url_start = "https://maker.ifttt.com/trigger/"
        self.webhooks_url_end = "/with/key/" + self.webhooks_key


    def send_webhooks_trigger(self, event = None, value1 = None, value2 = None, value3 = None):
        webhooks_url = self.webhooks_url_start + event + self.webhooks_url_end
        r = requests.post(webhooks_url, params={"value1":value1,"value2":value2,"value3":value3})
