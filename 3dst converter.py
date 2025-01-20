import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from py3dst import Texture3dst

def convert_image_to_3dst(image_path, output_path):
    try:
        # Load the image
        image = Image.open(image_path)
        
        # Create a 3DST texture from the image
        texture = Texture3dst().fromImage(image)
        
        # Export the texture to a .3dst file
        texture.export(output_path)
        
        messagebox.showinfo("Success", f"Successfully converted to: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def convert_3dst_to_image(three_dst_path, output_path):
    try:
        # Open the .3dst texture
        texture = Texture3dst().open(three_dst_path)
        
        # Get the size of the texture
        width, height = texture.size
        
        # Copy the texture as a PIL image
        image = texture.copy(0, 0, width, height)
        
        # Save the image to the specified output path
        image.save(output_path)
        
        messagebox.showinfo("Success", f"Successfully converted to: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=(
            ("Image and 3DST Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.3dst"),
            ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"),
            ("3DST Files", "*.3dst"),
            ("All Files", "*.*"),
        )
    )
    if file_path:
        input_path_var.set(file_path)
        show_image(file_path)

def save_output_file():
    file_path = filedialog.asksaveasfilename(
        title="Save Output File",
        defaultextension=".*",
        filetypes=(
            ("PNG Files", "*.png"),
            ("JPEG Files", "*.jpg"),
            ("BMP Files", "*.bmp"),
            ("TIFF Files", "*.tiff"),
            ("3DST Files", "*.3dst"),
            ("All Files", "*.*"),
        )
    )
    if file_path:
        output_path_var.set(file_path)

def show_image(file_path):
    try:
        # Open the image and resize it for display
        if file_path.endswith(".3dst"):
            texture = Texture3dst().open(file_path)
            width, height = texture.size
            image = texture.copy(0, 0, width, height)
        else:
            image = Image.open(file_path)
        
        # Resize for preview
        image.thumbnail((400, 400))
        img_preview = ImageTk.PhotoImage(image)
        
        # Update the label to display the image
        image_label.config(image=img_preview)
        image_label.image = img_preview
    except Exception as e:
        messagebox.showerror("Error", f"Cannot load image: {e}")

def convert_file():
    input_path = input_path_var.get()
    output_path = output_path_var.get()
    if not input_path or not output_path:
        messagebox.showwarning("Warning", "Please select both input and output files!")
        return
    if mode_var.get() == "image_to_3dst":
        convert_image_to_3dst(input_path, output_path)
    elif mode_var.get() == "three_dst_to_image":
        convert_3dst_to_image(input_path, output_path)

def toggle_mode():
    if mode_var.get() == "image_to_3dst":
        mode_var.set("three_dst_to_image")
        mode_button.config(text="Switch to Convert Image to 3DST")
        input_label.config(text="Select 3DST File:")
    else:
        mode_var.set("image_to_3dst")
        mode_button.config(text="Switch to Convert 3DST to Image")
        input_label.config(text="Select Image File:")

# Initialize the GUI app
app = tk.Tk()
app.title("3DST and Image Converter")
app.geometry("600x500")

# Mode variable to track which conversion is active
mode_var = tk.StringVar(value="image_to_3dst")

# Mode switch button in the top-right corner
mode_button = tk.Button(app, text="Switch to Convert 3DST to Image", command=toggle_mode, bg="blue", fg="white")
mode_button.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

# Input file selection
input_label = tk.Label(app, text="Select Image File:")
input_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

input_path_var = tk.StringVar()
input_entry = tk.Entry(app, textvariable=input_path_var, width=50)
input_entry.grid(row=1, column=1, padx=10, pady=10)
browse_button = tk.Button(app, text="Browse", command=select_file)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Output file selection
output_path_var = tk.StringVar()
output_entry = tk.Entry(app, textvariable=output_path_var, width=50)
output_entry.grid(row=2, column=1, padx=10, pady=10)
save_button = tk.Button(app, text="Save As", command=save_output_file)
save_button.grid(row=2, column=2, padx=10, pady=10)

# Image preview area
image_label = tk.Label(app, text="Image preview will appear here", bg="gray", width=50, height=25)
image_label.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

# Convert button
convert_button = tk.Button(app, text="Convert", command=convert_file, bg="green", fg="white")
convert_button.grid(row=4, column=1, pady=10)

# Run the app
app.mainloop()
