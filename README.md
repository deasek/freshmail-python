freshmail-python
================

Python class for FreshMail API

**Usage:
from .freshmail import FreshMail

#Contructor
fm = FreshMail(api_key,api_secret)

#get JSON response
response = fm.request('ping')

#get status code of response
http_code = fm.getHttpCode()

