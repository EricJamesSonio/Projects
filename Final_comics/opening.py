import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os
import pygame 

def open_app():
    pygame.mixer.init()
    pygame.time.wait(0) 
    pygame.mixer.music.load("music/1.mp3")  
    pygame.mixer.music.play(-1, 0.0) 

    root = tk.Tk()
    root.title("Opening Scene")
    root.attributes("-fullscreen", True) 
    root.configure(bg="black") 

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    text_label = tk.Label(root, text="Comic Book", font=("Impact", 60), fg="white", bg="black")
    text_label.place(relx=0.5, rely=0.5, anchor="center")  

    def animate_text(scale=1.0, alpha=1.0):
        if alpha > 0:
            new_font_size = int(60 * scale)
            text_label.config(font=("Impact", new_font_size), fg=f"#{int(alpha * 255):02x}{int(alpha * 255):02x}{int(alpha * 255):02x}")
            root.after(10, animate_text, scale * 1.05, alpha - 0.05)  
        else:
            text_label.destroy()  
            show_meme()
    root.after(800, animate_text)

    def show_meme():
        meme_path = os.path.join("memes", "meme.jpg") 
        try:
            meme_img = Image.open(meme_path)
            meme_img = meme_img.resize((int(screen_width * 0.4), int(screen_height * 0.4)), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"Error loading meme image: {e}")
            return
        meme_photo = ImageTk.PhotoImage(meme_img)
        meme_label = tk.Label(root, bg="black", image=meme_photo)
        meme_label.image = meme_photo 
        meme_label.place(relx=0.5, rely=0.5, anchor="center")  

        text_presenting = tk.Label(root, text="Presenting...", font=("Arial", 40, "bold"), fg="white", bg="black")
        text_presenting.place(relx=0.5, rely=0.75, anchor="center")
        meme_label.lift()
        text_presenting.lift()

        def fade_in_meme(alpha=0.0, text_alpha=0.0):
            if alpha < 1.0:
                meme_img_with_alpha = ImageEnhance.Brightness(meme_img).enhance(alpha)
                meme_photo = ImageTk.PhotoImage(meme_img_with_alpha)
                meme_label.config(image=meme_photo)
                meme_label.image = meme_photo  
                text_presenting.config(fg=f"#{int(text_alpha * 255):02x}{int(text_alpha * 255):02x}{int(text_alpha * 255):02x}")

        
                root.after(50, fade_in_meme, alpha + 0.05, text_alpha + 0.05)
            else:
                root.after(3000, fade_out_meme)

        def fade_out_meme(alpha=1.0, text_alpha=1.0):
            if alpha > 0:
                meme_img_with_alpha = ImageEnhance.Brightness(meme_img).enhance(alpha)
                meme_photo = ImageTk.PhotoImage(meme_img_with_alpha)
                meme_label.config(image=meme_photo)
                meme_label.image = meme_photo 

                text_presenting.config(fg=f"#{int(text_alpha * 255):02x}{int(text_alpha * 255):02x}{int(text_alpha * 255):02x}")
    
                root.after(50, fade_out_meme, alpha - 0.05, text_alpha - 0.05) 
            else:
                meme_label.destroy() 
                text_presenting.destroy()  
                show_spiderman_image() 
        fade_in_meme()

    def show_spiderman_image():
        img_width = int(screen_width * 0.6)
        img_height = int(screen_height * 0.7)
        image_path = os.path.join("opening", "amazing_spiderman_cover.jpg")
        try:
            img = Image.open(image_path)
            img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"Error loading image: {e}")
            return

        img_label = tk.Label(root, bg="black")
        img_label.place(x=(screen_width - img_width) // 2, y=(screen_height - img_height) // 2) 

        def fade_in_out(alpha=0, fade_in=True):
            """Handles the fade-in and fade-out effect for the image."""
            if 0 <= alpha <= 1:
                img_with_alpha = ImageEnhance.Brightness(img).enhance(alpha)
                photo = ImageTk.PhotoImage(img_with_alpha)
                img_label.config(image=photo)
                img_label.image = photo 
                next_alpha = alpha + 0.05 if fade_in else alpha - 0.05
                root.after(20, fade_in_out, next_alpha, fade_in)
            elif fade_in:
                root.after(3500, fade_in_out, 1, False)  
            else:
                root.destroy()  
        fade_in_out()

    root.mainloop()

if __name__ == "__main__":
    open_app()
