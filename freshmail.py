import requests
import json
import hashlib


class FreshMail(object):
    """
    Custom class for Freshmail REST API
    author: Dariusz Stepniak <stepniak.dariusz@gmail.com>

    requires Requests module:
    http://www.python-requests.org/en/latest/
    """

    response = ''
    rawResponse = ''
    httpCode = ''
    contentType = 'application/json'

    host = 'https://api.freshmail.com/'
    prefix = 'rest/'


    def __init__(self, api_key, api_secret):
        """
        Create class instance, requires api_key and api_secret
        :param api_key:
        :param api_secret:
        :return: FreshMail Instance
        """
        self.api_key = api_key
        self.api_secret = api_secret

    def setContentType(self, contentType):
        self.contentType = contentType

    def setHost(self, host):
        self.host = host

    def setPrefix(self, prefix):
        self.prefix = prefix

    def getResponse(self):
        return self.response

    def getHttpCode(self):
        return self.httpCode

    def request(self, url, payload=None, raw_resonse=False):
        """
        Makes request to REST API. Add payload data for POST request.
        :param url: API endpoint
        :param payload: POST data dict
        """
        if payload is None:
            post_data = ''
        else:
            post_data = json.dumps(payload)

        full_url = '%s%s%s' % (self.host, self.prefix, url,)

        strSign = "%s/%s%s%s%s" % (self.api_key,
                                   self.prefix,
                                   url,
                                   post_data,
                                   self.api_secret,)
        m = hashlib.sha1()
        m.update(strSign)
        headers = {
            'content-type': self.contentType,
            'X-Rest-ApiKey': self.api_key,
            'X-Rest-ApiSign': m.hexdigest()
        }
        r = requests.post(full_url, data=post_data, headers=headers)

        self.httpCode = r.status_code

        if self.httpCode != 200 and r.json()['status'] == 'ERROR':
            # get errors
            self.errors = r.json()['errors']
            for error in r.json()['errors']:
                raise FreshMailException({'message':error['message'],'code':error['code']})

        self.response = r.json()
        self.rawResponse = r.content

        if raw_resonse:
            return self.rawResponse
        else:
            return self.response

    def addSubscriber(self, email, list_hash, state=3, confirm=1, custom_fields=None):
        #self, url, payload=None, raw_resonse=False
        payload = {
          'email' : email,
          'list' : list_hash,
          'state' : state,
          'confirm' : confirm
        }
        url = 'subscriber/add'
        response = self.request(url, payload)
        print response
        return



class FreshMailException(Exception):
    pass