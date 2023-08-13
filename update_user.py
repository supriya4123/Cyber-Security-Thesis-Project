import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import bcrypt
import os

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

# Helper functions for database operations
def get_all_users():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM users")
    users = c.fetchall()
    conn.close()
    return users

def update_user_credentials(user_id, new_username, new_password, new_role):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    salt, hashed_password = generate_salt_and_hash_password(new_password)
    session_key = generate_session_key(new_username, hashed_password, new_role)
    session_expiration = get_session_expiration(new_role)

    c.execute("""
        UPDATE users SET 
        username = ?,
        password = ?,
        salted_password = ?,
        role = ?,
        session_key = ?,
        session_expiration = ?
        WHERE id = ?
    """, (new_username, new_password, hashed_password, new_role, session_key, session_expiration, user_id))

    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Main GUI application
class UserCredentialsApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("User Credentials Management")
        self.set_window_size_and_center(500, 300)

        self.user_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.user_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        users = get_all_users()
        for user in users:
            self.user_listbox.insert(tk.END, f"{user[0]} - {user[1]} ({user[2]})")

        self.update_button = tk.Button(self, text="Update User", command=self.update_user)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(self, text="Delete User", command=self.delete_user)
        self.delete_button.pack(pady=5)

        self.admin_panel_button = tk.Button(self, text="ADMIN PANEL", command=self.launch_admin_panel)
        self.admin_panel_button.pack(pady=5)

    def set_window_size_and_center(self, width, height):
        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates for centering the window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the window size and position
        self.geometry(f"{width}x{height}+{x}+{y}")

    def update_user(self):
        selected_index = self.user_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a user to update.")
            return

        user_id = self.user_listbox.get(selected_index[0]).split()[0]

        # Create a new window for updating user credentials
        update_window = tk.Toplevel(self)
        update_window.title("Update User Credentials")

        # Create labels and entry widgets for new username, password, and role
        tk.Label(update_window, text="New Username:").pack()
        new_username_entry = tk.Entry(update_window)
        new_username_entry.pack()

        tk.Label(update_window, text="New Password:").pack()
        new_password_entry = tk.Entry(update_window, show="*")
        new_password_entry.pack()

        tk.Label(update_window, text="New Role:").pack()
        new_role_var = tk.StringVar(update_window)
        new_role_var.set("other")
        new_role_dropdown = ttk.Combobox(update_window, textvariable=new_role_var, values=["admin", "other"])
        new_role_dropdown.pack()

        # Update button to perform the update action
        update_button = tk.Button(update_window, text="Update", command=lambda: self.perform_update(user_id, new_username_entry.get(), new_password_entry.get(), new_role_var.get(), update_window))
        update_button.pack(pady=5)

    def perform_update(self, user_id, new_username, new_password, new_role, update_window):
        if not new_username or not new_password or not new_role:
            messagebox.showerror("Error", "Please enter all the fields.")
            return

        update_user_credentials(user_id, new_username, new_password, new_role)

        messagebox.showinfo("Success", "User credentials updated successfully.")
        update_window.destroy()
        self.user_listbox.delete(0, tk.END)
        users = get_all_users()
        for user in users:
            self.user_listbox.insert(tk.END, f"{user[0]} - {user[1]} ({user[2]})")

    def delete_user(self):
        selected_index = self.user_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a user to delete.")
            return

        user_id = self.user_listbox.get(selected_index[0]).split()[0]
        delete_user(user_id)

        self.user_listbox.delete(selected_index[0])
        messagebox.showinfo("Success", "User deleted successfully.")

    def launch_admin_panel(self):
        # Close the current application window
        self.destroy()

        # Run admin_panel.py as a separate process
        os.system("python admin_panel.py")

if __name__ == "__main__":
    create_database()
    app = UserCredentialsApp()
    app.mainloop()
