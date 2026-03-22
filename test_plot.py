from auth import login
from plot_mood import plot_mood
user_id = login("anamika", "love123")
plot_mood(user_id)
