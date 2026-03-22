from auth import login
from partners import request_partner
# login as anamika
user_id = login("anamika", "love123")
# send partner request to 'him'
request_partner(user_id, "him")
