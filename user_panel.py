import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import subprocess

class InfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Information Display")
        
        self.root.configure(bg="#f0f0f0")
        self.header_font = ("Cambria", 16, "bold")
        self.text_font = ("Cambria", 12)
        
        self.center_window()
        
        self.tab_control = ttk.Notebook(root)
        self.rsa_tab = tk.Frame(self.tab_control, bg="#f0f0f0")
        self.lsb_tab = tk.Frame(self.tab_control, bg="#f0f0f0")
        
        self.tab_control.add(self.rsa_tab, text="RSA Algorithm")
        self.tab_control.add(self.lsb_tab, text="LSB Steganography")
        
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
        self.display_rsa_info()
        self.display_lsb_info()
        
        self.proceed_button = tk.Button(root, text="PROCEED", font=self.header_font, command=self.proceed_clicked)
        self.proceed_button.pack(pady=20)
    
    def center_window(self):
        window_width = 800
        window_height = 600
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    def display_rsa_info(self):
        rsa_info = [
            "RSA Algorithm:",
            "- RSA (Rivest–Shamir–Adleman) is a widely used asymmetric cryptography algorithm.",
            "- It involves the use of a public key for encryption and a private key for decryption.",
            "- The security of RSA is based on the difficulty of factoring the product of two large prime numbers.",
            "- RSA is used for secure data transmission and digital signatures."
        ]
        rsa_label = tk.Label(self.rsa_tab, text="RSA Algorithm", font=self.header_font, bg="#f0f0f0")
        rsa_label.pack(pady=10)
        
        for info in rsa_info:
            info_label = tk.Label(self.rsa_tab, text=info, font=self.text_font, bg="#f0f0f0", anchor="w")
            info_label.pack(fill="x", padx=10)
    
    def display_lsb_info(self):
        lsb_info = [
            "LSB Image Steganography:",
            "- LSB (Least Significant Bit) steganography is a technique to hide information within an image's pixel values.",
            "- It works by replacing the least significant bits of pixel values with the hidden data bits.",
            "- LSB steganography is simple but can be vulnerable to certain attacks.",
            "- It is commonly used for hiding messages in images without causing significant visual changes."
        ]
        lsb_label = tk.Label(self.lsb_tab, text="LSB Steganography", font=self.header_font, bg="#f0f0f0")
        lsb_label.pack(pady=10)
        
        for info in lsb_info:
            info_label = tk.Label(self.lsb_tab, text=info, font=self.text_font, bg="#f0f0f0", anchor="w")
            info_label.pack(fill="x", padx=10)
    
    def proceed_clicked(self):
        root.destroy()
        subprocess.run(['python', 'two_factor_auth.py'])

if __name__ == "__main__":
    root = tk.Tk()
    app = InfoApp(root)
    root.mainloop()
