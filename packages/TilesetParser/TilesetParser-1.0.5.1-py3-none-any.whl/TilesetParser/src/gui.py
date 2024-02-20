import tkinter as tk
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk


def show_images(images_data):

    current_image_index = [0]

    def update_image():
        if 0 <= current_image_index[0] < len(images_data):
            image_data = images_data[current_image_index[0]]
            image_file = image_data["file"]
            similarity = image_data["similarity"]

            img = Image.open(image_file)
            img = img.resize((704, 704), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            image_label.configure(image=img)
            image_label.image = img
            info_label.config(
                text=f"File: {image_file}\nSimilarity: {similarity}\n{current_image_index[0] + 1} of {len(images_data)}")
        else:
            info_label.config(text="No more images.")

    def show_next_image():
        if current_image_index[0] < len(images_data) - 1:
            current_image_index[0] += 1
            update_image()

    def show_previous_image():
        if current_image_index[0] > 0:
            current_image_index[0] -= 1
            update_image()

    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(images_data[current_image_index[0]]['file'])
        root.update()
        messagebox.showinfo("Copy to Clipboard",
                            "File path copied to clipboard!")

    root = tk.Tk()
    root.title("Image Viewer")

    image_label = Label(root)
    image_label.pack()

    info_label = Label(root, text="", justify=tk.LEFT)
    info_label.pack()
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(fill=tk.X, expand=True)

    prev_button = Button(buttons_frame, text="Back",
                         command=show_previous_image)
    prev_button.pack(side=tk.LEFT, expand=True)

    copy_button = Button(
        buttons_frame, text="Copy path to Clipboard", command=copy_to_clipboard)
    copy_button.pack(side=tk.LEFT, expand=True)

    next_button = Button(buttons_frame, text="Next", command=show_next_image)
    next_button.pack(side=tk.RIGHT, expand=True)

    update_image()
    root.mainloop()
