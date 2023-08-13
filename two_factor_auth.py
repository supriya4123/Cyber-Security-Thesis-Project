import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import bcrypt
import subprocess

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

# Validate user credentials from the database
def validate_user(username, password):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT username, salted_password, role FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()

    if result:
        stored_username, salted_password, role = result
        if bcrypt.checkpw(password.encode('utf-8'), salted_password):
            return role
        else:
            return None
    else:
        return None

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

# Function to handle the login button click
def on_login():
    username = entry_username.get()
    password = entry_password.get()

    role = validate_user(username, password)
    if role:
        session_key = generate_session_key(username, password, role)
        session_expiration = get_session_expiration(role)

        if role == 'admin' or 'other':
            root.destroy()
            subprocess.run(['python', 'main_encrypt_decrypt.py'])
        else:
            messagebox.showerror('Error', 'Invalid USER!')

    else:
        messagebox.showerror('Login Failed', 'Invalid credentials!')

# Create the main application window
root = tk.Tk()
root.title('Two Factor')
root.geometry('400x400')

# Create and place widgets on the window
label_title = tk.Label(root, text='Validate Your Account', font=('Cambria', 20))
label_title.pack(pady=20)

label_username = tk.Label(root, text='Username:', font=('Cambria'))
label_username.pack(pady=10)
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text='Password:', font=('Cambria'))
label_password.pack(pady=10)
entry_password = tk.Entry(root, show='*', font=('Cambria'))
entry_password.pack()

btn_login = tk.Button(root, text='Login', command=on_login, width=15, font=('Cambria'))
btn_login.pack(pady=30)

# Center the window on the desktop screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 400) // 2
y = (screen_height - 400) // 2
root.geometry('400x400+{}+{}'.format(x, y))

# Start the main event loop
root.mainloop()
