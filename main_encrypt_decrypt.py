import tkinter as tk
from math import gcd
import random
from PIL import Image
from image_stegan import Encode, Decode
import math
from tkinter import messagebox
import subprocess

letter = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",",",".","!","?"," "]
number = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

def cipher(num,e):
    for i in range(len(num)):
        X.append((int(num[i])**e)%n)
        
def decipher(num,d):
    for i in range(len(num)):
        Y.append((int(num[i])**d)%n)
        
def gcd(a, b):
    while b != 0:
        (a, b)=(b, a % b)
    return a

def phi(n):
    amount = 0
    for k in range(1, n + 1):
        if math.gcd(n, k) == 1:
            amount += 1
    return amount

def Decrypt():
    global i,j,Y
    Y=[]
    encoded_image_file = "enc_image.png"

    img2 = Image.open(encoded_image_file)
    # print(img2, img2.mode)

    hidden_text = Decode(img2)

    # print(hidden_text)

    decipher(hidden_text,d)
    numD=[]
    for i in range(len(Y)):
        for j in range(len(number)):
            if(Y[i]==int(number[j])):
                numD.append(letter[j])

    # for i in numD:
    #     print(i,end="")

    # output = " ".join(str(i) for i in numD)
    output = "".join(numD) 

    # print("Message in clear text: ", output)
    messagebox.showinfo("Message in clear text is: ", output)

    window.destroy()
    subprocess.run(['python', 'two_factor_auth.py'])
    

def Encrypt(plaintext_entry):
    # Encrypts a plaintext message using the current key
    global plaintext, numC, j, X
    X = []
    plaintext = plaintext_entry.get("1.0", "end-1c")  # Get text from the text box
    plaintext = plaintext.lower()
    numC = []
    for i in range(len(plaintext)):
        for j in range(len(letter)):
            if plaintext[i] == letter[j]:
                numC.append(number[j])
    cipher(numC, e)
    
    encrypted_text_message = "Encrypted text in numbers: " + ', '.join(map(str, X))
    messagebox.showinfo("Encrypted Text", encrypted_text_message)

    # Display the number of encrypted blocks using a message box
    num_blocks_message = "Number of encrypted blocks: " + str(len(X))
    messagebox.showinfo("Number of Encrypted Blocks", num_blocks_message)

    original_image_file = "image.png"
    img = Image.open(original_image_file)

    # print(img, img.mode)

    encoded_image_file = "enc_" + original_image_file

    img_encoded = Encode(img, plaintext, X)
    if img_encoded:
        img_encoded.save(encoded_image_file)
        
        message = "'{}' saved!".format(encoded_image_file)
        messagebox.showinfo("Image Saved", message)

def on_decrypt_button():
    Decrypt()

# Initialize n, e, and d
n = 2537
e = 13
d = 937

# Create the GUI window
window = tk.Tk()
window.title("RSA Encryption/Decryption")

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate window position for centering
window_width = 300
window_height = 350
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set window dimensions and position
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create and place widgets
n_label = tk.Label(window, text="MODULUS: 2537", font="Cambria")
n_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

e_label = tk.Label(window, text="EXPONENT: 13", font="Cambria")
e_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

d_label = tk.Label(window, text="PRIVATE COMPONENT: 937", font="Cambria")
d_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Create a text box for entering plaintext
plaintext_textbox = tk.Text(window, height=5, width=30, font="Cambria")
plaintext_textbox.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

encrypt_button = tk.Button(window, text="Encrypt", command=lambda: Encrypt(plaintext_textbox), font="Cambria")
encrypt_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

decrypt_button = tk.Button(window, text="Decrypt", command=on_decrypt_button, font="Cambria")
decrypt_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

window.mainloop()

