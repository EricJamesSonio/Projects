import tkinter as tk


def openning():
    window = tk.Tk()
    window.title("Genesis Chapter 1")
    window.attributes("-fullscreen", True)
    window.config(bg="#F5F5DC")
    canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
    canvas.pack(fill="both", expand=True)
    canvas.create_rectangle(0,0,window.winfo_screenwidth(),window.winfo_screenheight(),fill="#F5F5DC",outline="#F5F5DC",)
    label = tk.Label(
        window,
        text="Genesis Chapter 1",
        font=("Garamond", 50, "bold"),
        fg="#4B2F15",
        bg="#F5F5DC",
        pady=30,
    )
    label.place(relx=0.5, rely=0.4, anchor="center")
    start_button = tk.Button(
        window,
        text="Start",
        font=("Times New Roman", 18, "bold"),
        fg="white",
        bg="#8B4513",
        relief="raised",
        width=20,
        height=3,
        activebackground="#5C4033",
        activeforeground="white",
        command=window.destroy,
    )
    start_button.place(relx=0.5, rely=0.6, anchor="center")
    button_shadow = tk.Button(
        window,
        text="Start",
        font=("Times New Roman", 18, "bold"),
        fg="white",
        bg="#8B4513",
        relief="raised",
        width=20,
        height=3,
        activebackground="#5C4033",
        activeforeground="white",
        command=window.destroy,
    )
    button_shadow.place(relx=0.5, rely=0.6, anchor="center", x=3, y=3)
    window.mainloop()

if __name__ == "__main__":
    openning()
