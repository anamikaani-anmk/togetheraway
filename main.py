from auth import login, register
from prompts import get_random_prompt
from game_tictactoe import tictactoe
def main_menu(user_id):
    while True:
        print("\n──────────────────────────")
        print("💞 TOGETHERAWAY - MAIN MENU")
        print("──────────────────────────")
        print("1. Get Daily Connection Prompt")
        print("2. Play Tic Tac Toe")
        print("3. Logout")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            print("\n💗 Your Prompt:")
            print(get_random_prompt())
        
        elif choice == "2":
            print("\n🎮 Enter partner login to play")
            partner_username = input("Partner username: ")
            partner_password = input("Partner password: ")
            partner_id = login(partner_username, partner_password)
            
            if partner_id:
                tictactoe(user_id, partner_id)
            else:
                print("❌ Partner login failed.")
        
        elif choice == "3":
            print("👋 Logged out!")
            break
        
        else:
            print("❌ Invalid choice. Try again.")


def welcome():
    while True:
        print("\n──────────────────────────────")
        print("💞 WELCOME TO TOGETHERAWAY 💞")
        print("──────────────────────────────")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Choose (1-3): ").strip()

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            user_id = login(username, password)

            if user_id:
                main_menu(user_id)

        elif choice == "2":
            username = input("New Username: ")
            password = input("New Password: ")
            register(username, password)

        elif choice == "3":
            print("🌙 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Try again.")

welcome()
