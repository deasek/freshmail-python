from freshmail import FreshMail
from freshmail_config import *

email = TEST_EMAIL

fm = FreshMail(FRESHMAIL_API_KEY,FRESHMAIL_API_SECRET)
list = '16ll8gurkq'
state = 1 #Active
confirm = 0 #Do not send confirmation email
custom_fields = {'name':'Full Name', 'first_name': 'FirstName'}
fm.addSubscriber(email,list,state,confirm,custom_fields);

