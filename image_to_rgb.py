import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def convert_to_rgb():
    global image_path
    if image_path:
        original_image = Image.open(image_path)
        rgb_image = original_image.convert('RGB')
        rgb_image.save('image.png')
        rgb_image.show()

def open_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if image_path:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

# Create the main window
root = tk.Tk()
root.title("Image to RGB Converter")
root.configure(bg='#F0F0F0')  # Light gray background color

# Calculate the center of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - root.winfo_reqwidth()) // 2
y_coordinate = (screen_height - root.winfo_reqheight()) // 2

# Set the window to appear at the center of the screen
root.geometry(f"+{x_coordinate}+{y_coordinate}")

# Create GUI components
open_button = tk.Button(root, text="Open Image", command=open_image, padx=10, pady=5, bg='#4CAF50', fg='white')
convert_button = tk.Button(root, text="Convert to RGB", command=convert_to_rgb, padx=10, pady=5, bg='#008CBA', fg='white')
image_label = tk.Label(root, bg='#FFFFFF')  # White background color for the image display area

# Pack the GUI components
open_button.pack(pady=10)
convert_button.pack(pady=5)
image_label.pack(padx=20, pady=10, fill='both', expand=True)

# Initialize global variables
image_path = None

# Start the GUI event loop
root.mainloop()
