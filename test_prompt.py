from auth import login
from prompts import get_random_prompt
user_id = login("anamika", "love123")
print("\n💗 Your Daily Love Prompt:")
print(get_random_prompt())
