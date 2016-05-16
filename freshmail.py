import requests
import json
import hashlib

"""
subscriber status codes for use with API: (undocumented in API)
1 active
2 activation pending
3 not activated
4 resigned
5 soft bouncing
8 hard bouncing
"""

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

    def request(self, url, payload=None, raw_response=False, method='POST'):
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
        m.update(strSign.encode("utf-8"))
        headers = {
            'content-type': self.contentType,
            'X-Rest-ApiKey': self.api_key,
            'X-Rest-ApiSign': m.hexdigest()
        }
        if method is 'POST':
          r = requests.post(full_url, data=post_data, headers=headers)
        elif method is 'GET':
          r = requests.get(full_url, data=post_data, headers=headers)
        else:
          raise FreshMailException({'message':'GET or POST required methods. Got {}'.format(method)})

        self.httpCode = r.status_code

        if self.httpCode != 200 and r.json()['status'] == 'ERROR':
            # get errors
            self.errors = r.json()['errors']
            for error in r.json()['errors']:
                raise FreshMailException({'message':error['message'],'code':error['code']})

        self.response = r.json()
        self.rawResponse = r.content

        if raw_response:
            return self.rawResponse
        else:
            return self.response

    def mailText(self, email, subject, text):
        # self, url, payload=None, raw_response=False
        payload = {
            'subscriber': email,
            'subject': subject,
            'text': text
        }

        url = 'mail'
        response = self.request(url, payload)
        print(response)
        return

    def mailHtml(self, email, subject, html):
        # self, url, payload=None, raw_response=False
        payload = {
            'subscriber': email,
            'subject': subject,
            'html': html
        }

        url = 'mail'
        response = self.request(url, payload)
        print(response)
        return

    def addSubscriber(self, email, list_hash, state=3, confirm=1, custom_fields=None):
        #self, url, payload=None, raw_response=False
        payload = {
          'email' : email,
          'list' : list_hash,
          'state' : state,
          'confirm' : confirm
        }

        if custom_fields is not None and isinstance(custom_fields, dict):
          # custom fields need to be a dict
          payload['custom_fields'] = custom_fields
        else:
          raise FreshMailException({'message':'Custom fields must be a dict. Got {}'.format(custom_fields)})

        url = 'subscriber/add'
        response = self.request(url, payload)
        print(response)
        return
        
    def deleteSubscriber(self, email, list_hash):
        #self, url, payload=None, raw_response=False
        payload = {
          'email' : email,
          'list' : list_hash
        }
        url = 'subscriber/delete'
        response = self.request(url, payload)
        print(response)
        return

    def getLists(self):
        #self, url, payload=None, raw_response=False
        url = 'subscribers_list/lists'
        response = self.request(url)
        if response.get('status') and response.get('status') == 'OK':
          return response.get('lists')
        else:
          return None

    def getSubscriber(self, email, list_hash):
        #self, url, payload=None, raw_response=False
        url = 'subscriber/get/{}/{}'.format(list_hash, email)
        response = self.request(url,method='GET')
        return response

    def findSubscriber(self, email):
        #slow with large number of lists
        lists = self.getLists()
        if len(lists) > 0:
          subscribed_lists = []
          for list in lists:
            list_hash = list['subscriberListHash']
            try:
              result = self.getSubscriber(email, list_hash)
              subscribed_list = { 'list_hash' : list_hash, 'name': list['name'], 'subscriber':result}
              subscribed_lists.append(subscribed_list)
            except:
              #ignore not found errors
              pass
          
          return subscribed_lists
              
        else:
          raise FreshMailException({'message':'No lists found'})

    def findSubscriberInLists(self, email, lists):
        #slow with large number of lists
        if len(lists) > 0:
          subscribed_lists = []
          for list in lists:
            list_hash = list['subscriberListHash']
            try:
              result = self.getSubscriber(email, list_hash)
              subscribed_list = { 'list_hash' : list_hash, 'name': list['name'], 'subscriber':result}
              subscribed_lists.append(subscribed_list)
            except:
              #ignore not found errors
              pass
          
          return subscribed_lists
              
        else:
          raise FreshMailException({'message':'No lists found'})
        
    def addCustomFieldtoList(self, list, field_name, tag=None, type=0):
        url = 'subscribers_list/addField'
        payload = {
            'hash': list,
            'name' : field_name,
            'type' : type
        }
        if tag is not None:
          payload['tag'] = tag
          
        response = self.request(url,payload,method='POST')
        return response

class FreshMailException(Exception):
    pass