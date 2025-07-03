import tkinter as tk
import json

def dashboadr():
    window = tk.Tk()
    window.title("Money Manager")
    window.configure(bg="#f5f7fb")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

    img = tk.PhotoImage(file="logo.png")
    window.iconphoto(True, img)

    window.mainloop()
# dashboadr()