import tkinter as tk
from tkinter import messagebox
import json

from dashboard import dashboadr
def login():
    window = tk.Tk()
    window.geometry("350x400")
    window.title("MoneyManager")
    window.configure(bg="#B8B8B8")

    img = tk.PhotoImage(file="logo.png")
    window.iconphoto(True, img)
 
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
 
    mainTitle = tk.Label(window, text="Money Manager", font=("Helvetica", 28, "bold"), bg="#B8B8B8" ,justify='center')
    mainTitle.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    subTitle = tk.Label(window, text="Login", font=("Helvetica", 18), bg="#B8B8B8", justify='center')
    subTitle.grid(row=1, column=0, columnspan=2, pady=(0, 20))
   
    user = tk.Label(window, text="User Name:", font=("Helvetica", 12, "bold"), bg="#B8B8B8")
    user.grid(row=2, column=0, sticky="e", pady=10)

    userName = tk.Entry(window, width=30)
    userName.grid(row=2, column=1, padx=10, pady=10)
  
    password = tk.Label(window, text="Password:", font=("Helvetica", 12, "bold"), bg="#B8B8B8")
    password.grid(row=3, column=0, sticky="e", padx=10, pady=10)

    passWord = tk.Entry(window, width=30, show="*")
    passWord.grid(row=3, column=1, padx=10, pady=10)

    #Handalin Login
    def check_login():

        # user_name = "admin"
        # pass_word = "admin"

        def get_login_info():
            with open("user_data.json", "r") as file:
                data = json.load(file)
                return data.get("username"), data.get("password")
                        
        user = userName.get()
        pasword = passWord.get()

        user_name, pass_word = get_login_info()

        if user_name == user and pasword == pass_word:
            window.destroy()
            dashboadr()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password please try again")

    loginBtn = tk.Button(window, text="Login", font=("Helvetica", 12), width=15, bg="#4CA3AF", fg="white" ,justify='center', command=check_login)
    loginBtn.grid(row=4, column=0, columnspan=2, pady=20)

    # Register Prompt
    #for Registering the user.
    def reg_user():
        # messagebox.showinfo("Sucess", "Party")
        window.destroy()
        reg_win = tk.Tk()
        reg_win.geometry("500x500")
        img = tk.PhotoImage(file="logo.png")
        reg_win.iconphoto(True, img)
        reg_win.title("MoneyManager")
        reg_win.configure(bg="#B8B8B8")
    
    #config of window rto make it full width
        reg_win.grid_columnconfigure(0, weight=1)
        reg_win.grid_columnconfigure(1, weight=1)

        mainTitle = tk.Label(reg_win, text="Money Manager", font=("Helvetica", 28, "bold"), bg="#B8B8B8" ,justify='center')
        mainTitle.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        subTitle = tk.Label(reg_win, text="SignUP", font=("Helvetica", 18), bg="#B8B8B8", justify='center')
        subTitle.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        fullName = tk.Label(reg_win, text="Full Name:", font=("Helvetica", 12, "bold"), bg="#B8B8B8")
        fullName.grid(row=2, column=0, sticky="e", pady=10)
        Fullname = tk.Entry(reg_win, width=30)
        Fullname.grid(row=2, column=1, padx=10, pady=10)


        email = tk.Label(reg_win, text="email:", font=("Helvetica", 12, "bold"), bg="#B8B8B8")
        email.grid(row=3, column=0, sticky="e", pady=10)
        email = tk.Entry(reg_win, width=30)
        email.grid(row=3, column=1, padx=10, pady=10)

        password = tk.Label(reg_win, text="Password:", font=("Helvetica", 12, "bold"), bg="#B8B8B8")
        password.grid(row=4, column=0, sticky="e", pady=10)
        password = tk.Entry(reg_win, width=30)
        password.grid(row=4, column=1, padx=10, pady=10)

        # To handle signups 
        def handle_signups():
            reg_win.destroy()
            login()

        signUp = tk.Button(reg_win, text="Sign up", font=("Helvetica", 12), width=15, bg="#4CA3AF", fg="white" ,justify='center', command=handle_signups)
        signUp.grid(row=5, column=0, columnspan=2, pady=20)
        reg_win.mainloop()       

    # Regestration button of login page
    register = tk.Label(window, text="Don't have an account? Register", fg="blue", bg="#B8B8B8", cursor="hand2")
    register.grid(row=5, column=0, columnspan=2, pady=10)
    register.bind("<Button-1>", lambda e: reg_user())
       
    window.mainloop()

# login()