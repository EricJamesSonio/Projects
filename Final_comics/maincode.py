import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from opening import open_app
import pygame

class Node:
    def __init__(self, page_number, image_path):
        self.page_number = page_number
        self.image_path = image_path
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.page_count = 0

    def add_page(self, image_path, position="back", before_page=None):
        self.page_count += 1
        new_node = Node(self.page_count, image_path)

        if not self.head:  
            self.head = self.tail = self.current = new_node  
        elif position == "front":
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        elif position == "before" and before_page:
            x = self.head
            while x and x.page_number != before_page:
                x = x.next
            if x:
                new_node.prev = x.prev
                new_node.next = x
                if x.prev:
                    x.prev.next = new_node
                x.prev = new_node
                if x == self.head:
                    self.head = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.renumber_pages() 
        self.save_pages()

    def remove_page(self, page_number):
        x = self.head

        while x:
            if x.page_number == page_number:
                if x == self.head and x == self.tail:
                    self.head = self.tail = self.current = None
                elif x == self.head:
                    self.head = x.next
                    if self.head:
                        self.head.prev = None
                        self.current = self.head  
                elif x == self.tail:
                    self.tail = x.prev
                    if self.tail:
                        self.tail.next = None
                        self.current = self.tail  
                else:
                    x.prev.next = x.next
                    x.next.prev = x.prev
                    self.current = x.next if x.next else x.prev 

                self.page_count -= 1
                self.reorder_page_numbers()
                self.save_pages()  
                return True 

            x = x.next
            self.save_pages()

        return False

    def search_page(self, page_number):
        x = self.head
        while x:
            if x.page_number == page_number:
                return x
            x = x.next
        return None

    def next_page(self):
        if self.current and self.current.next:
            self.current = self.current.next
        return self.current

    def prev_page(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        return self.current
    
    def get_all_pages(self):
        pages = []
        current = self.head 
        while current:
            pages.append(current) 
            current = current.next
        return pages

    def reorder_page_numbers(self):
        x = self.head
        page_number = 1
        while x:
            x.page_number = page_number
            page_number += 1
            x = x.next
            
    def save_pages(self):
        with open("pages.txt", "w") as f:
            x = self.head
            while x:
                f.write(x.image_path + "\n") 
                x = x.next

    def renumber_pages(self):
        x = self.head
        num = 1
        while x:
            x.page_number = num
            x = x.next
            num += 1


class ComicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comic Viewer")
        self.root.attributes('-fullscreen', True) 
        self.comic = DoublyLinkedList()
    
        pygame.mixer.init()
        pygame.time.wait(2000) 
        pygame.mixer.music.load("music/2.mp3") 
        pygame.mixer.music.play(-1, 0.0)
        self.design = Design(self.root, self) 
        self.load_initial_pages()
        self.show_page()
    
    def load_initial_pages(self):
        image_folder = "images"
        image_files = sorted(os.listdir(image_folder), key=lambda x: int(x.split('.')[0]))

        if os.path.exists("pages.txt"):
            with open("pages.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    self.comic.add_page(line.strip())
        else:
            for image in image_files:
                if image.endswith((".jpg", ".png", ".jpeg")):
                    self.comic.add_page(os.path.join(image_folder, image))

    def show_page(self):
        if self.comic.current:
            try:
                img = Image.open(self.comic.current.image_path)
                img = img.resize((900, 600), Image.Resampling.LANCZOS) 
                self.photo = ImageTk.PhotoImage(img)
                
                self.design.canvas.delete("all")
                self.design.canvas.create_image(450, 300, image=self.photo, anchor=tk.CENTER)
                self.design.canvas.image = self.photo
            except Exception as e:
                messagebox.showerror("Error", f"Image not found!\n{e}")
    
    def show_next(self):
        self.animate_page_turn("next")
    
    def show_prev(self):
        self.animate_page_turn("prev")
    
    def animate_page_turn(self, direction):
        current = Image.open(self.comic.current.image_path)
        current = current.resize((900, 600), Image.Resampling.LANCZOS)
        current_photo = ImageTk.PhotoImage(current)
        next_page = self.comic.next_page() if direction == "next" else self.comic.prev_page()
        if next_page:
            next = Image.open(next_page.image_path)
            next = next.resize((900, 600), Image.Resampling.LANCZOS)
            next_photo = ImageTk.PhotoImage(next)

  
            self.design.canvas.delete("all")
            self.design.canvas.create_image(450, 300, image=current_photo, anchor=tk.CENTER)
            self.design.canvas.image = current_photo
            
            self.root.update_idletasks()
            for i in range(900, 0, -10):
                self.design.canvas.delete("all")
                self.design.canvas.create_image(450 + i, 300, image=current_photo, anchor=tk.CENTER)
                self.design.canvas.create_image(450 - i, 300, image=next_photo, anchor=tk.CENTER)
                self.root.update_idletasks()
                self.root.after(10)  
            
            self.show_page()
    
    def add_page(self):
        select_window = tk.Toplevel(self.root)
        select_window.title("Select Comic Page")
        select_window.geometry("800x600")
        select_window.configure(bg='#2e2e2e')

        image_frame = tk.Frame(select_window, bg='#2e2e2e')
        image_frame.pack(pady=20)

        image_folder = "new_comics"
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        thumbnail_images = []

        for image_file in image_files:
            img_path = os.path.join(image_folder, image_file)
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            thumbnail_images.append((photo, img_path))

        rows = 3
        cols = 4
        for i, (thumbnail, img_path) in enumerate(thumbnail_images):
            row = i // cols
            col = i % cols
            thumb_frame = tk.Frame(image_frame, bg='#444444', bd=5, relief='solid')
            thumb_frame.grid(row=row, column=col, padx=10, pady=10)
            btn = tk.Button(thumb_frame, image=thumbnail, 
                            command=lambda path=img_path: self.select_image(path, select_window), bd=0)
            btn.grid(row=0, column=0)
            btn.image = thumbnail

        position_frame = tk.Frame(select_window, bg='#2e2e2e')
        position_frame.pack(pady=20)

        position_button_style = {'fg': 'black', 'bg': 'yellow', 'font': ('Comic Sans MS', 12, 'bold')}
        btn_add_front = tk.Button(position_frame, text="Add to Front", 
                                  command=lambda: self.add_to_position(None, 'front', None, select_window), 
                                  **position_button_style)
        btn_add_front.pack(side=tk.LEFT, padx=10)
        btn_choose_page = tk.Button(position_frame, text="Choose Page", 
                                    command=lambda: self.choose_page(select_window), 
                                    **position_button_style)
        btn_choose_page.pack(side=tk.LEFT, padx=10)
        btn_add_back = tk.Button(position_frame, text="Add to Back", 
                                 command=lambda: self.add_to_position(None, 'back', None, select_window), 
                                 **position_button_style)
        btn_add_back.pack(side=tk.LEFT, padx=10)

    def choose_page(self, window):
        window.destroy()  
        page_select_window = tk.Toplevel(self.root)
        page_select_window.title("Select Page to Replace")
        page_select_window.geometry("600x400")
        page_select_window.configure(bg='#2e2e2e')
        current_pages = self.comic.get_all_pages()
        page_buttons_frame = tk.Frame(page_select_window, bg='#2e2e2e')
        page_buttons_frame.pack(pady=20)
        for i, page in enumerate(current_pages):
            btn = tk.Button(page_buttons_frame, text=f"Page {i+1}", command=lambda idx=i: self.replace_page(idx, page_select_window), **{'fg': 'black', 'bg': 'yellow', 'font': ('Comic Sans MS', 12, 'bold')})
            btn.grid(row=i // 4, column=i % 4, padx=10, pady=10)

    def replace_page(self, page_idx, window):
        window.destroy() 
        image_path = self.comic.current.image_path  
        self.comic.replace_page(page_idx, image_path)
        messagebox.showinfo("Success", f"Page {page_idx+1} replaced with new image!")
        self.show_page()

    def select_position(self, position, window):
        window.destroy()  
        image_path = self.comic.current.image_path  
        self.comic.add_page(image_path, position)
        messagebox.showinfo("Success", f"Page added at {position}!")
        self.show_page()
    def select_image(self, image_path, window):
        window.destroy()
        position_window = tk.Toplevel(self.root)
        position_window.title("Choose Page Position")
        position_window.configure(bg='#2e2e2e')
        current_pages = self.comic.get_all_pages()  
        num_pages = len(current_pages)
        window_height = 150 + (num_pages * 40)
        position_window.geometry(f"600x{min(window_height, 600)}")
        canvas = tk.Canvas(position_window, bg='#2e2e2e')
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(position_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        page_selection_frame = tk.Frame(canvas, bg='#2e2e2e')
        canvas.create_window((0, 0), window=page_selection_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        button_style = {'fg': 'black', 'bg': 'yellow', 'font': ('Comic Sans MS', 12, 'bold')}
        btn_add_front = tk.Button(page_selection_frame, text="➕ Add to Front",
                                  command=lambda: self.add_to_position(image_path, 'front', None, position_window),
                                  **button_style)
        btn_add_front.pack(pady=5)
        for i, page in enumerate(current_pages):
            page_name = f"Page {i + 1}"
            btn_select_page = tk.Button(page_selection_frame, text=f"➕ Insert  {page_name}",
                                        command=lambda idx=i: self.add_to_position(image_path, 'page', idx, position_window),
                                        **button_style)
            btn_select_page.pack(pady=5)
        btn_add_back = tk.Button(page_selection_frame, text="➕ Add to Back",
                                 command=lambda: self.add_to_position(image_path, 'back', None, position_window),
                                 **button_style)
        btn_add_back.pack(pady=5)
        page_selection_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def add_to_position(self, image_path, position, page_idx=None, window=None):
        if window:
            window.destroy()

        if position == 'front':
            self.comic.add_page(image_path, 'front')
            messagebox.showinfo("Success", "Page added to the front!")
        elif position == 'back':
            self.comic.add_page(image_path, 'back')
            messagebox.showinfo("Success", "Page added to the back!")
        elif position == 'page' and page_idx is not None:
            self.comic.add_page(image_path, 'before', before_page=page_idx + 1)  # Page numbers are 1-based
            messagebox.showinfo("Success", f"Page added before Page {page_idx + 1}!")

        self.show_page()
        
    def remove_page(self):
        try:
            page_number = int(self.design.entry_search.get())
            if self.comic.remove_page(page_number):
                messagebox.showinfo("Success", f"Page {page_number} removed!")
            else:
                messagebox.showerror("Error", "Page not found!")
            self.reset_input() 
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid page number.")
    
    def search_page(self):
        try:
            page_number = int(self.design.entry_search.get())
            target_page = self.comic.search_page(page_number)
            if target_page:
                self.animate_to_page(page_number)       
            else:
                messagebox.showerror("Error", "Page not found!")
                self.reset_input() 

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid page number.")

        self.design.entry_search.delete(0, tk.END)
    
    def animate_to_page(self, target_page_number):
        def step():
            if self.comic.current.page_number == target_page_number:
                self.show_page()
                return
            
            if self.comic.current.page_number < target_page_number:
                self.comic.next_page()
            else:
                self.comic.prev_page()
            
            self.show_page()
            self.root.after(500, step)
        
        step()

    def exit_app(self):
        confirm_exit = tk.Toplevel(self.root)
        confirm_exit.title("Exit Confirmation")
        confirm_exit.geometry("400x200")
        confirm_exit.configure(bg='#1c1c1c') 
        confirm_exit.resizable(False, False)
        confirm_exit.protocol("WM_DELETE_WINDOW", lambda: None) 
        message_label = tk.Label(confirm_exit, text="Are you sure you want to exit?", 
                                 font=('Comic Sans MS', 16, 'bold'), bg='#1c1c1c', fg='white')
        message_label.grid(row=0, column=0, columnspan=2, pady=20)
        button_frame = tk.Frame(confirm_exit, bg='#1c1c1c')
        button_frame.grid(row=1, column=0, columnspan=2)
        yes_button = tk.Button(button_frame, text="Yes", command=lambda: self.quit_app(confirm_exit), 
                               fg='black', bg='yellow', font=('Comic Sans MS', 14, 'bold'))
        yes_button.grid(row=0, column=0, padx=20)
        no_button = tk.Button(button_frame, text="No", command=confirm_exit.destroy, 
                              fg='black', bg='yellow', font=('Comic Sans MS', 14, 'bold'))
        no_button.grid(row=0, column=1, padx=20)

        width = 400
        height = 200
        screen_width = confirm_exit.winfo_screenwidth()
        screen_height = confirm_exit.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        confirm_exit.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def quit_app(self, confirm_exit):
        confirm_exit.destroy()
        self.root.quit()
    def reset_input(self):
        self.entry_search.delete(0, tk.END) 

class Design:
    def __init__(self, root, comic_app):
        self.root = root
        self.comic_app = comic_app
        self.canvas = None
        self.entry_search = None
        self.btn_prev = None
        self.btn_next = None
        self.btn_add = None
        self.btn_remove = None
        self.btn_search = None
        self.btn_exit = None
        
        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg='black')
        
        self.canvas = tk.Canvas(self.root, width=900, height=600, bg='white')
        self.canvas.pack(pady=20)
        
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(side=tk.BOTTOM, pady=20)
        
        button_style = {'fg': 'black', 'bg': 'yellow', 'font': ('Comic Sans MS', 14, 'bold')}
        
        self.btn_prev = tk.Button(button_frame, text="<< Prev", command=self.comic_app.show_prev, **button_style)
        self.btn_prev.grid(row=0, column=0, padx=10)
        
        self.btn_next = tk.Button(button_frame, text="Next >>", command=self.comic_app.show_next, **button_style)
        self.btn_next.grid(row=0, column=1, padx=10)
        
        self.btn_add = tk.Button(button_frame, text="Add Page", command=self.comic_app.add_page, **button_style)
        self.btn_add.grid(row=0, column=2, padx=10)
        
        self.btn_remove = tk.Button(button_frame, text="Remove Page", command=self.comic_app.remove_page, **button_style)
        self.btn_remove.grid(row=0, column=3, padx=10)
        
        self.entry_search = tk.Entry(button_frame, font=('Comic Sans MS', 14))
        self.entry_search.grid(row=1, column=1, columnspan=2, pady=10)
        
        self.btn_search = tk.Button(button_frame, text="Search Page", command=self.comic_app.search_page, **button_style)
        self.btn_search.grid(row=1, column=3, padx=10)

        self.btn_exit = tk.Button(self.root, text="Exit", command=self.comic_app.exit_app, fg='black', bg='yellow', font=('Comic Sans MS', 14, 'bold'))
        self.btn_exit.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    

if __name__ == "__main__":
    open_app() 
    root = tk.Tk()
    app = ComicApp(root)
    root.mainloop()
