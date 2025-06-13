import tkinter as tk
def dashboadr():
    window = tk.Tk()
    window.geometry("1100x800")
    window.title("MoneyManager")
    window.configure(bg="#B8B8B8")

    img = tk.PhotoImage(file="logo.png")
    window.iconphoto(True, img)
    
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    mainTitle = tk.Label(window, text="Dashboard",anchor='center',font=("Helvetica", 28, "bold"), bg="#B8B8B8")
    mainTitle.grid(row=0, column=0, columnspan=2, pady=(20))

    window.mainloop()

# dashboadr()