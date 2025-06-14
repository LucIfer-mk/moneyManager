import tkinter as tk
import json

def dashboadr():
    window = tk.Tk()
    window.geometry("1100x800")
    window.title("MoneyManager")
    window.configure(bg="#B8B8B8")

    img = tk.PhotoImage(file="logo.png")
    window.iconphoto(True, img)
    
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    def user_info():
            with open("user_data.json", "r") as file:
                data = json.load(file)
                return data.get("username")

    mainTitle = tk.Label(window, text="Dashboard", anchor="w", font=("Helvetica", 28, "bold"), bg="#B8B8B8")
    mainTitle.grid(row=0, column=0, sticky="w", padx=40, pady=(20, 0))

    addTransction = tk.Button(window, text="+ Add Transaction", font=("Helvetica", 12), width=15, bg="#3235F0", fg="white" ,cursor="hand2")
    addTransction.grid(row=0, column=1, sticky="e", padx=40, pady=(20, 0))

    welcomeMessage = tk.Label(window, text=f"Welcome {user_info()}! Here's your financial overview", anchor="w", font=("Helvetica", 10), bg="#B8B8B8")
    welcomeMessage.grid(row=1, column=0, columnspan=2, sticky="w", padx=40)


    # total balance, income and expense card
    #######################3Dbug Box#####################


     # container frame for the 3 cards
    cardContainer = tk.Frame(window, bg="#B8B8B8")
    cardContainer.grid(row=2, column=0, columnspan=2, pady=30)

    def create_card(parent, title, amount, change, change_color, icon_text, icon_bg):
        card = tk.Frame(parent, bg="white", width=300, height=120)
        card.pack(side="left", padx=20)

        # Title
        tk.Label(card, text=title, font=("Helvetica", 10), bg="white", fg="gray").place(x=10, y=10)

        # Amount
        tk.Label(card, text=amount, font=("Helvetica", 18, "bold"), bg="white", fg="black").place(x=10, y=35)

        # Change
        tk.Label(card, text=change, font=("Helvetica", 10), bg="white", fg=change_color).place(x=10, y=75)

        # Icon
        icon = tk.Label(card, text=icon_text, bg=icon_bg, fg="white", font=("Helvetica", 12, "bold"), width=2, height=1)
        icon.place(x=250, y=15)

        return card

    # Create the 3 cards
    def get_userAccount():
         with open("user_data.json", "r") as file:
              data =json.load(file)
              return data.get("income")
            
    
    
    create_card(cardContainer, "Total Balance", "$12,580.35", "↗ +2.5% from last month", "green", "$", "#4A7BF7")
    create_card(cardContainer, "Income", "$4,850.00", "↗ +1.2% from last month", "green", "↑", "#00771E")
    create_card(cardContainer, "Expenses", "$2,365.75", "↘ +3.8% from last month", "red", "↓", "#AF0000")


    ##################################################
    window.mainloop()

dashboadr()