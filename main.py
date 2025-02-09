import tkinter as tk
from openning import openning
from tkinter import messagebox, ttk
import time
from genesis import verses


class Node:
    def __init__(self, verse, reference):
        self.verse = verse
        self.reference = reference
        self.prev = None
        self.next = None

class Genesis:
    def __init__(self, text_widget):
        self.head = None
        self.tail = None
        self.current_node = None
        self.page_nodes = []
        self.current_page = 0
        self.text_widget = text_widget
        self.highlighted_verse = None
    def add_verse(self, verse, reference):
        new_node = Node(verse, reference)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
    def turn_page(self):
        current_node = self.head
        words_per_page = 150
        current_page = []
        word_count = 0
        while current_node:
            verse_text = current_node.verse
            word_count += len(verse_text.split())
            current_page.append(current_node)
            if word_count >= words_per_page:
                self.page_nodes.append(current_page)
                current_page = []
                word_count = 0
            current_node = current_node.next
        if current_page:
            self.page_nodes.append(current_page)

    def display_page(self):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        current_page_nodes = self.page_nodes[self.current_page]
        for node in current_page_nodes:
            verse_text = node.verse
            verse_display = f"{node.reference}: {verse_text}\n"
            if node == self.highlighted_verse:
                self.text_widget.insert(tk.END, verse_display, "highlight")
            else:
                self.text_widget.insert(tk.END, verse_display, "normal_text")
        self.text_widget.config(state=tk.DISABLED)

    def next_page(self):
        if self.current_page < len(self.page_nodes) - 1:
            self.current_page += 1
            self.display_page()
        else:
            messagebox.showinfo("End", "You've reached the end of the chapters.")

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()
        else:
            messagebox.showinfo("Start", "You're at the beginning of the chapters.")

    def next_verse(self):
        if self.highlighted_verse and self.highlighted_verse.next:
            self.highlighted_verse = self.highlighted_verse.next
            self.display_page()
        else:
            messagebox.showinfo("End of Verses", "You're at the last verse.")

    def prev_verse(self):
        if self.highlighted_verse and self.highlighted_verse.prev:
            self.highlighted_verse = self.highlighted_verse.prev
            self.display_page()
        else:
            messagebox.showinfo("Start of Verses", "You're at the first verse.")

    def find_verse(self, target_reference):
        current_node = self.head
        while current_node:
            if current_node.reference == target_reference:
                self.highlight(current_node)
                return
            current_node = current_node.next
        messagebox.showinfo("Not Found", "Verse not found.")

    def highlight(self, target_node):
        step_delay = 500
        current_node = self.highlighted_verse

        if current_node == target_node:
            return

        direction = (1 if self.get_node_index(current_node) < self.get_node_index(target_node) else -1)

        def step():
            nonlocal current_node
            if current_node == target_node:
                return
            current_node = current_node.next if direction == 1 else current_node.prev
            self.highlighted_verse = current_node
            self.display_page()
            self.text_widget.after(step_delay, step)
        step()

    def get_node_index(self, node):
        index = 0
        current = self.head
        while current:
            if current == node:
                return index
            current = current.next
            index += 1
        return -1

def exit(window):
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        window.destroy()

def main():
    window = tk.Tk()
    window.title("Genesis Chapter 1")
    window.attributes("-fullscreen", True)
    window.config(bg="#f5f5dc")
    frame = tk.Frame(window, bg="#8B4513", bd=5, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    text_widget = tk.Text(
        frame,
        wrap=tk.WORD,
        font=("Garamond", 16),
        height=15,
        width=80,
        padx=10,
        pady=10,
        bg="#f9f6ef",
        fg="#4B2E1F",
    )
    text_widget.pack(padx=10, pady=10)

    text_widget.tag_configure(
        "highlight",
        background="#FFD700",
        foreground="#000000",
        font=("Garamond", 16, "bold"),
    )
    text_widget.tag_configure("normal_text", foreground="#4B2E1F")

    button_frame = tk.Frame(window, bg="#f5f5dc")
    button_frame.pack(side=tk.BOTTOM, pady=10)

    btn_prev_page = tk.Button(
        button_frame,
        text="Previous Page",
        command=lambda: genesis.prev_page(),
        font=("Helvetica", 12, "bold"),
        bg="#8B4513",
        fg="white",
        width=15,
    )
    btn_prev_page.pack(side=tk.LEFT, padx=10)

    btn_next_page = tk.Button(
        button_frame,
        text="Next Page",
        command=lambda: genesis.next_page(),
        font=("Helvetica", 12, "bold"),
        bg="#8B4513",
        fg="white",
        width=15,
    )
    btn_next_page.pack(side=tk.LEFT, padx=10)

    btn_prev_verse = tk.Button(
        button_frame,
        text="Previous Verse",
        command=lambda: genesis.prev_verse(),
        font=("Helvetica", 12, "bold"),
        bg="#D4A017",
        fg="black",
        width=15,
    )
    btn_prev_verse.pack(side=tk.LEFT, padx=10)

    btn_next_verse = tk.Button(
        button_frame,
        text="Next Verse",
        command=lambda: genesis.next_verse(),
        font=("Helvetica", 12, "bold"),
        bg="#D4A017",
        fg="black",
        width=15,
    )
    btn_next_verse.pack(side=tk.LEFT, padx=10)

    search_frame = tk.Frame(window, bg="#f5f5dc")
    search_frame.pack(side=tk.TOP, pady=10)

    search_label = tk.Label(
        search_frame, text="Search Verse:", font=("Helvetica", 12), bg="#f5f5dc"
    )
    search_label.pack(side=tk.LEFT, padx=5)

    verse_combobox = ttk.Combobox(search_frame, font=("Helvetica", 12), width=15)
    verse_combobox.pack(side=tk.LEFT, padx=5)

    btn_find = tk.Button(
        search_frame,
        text="Find",
        command=lambda: genesis.find_verse(verse_combobox.get()),
        font=("Helvetica", 12, "bold"),
        bg="#228B22",
        fg="white",
        width=10,
    )
    btn_find.pack(side=tk.LEFT, padx=5)

    btn_exit = tk.Button(
        button_frame,
        text="Exit",
        command=lambda: exit(window),
        font=("Helvetica", 12, "bold"),
        bg="#B22222",
        fg="white",
        width=15,
    )
    btn_exit.pack(side=tk.LEFT, padx=10)

    genesis = Genesis(text_widget)

    for verse, reference in verses:
        genesis.add_verse(verse, reference)

    genesis.turn_page()
    genesis.highlighted_verse = genesis.head
    genesis.display_page()

    verse_combobox["values"] = [reference for _, reference in verses]
    window.mainloop()

if __name__ == "__main__":
    openning()
    main()
