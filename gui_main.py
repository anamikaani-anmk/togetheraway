import customtkinter as ctk
from tkinter import messagebox, filedialog
from auth import login, register, get_pair_id
from prompts import get_random_prompt
from game_tictactoe import tictactoe_gui
from photo_wall import save_photo, get_photos
from diary import add_private_entry, get_private_entries, add_shared_entry, get_shared_entries
from moods import log_mood
from config import get_db
from PIL import Image, ImageTk
import datetime
from auth import get_partner_id, get_pair_id
from love import get_start_date, set_start_date
from bucket_list import add_bucket_item, get_bucket_items, get_done_items, complete_item
from moods import get_moods_by_date
from auth import get_pair_id, get_partner_id
import datetime
from plot_mood import plot_mood





# --- Theme ---
PRIMARY = "#ff8fb7"
PRIMARY_HOVER = "#ff6b98"
BG = "#ffe6ef"
TEXT = "#5a3e47"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("TogetherAway 💗")
app.geometry("380x520")
app.configure(fg_color=BG)

def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def home_btn(parent, user_id=None):
    """fixed home icon button"""
    btn = ctk.CTkButton(parent, text="🏠", width=35, height=30,
                        fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                        command=(lambda: menu_screen(user_id)) if user_id else welcome_screen)
    btn.place(relx=0.92, rely=0.02, anchor="ne")

# --- Screens ---

def welcome_screen():
    clear(main_frame)
    ctk.CTkLabel(main_frame, text="💞 TOGETHERAWAY 💞",
                 font=("Arial", 26, "bold"), text_color=TEXT).pack(pady=40)
    ctk.CTkButton(main_frame, text="Login", width=200,
                  fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                  command=login_screen).pack(pady=12)
    ctk.CTkButton(main_frame, text="Register", width=200,
                  fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                  command=register_screen).pack(pady=12)
    ctk.CTkButton(main_frame, text="Exit", width=200,
                  fg_color="#ff6b81", hover_color="#ff5670",
                  command=app.destroy).pack(pady=25)

def login_screen():
    clear(main_frame)
    ctk.CTkLabel(main_frame, text="💗 Login", font=("Arial", 22, "bold"), text_color=TEXT).pack(pady=20)
    username = ctk.CTkEntry(main_frame, placeholder_text="Username", width=220)
    password = ctk.CTkEntry(main_frame, placeholder_text="Password", show="*", width=220)
    username.pack(pady=8); password.pack(pady=8)

    def attempt():
        user_id = login(username.get(), password.get())
        if user_id: menu_screen(user_id)
        else: messagebox.showerror("Error", "Wrong username or password")

    ctk.CTkButton(main_frame, text="Login", width=200,
                  fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                  command=attempt).pack(pady=18)
    ctk.CTkButton(main_frame, text="Back", width=200,
                  fg_color="#d3b9c4", hover_color="#caa6b6",
                  command=welcome_screen).pack()

def register_screen():
    clear(main_frame)
    ctk.CTkLabel(main_frame, text="📝 Register", font=("Arial", 22, "bold"), text_color=TEXT).pack(pady=20)
    username = ctk.CTkEntry(main_frame, placeholder_text="Choose Username", width=220)
    password = ctk.CTkEntry(main_frame, placeholder_text="Choose Password", show="*", width=220)
    username.pack(pady=8); password.pack(pady=8)

    def attempt():
        register(username.get(), password.get())
        messagebox.showinfo("Done", "Account created ✅")
        welcome_screen()

    ctk.CTkButton(main_frame, text="Create Account", width=200,
                  fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                  command=attempt).pack(pady=18)
    ctk.CTkButton(main_frame, text="Back", width=200,
                  fg_color="#d3b9c4", hover_color="#caa6b6",
                  command=welcome_screen).pack()

def menu_screen(user_id):
    clear(main_frame); home_btn(main_frame, user_id)
    ctk.CTkLabel(main_frame, text="🏠 Home",
                 font=("Arial", 22, "bold"), text_color=TEXT).pack(pady=25)

    buttons = [
        ("💞 Link Partner", lambda: link_partner_screen(user_id)),
        ("💗 Get Daily Prompt", lambda: messagebox.showinfo("Your Prompt", get_random_prompt())),
        ("🎮 Play Tic Tac Toe", lambda: partner_login(user_id)),
        ("🖼 Add Photo to Wall", lambda: add_photo_screen(user_id)),
        ("📷 View Photo Wall", lambda: view_photo_wall(user_id)),
        ("📝 My Diary", lambda: private_diary_screen(user_id)),
        ("📔 Our Shared Diary", lambda: shared_diary_screen(user_id)),
        ("🧠 Mood Tracker", lambda: mood_screen(user_id)),
        ("💞 Mood Comparison", lambda: compare_mood_screen(user_id)),
        ("💞 Love Counter", lambda: love_counter_screen(user_id)),
        ("🎯 Shared Bucket List", lambda: bucket_list_screen(user_id)),

        


    ]
    for text, cmd in buttons:
        ctk.CTkButton(main_frame, text=text, width=220,
                      fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                      command=cmd).pack(pady=8)

    ctk.CTkButton(main_frame, text="🚪 Logout", width=220,
                  fg_color="#ff6b81", hover_color="#ff5670",
                  command=welcome_screen).pack(pady=20)

def partner_login(user_id):
    clear(main_frame); home_btn(main_frame, user_id)
    ctk.CTkLabel(main_frame, text="Partner Login", font=("Arial", 20, "bold"), text_color=TEXT).pack(pady=20)
    u = ctk.CTkEntry(main_frame, placeholder_text="Partner Username", width=220)
    p = ctk.CTkEntry(main_frame, placeholder_text="Partner Password", show="*", width=220)
    u.pack(pady=6); p.pack(pady=6)

    def start_game():
        partner_id = login(u.get(), p.get())
        if partner_id: tictactoe_gui(user_id, partner_id)
        else: messagebox.showerror("Error", "Partner login failed")

    ctk.CTkButton(main_frame, text="Start Game 💞", width=200,
                  fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                  command=start_game).pack(pady=15)
    ctk.CTkButton(main_frame, text="Back", width=200,
                  fg_color="#d3b9c4", hover_color="#caa6b6",
                  command=lambda: menu_screen(user_id)).pack()
def link_partner_screen(user_id):
    clear(main_frame)
    home_btn(main_frame, user_id)

    ctk.CTkLabel(main_frame, text="Link Your Partner 💞", 
                 font=("Poppins", 22, "bold"), text_color=TEXT).pack(pady=20)

    username_entry = ctk.CTkEntry(main_frame, placeholder_text="Partner Username", width=240)
    username_entry.pack(pady=10)

    def link():
        from auth import link_partner
        success, msg = link_partner(user_id, username_entry.get())
        if success:
            messagebox.showinfo("Done 💗", msg)
            menu_screen(user_id)
        else:
            messagebox.showerror("Oops", msg)

    ctk.CTkButton(main_frame, text="Link 💞", width=200, fg_color=PRIMARY,
                  hover_color=PRIMARY_HOVER, command=link).pack(pady=15)

    ctk.CTkButton(main_frame, text="Back", width=200,
                  command=lambda: menu_screen(user_id)).pack(pady=15)


def add_photo_screen(user_id):
    clear(main_frame); home_btn(main_frame, user_id)
    ctk.CTkLabel(main_frame, text="Add Photo to Wall 💗", font=("Poppins", 20, "bold")).pack(pady=20)

    def choose_file():
        fp = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp")])
        if fp:
            save_photo(user_id, fp)
            messagebox.showinfo("Done 💞", "Photo added to your Wall!")
            menu_screen(user_id)

    ctk.CTkButton(main_frame, text="Choose Photo", width=200, command=choose_file).pack(pady=10)
    ctk.CTkButton(main_frame, text="Back", width=200,
                  command=lambda: menu_screen(user_id)).pack(pady=10)

def view_photo_wall(user_id):
    clear(main_frame); home_btn(main_frame, user_id)
    ctk.CTkLabel(main_frame, text="Your Photo Wall 📷💞", font=("Poppins", 20, "bold")).pack(pady=10)
    photos = get_photos(user_id)
    if not photos:
        ctk.CTkLabel(main_frame, text="No photos yet... 💭", font=("Poppins", 14)).pack(pady=20)
    else:
        for p in photos:
            try:
                img = Image.open(p); img.thumbnail((180,180))
                tk_img = ImageTk.PhotoImage(img)
                panel = ctk.CTkLabel(main_frame, image=tk_img, text=""); panel.image = tk_img; panel.pack(pady=6)
            except: continue
    ctk.CTkButton(main_frame, text="Back", width=200,
                  command=lambda: menu_screen(user_id)).pack(pady=12)

def private_diary_screen(user_id):
    clear(main_frame); home_btn(main_frame, user_id)
    ctk.CTkLabel(main_frame, text="My Diary 📝💗", font=("Poppins", 20, "bold"), text_color=TEXT).pack(pady=10)
    entry_box = ctk.CTkTextbox(main_frame, width=300, height=120); entry_box.pack(pady=8)

    def save_entry():
        text = entry_box.get("1.0","end").strip()
        if text: add_private_entry(user_id, text); private_diary_screen(user_id)

    ctk.CTkButton(main_frame, text="Save", width=200, fg_color=PRIMARY, command=save_entry).pack(pady=8)
    for e in get_private_entries(user_id):
        ctk.CTkLabel(main_frame, text=f"{e['created_at'].strftime('%b %d, %Y')}: {e['content']}",
                     anchor="w", font=("Poppins", 12), text_color=TEXT).pack(pady=3)
    ctk.CTkButton(main_frame, text="Back", width=200,
                  command=lambda: menu_screen(user_id)).pack(pady=10)

def shared_diary_screen(user_id):
    clear(main_frame); home_btn(main_frame, user_id)
    pair_id = get_pair_id(user_id)
    if not pair_id:
        ctk.CTkLabel(main_frame, text="No partner linked yet 💭", font=("Poppins", 14)).pack(pady=20)
        ctk.CTkButton(main_frame, text="Back", width=200,
                      command=lambda: menu_screen(user_id)).pack(); return
    ctk.CTkLabel(main_frame, text="Our Shared Diary 📔💞",
                 font=("Poppins", 20, "bold"), text_color=TEXT).pack(pady=10)
    entry_box = ctk.CTkTextbox(main_frame, width=300, height=120); entry_box.pack(pady=8)

    def save_shared():
        text = entry_box.get("1.0","end").strip()
        if text: add_shared_entry(pair_id, user_id, text); shared_diary_screen(user_id)

    ctk.CTkButton(main_frame, text="Save to Shared Diary", width=240,
                  fg_color=PRIMARY, command=save_shared).pack(pady=8)
    for e in get_shared_entries(pair_id):
        ctk.CTkLabel(main_frame, text=f"{e['username']} ✍️: {e['content']} ({e['created_at'].strftime('%b %d')})",
                     anchor="w", font=("Poppins", 12), text_color=TEXT).pack(pady=3)
    ctk.CTkButton(main_frame, text="Back", width=200,
                  command=lambda: menu_screen(user_id)).pack(pady=10)

def mood_screen(user_id):
    clear(main_frame); home_btn(main_frame, user_id)
    ctk.CTkLabel(main_frame, text="🧠 Mood Tracker", font=("Poppins", 22, "bold"), text_color=TEXT).pack(pady=12)
    mood_tag = ctk.CTkOptionMenu(main_frame, values=["Happy 😊","Sad 😔","Stressed 😣","Excited 🤩","Calm 🫶","Angry 😤"], width=220)
    mood_tag.pack(pady=10); mood_tag.set("Happy 😊")
    rating = ctk.CTkSlider(main_frame, from_=1, to=10, number_of_steps=9, width=200); rating.set(5); rating.pack(pady=10)
    rating_label = ctk.CTkLabel(main_frame, text="Rating: 5/10", font=("Poppins",14), text_color=TEXT); rating_label.pack(pady=5)
    rating.configure(command=lambda v: rating_label.configure(text=f"Rating: {int(v)}/10"))
    mood_note = ctk.CTkEntry(main_frame, placeholder_text="Add a short note (optional)", width=250); mood_note.pack(pady=10)

    def save():
        tag = mood_tag.get(); rate = int(rating.get()); note = mood_note.get()
        log_mood(user_id, tag, rate, note); messagebox.showinfo("Saved 💞","Your mood has been recorded today."); mood_screen(user_id)

    ctk.CTkButton(main_frame, text="Save Mood 📝", width=200, fg_color=PRIMARY,
                  hover_color=PRIMARY_HOVER, command=save).pack(pady=15)
    ctk.CTkButton(main_frame, text="View History 📜", width=200, fg_color="#d3b9c4",
                  hover_color="#caa6b6", command=lambda: mood_history_screen(user_id)).pack(pady=10)
    ctk.CTkButton(main_frame, text="Back", width=200, command=lambda: menu_screen(user_id)).pack(pady=15)

def mood_history_screen(user_id):
    clear(main_frame); home_btn(main_frame, user_id)
    ctk.CTkLabel(main_frame, text="📜 Mood History", font=("Poppins",22,"bold"), text_color=TEXT).pack(pady=10)
    conn=get_db(); cur=conn.cursor(dictionary=True)
    cur.execute("SELECT mood_date, mood_tag, rating, mood_note FROM moods WHERE user_id=%s ORDER BY mood_date DESC LIMIT 20",(user_id,))
    moods=cur.fetchall(); cur.close(); conn.close()
    if not moods:
        ctk.CTkLabel(main_frame, text="No moods logged yet 💭", font=("Poppins",14), text_color=TEXT).pack(pady=20)
    else:
        box=ctk.CTkTextbox(main_frame, width=300, height=250); box.pack(pady=10)
        for m in moods:
            box.insert("end",f"{m['mood_date']} — {m['mood_tag']} ({m['rating']}/10)\n{m['mood_note']}\n\n")
        box.configure(state="disabled")
    ctk.CTkButton(main_frame, text="Back", width=200, command=lambda: mood_screen(user_id)).pack(pady=15)
    ctk.CTkButton(main_frame, text="View Mood Graph 📊", width=200,
              fg_color="#b48ce3", hover_color="#9c6fde",
              command=lambda: plot_mood(user_id)).pack(pady=10)

from love import get_start_date, days_together, next_monthiversary, next_anniversary
from auth import get_pair_id
import datetime
from tkinter import simpledialog

def love_counter_screen(user_id):
    clear(main_frame); home_btn(main_frame, user_id)

    pair_id = get_pair_id(user_id)
    if not pair_id:
        ctk.CTkLabel(main_frame, text="No partner linked yet 💭", font=("Poppins", 16)).pack(pady=20)
        ctk.CTkButton(main_frame, text="Back", width=200, command=lambda: menu_screen(user_id)).pack()
        return

    start_date = get_start_date(pair_id)

    # If no date, ask user to set it
    if not start_date:
        ctk.CTkLabel(main_frame, text="You haven't set a relationship start date yet 💞",
                     font=("Poppins", 14)).pack(pady=20)

        def pick_date():
            date_str = simpledialog.askstring("Set Date", "Enter date (YYYY-MM-DD):")
            if date_str:
                try:
                    d = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    set_start_date(pair_id, d)
                    love_counter_screen(user_id)
                except:
                    messagebox.showerror("Error", "Enter date in correct format!")

        ctk.CTkButton(main_frame, text="Set Relationship Date 💗", width=220,
                      fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                      command=pick_date).pack(pady=10)

        ctk.CTkButton(main_frame, text="Back", width=200,
                      command=lambda: menu_screen(user_id)).pack(pady=20)
        return

    # If date exists → calculate counters
    today = datetime.date.today()
    days_together = (today - start_date).days
    next_anniv = datetime.date(today.year, start_date.month, start_date.day)
    if next_anniv < today:
        next_anniv = datetime.date(today.year+1, start_date.month, start_date.day)
    days_left = (next_anniv - today).days

    # UI
    ctk.CTkLabel(main_frame, text="🥰 Love Counter 🥰", font=("Poppins", 24, "bold")).pack(pady=10)
    ctk.CTkLabel(main_frame, text=f"Together Since: {start_date.strftime('%d %b %Y')}",
                 font=("Poppins", 16)).pack(pady=10)

    ctk.CTkLabel(main_frame, text=f"Days Together: {days_together} 💞",
                 font=("Poppins", 18, "bold")).pack(pady=10)

    ctk.CTkLabel(main_frame, text=f"Days Until Next Anniversary: {days_left} 🎉",
                 font=("Poppins", 16)).pack(pady=10)

    ctk.CTkButton(main_frame, text="Change Date 💗", width=200,
                  fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                  command=lambda: set_start_date(pair_id, simpledialog.askstring("Set Date", "YYYY-MM-DD"))).pack(pady=10)

    ctk.CTkButton(main_frame, text="Back", width=200,
                  command=lambda: menu_screen(user_id)).pack(pady=20)
from bucket_list import add_bucket_item, get_bucket_items, get_done_items, complete_item
from auth import get_pair_id

def bucket_list_screen(user_id):
    clear(main_frame); home_btn(main_frame, user_id)
    
    pair_id = get_pair_id(user_id)
    if not pair_id:
        ctk.CTkLabel(main_frame, text="No partner linked yet 💭").pack(pady=20)
        ctk.CTkButton(main_frame, text="Back", width=200,
                      command=lambda: menu_screen(user_id)).pack()
        return

    ctk.CTkLabel(main_frame, text="🎯 Shared Bucket List", font=("Poppins", 20, "bold")).pack(pady=10)

    title_box = ctk.CTkEntry(main_frame, placeholder_text="Bucket list item (e.g., Goa trip 💖)", width=260)
    title_box.pack(pady=5)

    desc_box = ctk.CTkEntry(main_frame, placeholder_text="Short description (optional)", width=260)
    desc_box.pack(pady=5)

    def add_item():
        t = title_box.get().strip()
        d = desc_box.get().strip()
        if t:
            add_bucket_item(pair_id, t, d)
            bucket_list_screen(user_id)

    ctk.CTkButton(main_frame, text="Add 💞", width=200,
                  fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                  command=add_item).pack(pady=8)

    ctk.CTkLabel(main_frame, text="Pending Goals 🕒", font=("Poppins",16)).pack(pady=6)
    for item in get_bucket_items(pair_id):
        ctk.CTkButton(main_frame, text=f"✅ {item['title']}",
                      width=260,
                      command=lambda i=item['item_id']: (complete_item(i), bucket_list_screen(user_id))).pack(pady=3)

    ctk.CTkLabel(main_frame, text="Completed Goals 🎉", font=("Poppins",16)).pack(pady=15)
    for item in get_done_items(pair_id):
        ctk.CTkLabel(main_frame, text=f"🎀 {item['title']}", font=("Poppins",12)).pack()

    ctk.CTkButton(main_frame, text="Back", width=200,
                  command=lambda: menu_screen(user_id)).pack(pady=15)
def compare_mood_screen(user_id):
    clear(main_frame); home_btn(main_frame, user_id)

    pair_id = get_pair_id(user_id)
    if not pair_id:
        ctk.CTkLabel(main_frame, text="No partner linked yet 💭", font=("Poppins", 14)).pack(pady=20)
        ctk.CTkButton(main_frame, text="Back", width=200,
                      command=lambda: menu_screen(user_id)).pack()
        return

    ctk.CTkLabel(main_frame, text="💞 Compare Moods", font=("Poppins", 22, "bold"), text_color=TEXT).pack(pady=12)

    date_entry = ctk.CTkEntry(main_frame, placeholder_text="Enter date (YYYY-MM-DD)", width=240)
    date_entry.pack(pady=8)

    result_box = ctk.CTkTextbox(main_frame, width=300, height=260)
    result_box.pack(pady=10)

    def check():
        d = date_entry.get().strip()
        try:
            datetime.date.fromisoformat(d)
        except:
            result_box.delete("1.0","end")
            result_box.insert("end","⚠ Invalid date format. Use YYYY-MM-DD.")
            return

        data = get_moods_by_date(pair_id, d)

        result_box.delete("1.0","end")
        if not data:
            result_box.insert("end","☁ No mood data for this date.")
            return

        for row in data:
            name = "You" if row["user_id"] == user_id else "Partner"
            result_box.insert("end", f"{name}: {row['mood_tag']} ({row['rating']}/10)\n{row['mood_note']}\n\n")

    ctk.CTkButton(main_frame, text="Compare 💞", width=200,
                  fg_color=PRIMARY, hover_color=PRIMARY_HOVER, command=check).pack(pady=10)

    ctk.CTkButton(main_frame, text="Back", width=200,
                  command=lambda: menu_screen(user_id)).pack(pady=15)





main_frame = ctk.CTkFrame(app, fg_color=BG)
main_frame.pack(fill="both", expand=True)
welcome_screen()
app.mainloop()
