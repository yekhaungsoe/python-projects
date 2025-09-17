import tkinter as tk
from PIL import Image, ImageTk
import pygame

pygame.mixer.init()
pygame.mixer.music.load("sea_shanty.mp3")
pygame.mixer.music.play(-1, fade_ms=4000)

root = tk.Tk()
root.title("Pirate's Plunder")
root.state('zoomed')
root.config(bg="blue")

bg_img = Image.open("pirate_bg.png")
bg_img = bg_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
bg_photo = ImageTk.PhotoImage(bg_img)

img = Image.open("chest_img.png")
# Increase base chest size to 220x220
img = img.resize((220, 220))
chest_img = ImageTk.PhotoImage(img)

# Use a Canvas so the background image is a single layer and other items
# (title text and chest images) are drawn on top. Using a Canvas prevents
# widget backgrounds (like Labels or Frames) from showing a solid color
# box over the background image — this solves the previous "white/blue
# rectangle" issue.
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
canvas = tk.Canvas(root, width=screen_w, height=screen_h, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Draw background and keep reference
canvas_bg = canvas.create_image(0, 0, image=bg_photo, anchor="nw")
canvas.bg_photo = bg_photo

# Note: the title is drawn on the canvas so it blends with the background
# image instead of being a separate Label widget which had an opaque bg.

def handle_choice(name):
    # Close or hide the main menu if you want
    root.withdraw()  # hides the main window (optional)

    # Create a new window
    new_win = tk.Toplevel(root)
    new_win.title(f"{name} - Pirate's Plunder")
    new_win.state('zoomed')  # make it full screen like the main menu
    new_win.config(bg="blue")

    # Add a label to show which choice was clicked
    tk.Label(new_win,
             text=f"Welcome to the {name} treasure room!",
             font=("Courier", 28, "bold"),
             fg="gold", bg="black").pack(pady=50)

    # Add a back button to return to the main menu
    def go_back():
        new_win.destroy()
        root.deiconify()  # show main menu again if you hid it

    tk.Button(new_win,
              text="Back to Deck",
              font=("Courier", 16, "bold"),
              bg="red", fg="white",
              command=go_back).pack(pady=20)

    # You can add more widgets here depending on the choice
    # For example, a scrollable list of movies/books/games
# Place three chest images horizontally centered
title_x = screen_w // 2  # Center the title on the screen
spacing = 320
start_x = title_x - spacing
# Lower the chests down as requested
chest_y = 500

# Create hover and pressed image variants so we can provide simple visual
# feedback when the user moves the mouse over a chest or presses it.
# We generate slightly larger (hover) and slightly smaller (pressed)
# versions with PIL and convert them to PhotoImage for the Canvas.
hover_img_pil = Image.open("chest_img.png").resize((250, 250))
pressed_img_pil = Image.open("chest_img.png").resize((200, 200))
hover_img = ImageTk.PhotoImage(hover_img_pil)
pressed_img = ImageTk.PhotoImage(pressed_img_pil)

movies_id = canvas.create_image(start_x, chest_y, image=chest_img, anchor="n")
books_id = canvas.create_image(start_x + spacing, chest_y, image=chest_img, anchor="n")
games_id = canvas.create_image(start_x + 2 * spacing, chest_y, image=chest_img, anchor="n")

# Keep references to the PhotoImage objects on the canvas object so Python
# doesn't garbage-collect them (a common Tkinter gotcha). We attach them as
# attributes of the canvas for convenience.
canvas.chest_img = chest_img
canvas.hover_img = hover_img
canvas.pressed_img = pressed_img

# Add simple text labels under each chest and bind them to the same
# hover/click behavior so users can click the label or the chest image.
# Labels removed: chests are now image-only clickable items. Use the images
# themselves for hover/press/click interactions.

# Helper to change image on hover/press for a given canvas item
# Bind hover and click effects for each chest canvas item. Using canvas
# tag_bind we can attach enter/leave/press/release handlers directly to
# the image items. The handlers swap the image to the pre-generated
# hover/pressed variants to create a simple visual effect.
def bind_effects(item_id, name):
    def on_enter(e):
        canvas.itemconfig(item_id, image=canvas.hover_img)

    def on_leave(e):
        canvas.itemconfig(item_id, image=canvas.chest_img)

    def on_press(e):
        canvas.itemconfig(item_id, image=canvas.pressed_img)

    def on_release(e):
        # restore hover or normal depending on pointer location
        canvas.itemconfig(item_id, image=canvas.hover_img)
        handle_choice(name)

    canvas.tag_bind(item_id, '<Enter>', on_enter)
    canvas.tag_bind(item_id, '<Leave>', on_leave)
    canvas.tag_bind(item_id, '<ButtonPress-1>', on_press)
    canvas.tag_bind(item_id, '<ButtonRelease-1>', on_release)

bind_effects(movies_id, 'Movies')
bind_effects(books_id, 'Books')
bind_effects(games_id, 'Games')

root.mainloop()

