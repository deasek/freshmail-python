from freshmail import FreshMail
from freshmail_config import *


fm = FreshMail(FRESHMAIL_API_KEY,FRESHMAIL_API_SECRET)
custom_fields = ['name','first_name']

lists = fm.getLists()
for list in lists:
  list_hash = list['subscriberListHash']
  for field in custom_fields:
    added = fm.addCustomFieldtoList(list_hash, field)
    print added
    
print 'done'