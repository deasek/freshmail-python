from freshmail import FreshMail

EMAIL = '?'
API_KEY = '?'
API_SECRET = '?'

fm = FreshMail(API_KEY, API_SECRET)

email = EMAIL
list = '3ssib1rq4c'
state = 1 # Active
confirm = 1 # Do not send confirmation email
custom_fields = {}

# fm.addSubscriber(email, list, state, confirm, custom_fields)
fm.mailText(email, "Subject", "Message body")
fm.mailHtml(email, "Subject", "<h1>Message body</h1>")
