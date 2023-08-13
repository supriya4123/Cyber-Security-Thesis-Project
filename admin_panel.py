import tkinter as tk
from tkinter import ttk
import bcrypt
import sqlite3
from datetime import datetime, timedelta
from tkinter import messagebox
import subprocess  # Import the subprocess module

# Database setup
def create_database():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salted_password TEXT NOT NULL,
            role TEXT NOT NULL,
            session_key TEXT,
            session_expiration INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Password hashing and salting
def generate_salt_and_hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return salt, hashed_password

# Generate a random session key
def generate_session_key(username, password, role):
    session_key_data = f"{username}{password}{role}"
    return bcrypt.hashpw(session_key_data.encode('utf-8'), bcrypt.gensalt())

# Set session expiration duration based on user role in minutes
def get_session_expiration(role):
    if role == "admin":
        return 60  # 1 hour for admin
    elif role == "user":
        return 30  # 30 minutes for regular users
    else:
        return 15  # 15 minutes for other roles

# Register a new user with user entry for username and password
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    role = var_role.get()

    salt, hashed_password = generate_salt_and_hash_password(password)
    session_key = generate_session_key(username, password, role)
    session_expiration = datetime.now() + timedelta(minutes=get_session_expiration(role))

    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, salted_password, role, session_key, session_expiration) VALUES (?, ?, ?, ?, ?, ?)',
              (username, password, hashed_password, role, session_key, session_expiration.timestamp()))
    conn.commit()
    conn.close()

    label_status.config(text="User created successfully!")
    update_user_listbox()

# Update the listbox with existing users and their details
def update_user_listbox():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT username, password, role FROM users')
    users = c.fetchall()
    conn.close()

    listbox_users.delete(0, tk.END)  # Clear the listbox

    for user in users:
        username, password, role = user
        password_hidden = "*" * len(password)
        listbox_users.insert(tk.END, f"Username: {username}, Password: {password_hidden}, Role: {role}")

# Function to view users in a new window
def view_users():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT username, password, role FROM users')
    users = c.fetchall()
    conn.close()

    if users:
        user_list = "\n".join(f"Username: {user[0]}, Password: {user[1]}, Role: {user[2]}" for user in users)
        messagebox.showinfo("Registered Users", f"List of Registered Users:\n{user_list}")
    else:
        messagebox.showinfo("Registered Users", "No users found!")

# Function to handle the "Update User" button click
def update_user_click():
    root.destroy()  # Close the main window
    subprocess.run(["python", "update_user.py"])  # Run the update_user.py module

def login_page():
    root.destroy()  # Close the main window
    subprocess.run(["python", "login_page.py"])

if __name__ == "__main__":
    create_database()

    def center_window(root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")

    root = tk.Tk()
    root.title("Admin Panel")
    window_width = 600
    window_height = 600
    root.resizable(False, False)
    center_window(root, window_width, window_height)

    style = ttk.Style()
    style.theme_use("clam")  # Use the "clam" theme for ttk widgets (feel free to explore other themes)

    frame = ttk.Frame(root)
    frame.pack(pady=20)

    label_username = ttk.Label(frame, text="Username:")
    label_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = ttk.Entry(frame)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    label_password = ttk.Label(frame, text="Password:")
    label_password.grid(row=1, column=0, padx=5, pady=5)
    entry_password = ttk.Entry(frame, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    label_role = ttk.Label(frame, text="Role:")
    label_role.grid(row=2, column=0, padx=5, pady=5)
    var_role = tk.StringVar()
    var_role.set("user")
    option_menu_role = ttk.OptionMenu(frame, var_role, "user", "admin", "other")
    option_menu_role.grid(row=2, column=1, padx=5, pady=5)

    button_register = ttk.Button(frame, text="Register", command=register_user)
    button_register.grid(row=3, column=0, columnspan=2, padx=5, pady=15)

    # Add the Update User button here
    button_update_user = ttk.Button(frame, text="Update/Delete", command=update_user_click)
    button_update_user.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    label_status = ttk.Label(root, text="", foreground="green")
    label_status.pack()

    # Frame for the listbox
    frame_listbox = ttk.Frame(root)
    frame_listbox.pack(pady=10)

    label_users = ttk.Label(frame_listbox, text="List of Users:")
    label_users.pack()

    listbox_users = tk.Listbox(frame_listbox, height=10, width=60)  # Increased height and width here
    listbox_users.pack()

    update_user_listbox()

    button_view_users = ttk.Button(root, text="View Users", command=view_users)
    button_view_users.pack(pady=10)

    button_view_users = ttk.Button(root, text="Log-in page", command=login_page)
    button_view_users.pack(pady=10)


    root.mainloop()
