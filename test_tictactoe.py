from auth import login
from game_tictactoe import tictactoe

print("Login Player 1:")
p1 = login("anamika", "love123")

print("\nLogin Player 2:")
p2 = login("him", "love123")       

tictactoe(p1, p2)
