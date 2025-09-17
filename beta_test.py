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
img = img.resize((220, 220))
chest_img = ImageTk.PhotoImage(img)

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
canvas = tk.Canvas(root, width=screen_w, height=screen_h, highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas_bg = canvas.create_image(0, 0, image=bg_photo, anchor="nw")
canvas.bg_photo = bg_photo

def handle_choice(name):
    root.withdraw()
    
    new_win = tk.Toplevel(root)
    new_win.title(f"{name} - Pirate's Plunder")
    new_win.state('zoomed')
    new_win.config(bg="blue")
    
    tk.Label(new_win,
             text=f"Welcome to the {name} treasure room!",
             font=("Courier", 28, "bold"),
             fg="gold", bg="black").pack(pady=50)

    def go_back():
        new_win.destroy()
        
    root.deiconify()

    tk.Button(new_win,
              text="Back to Deck",
              font=("Courier", 16, "bold"),
              bg="red", fg="white",
              command=go_back).pack(pady=20)

title_x = screen_w // 2
spacing = 320
start_x = title_x - spacing
chest_y = 500

hover_img_pil = Image.open("chest_img.png").resize((250, 250))
pressed_img_pil = Image.open("chest_img.png").resize((200, 200))
hover_img = ImageTk.PhotoImage(hover_img_pil)
pressed_img = ImageTk.PhotoImage(pressed_img_pil)

movies_id = canvas.create_image(start_x, chest_y, image=chest_img, anchor="n")
books_id = canvas.create_image(start_x + spacing, chest_y, image=chest_img, anchor="n")
games_id = canvas.create_image(start_x + 2 * spacing, chest_y, image=chest_img, anchor="n")

canvas.chest_img = chest_img
canvas.hover_img = hover_img
canvas.pressed_img = pressed_img

def bind_effects(item_id, name):
    def on_enter(e):
        canvas.itemconfig(item_id, image=canvas.hover_img)

    def on_leave(e):
        canvas.itemconfig(item_id, image=canvas.chest_img)

    def on_press(e):
        canvas.itemconfig(item_id, image=canvas.pressed_img)

    def on_release(e):
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