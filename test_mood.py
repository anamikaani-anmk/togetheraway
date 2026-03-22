from auth import login
from moods import log_mood, view_moods
# login as anamika
user_id = login("anamika", "love123")
# log a mood
log_mood(user_id, "happy", 9, "Feeling good today 💛")
# show mood history
view_moods(user_id)
