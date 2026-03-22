from auth import login
from partners import accept_partner
# login as him
user_id = login("him", "love123")
# accept partner request that has pair_id = 1
accept_partner(1)
