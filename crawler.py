# -*- coding: utf-8 -*-
# Author:  Felipe Fronchetti
# Contact: fronchettiemail@gmail.com
# IMPORTANT:
# This code is part of a side project called Octopus
try:
    import urllib2
    import time
    import datetime
    import json
except ImportError as error:
    raise ImportError(error)

# This class is responsible for performing each API request.
# Our crawler uses OAuth2 authentication. Learn more at:
# https://developer.github.com/v3/oauth/


class Crawler:

    def __init__(self, client_id, client_secret):
        self.id = client_id
        self.secret = client_secret
        self.rate_limit_remaining = None
        self.rate_limit_reset = None

    # Makes the request using OAuth Client ID and Client Secret
    # Returns a json object with the requested data
    # https://developer.github.com/v3/#schema

    def request(self, request, parameters=None):
        try:
            if parameters is None:
                print 'Processing request: ' + request
                url = 'https://api.github.com/' + request + '?client_id=' + \
                    self.id + '&client_secret=' + self.secret
            else:
                print 'Processing request: ' + request + ' ' + str(parameters)
                url = 'https://api.github.com/' + request + '?client_id=' + self.id + \
                    '&client_secret=' + self.secret + \
                    '&' + '&'.join(parameters)

            response = urllib2.urlopen(url)
            header = response.info()
            body = json.load(response)

            self.verify_rate_limit(header)

            return body

        except urllib2.URLError as error:
            raise urllib2.URLError(error)

    # Verify if GitHub API requests limit is over.
    # If it's, the crawler process goes sleep.
    # https://developer.github.com/v3/#rate-limiting

    def verify_rate_limit(self, header):

        for item in header.items():
            if 'x-ratelimit-remaining' in item:
                self.rate_limit_remaining = int(item[1])
            if 'x-ratelimit-reset' in item:
                self.rate_limit_reset = int(item[1])

        datetime_format = '%Y-%m-%d %H:%M:%S'
        datetime_reset = datetime.datetime.fromtimestamp(
            self.rate_limit_reset).strftime(datetime_format)
        datetime_now = datetime.datetime.now().strftime(datetime_format)

        print '[API] Requests Remainig:' + str(self.rate_limit_remaining)

        if self.rate_limit_remaining < 1:
            while(datetime_reset > datetime_now):
                print 'The request limit is over. The process'
                + 'is sleeping until it can be resumed.'
                print 'The limit will reset on: ' + datetime_reset
                datetime_now = datetime.datetime.now().strftime(
                    datetime_format)
                time.sleep(120)

    def get_rate_limit_remaining(self):
        return self.rate_limit_remaining

    def get_rate_limit_reset(self):
        return self.rate_limit_reset
