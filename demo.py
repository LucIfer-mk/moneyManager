import tkinter as tk
import json
from tkinter import ttk
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

def dashboadr():
    window = tk.Tk()
    window.title("Money Manager")
    window.configure(bg="#f5f7fb")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

    img = tk.PhotoImage(file="logo.png")
    window.iconphoto(True, img)
 
    ##### Read File ###
    def get_login_data():
        with open("user_data.json", "r") as file:
            data = json.load(file)
            return data.get("username")

    # Styling
    card_bg = "#ffffff"
    highlight_green = "#14c57c"
    highlight_red = "#e34d4d"
    text_dark = "#343a40"
    purple = "#6a5acd"

    
 
    # Title section
    title = tk.Label(window, text="Financial Dashboard", font=("Arial", 24, "bold"),
                      bg="#f5f7fb", anchor="w")
    title.place(x=30, y=20)

    subtitle = tk.Label(window, text=f"Welcome back, {get_login_data()} Here's your financial overview.", font=("Arial", 12), bg="#f5f7fb", anchor="w")
    subtitle.place(x=30, y=60)

    # Read statement.csv for summary calculations
    statement = []
    total_income = 0.0
    total_expense = 0.0
    with open("statement.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            statement.append(row)
            amount = float(row["Amount"])
            if row["Type"].lower() == "income":
                total_income += amount
            elif row["Type"].lower() == "expense":
                total_expense += amount
    total_balance = total_income + total_expense  # expenses are negative

    # Summary cards
    def create_summary_card(parent, x, y, title, amount, change, color):
        frame = tk.Frame(parent, bg=card_bg, width=250, height=100, highlightbackground="#ccc", highlightthickness=1)
        frame.place(x=x, y=y)

        tk.Label(frame, text=title, font=("Arial", 10), bg=card_bg).place(x=15, y=10)
        tk.Label(frame, text=amount, font=("Arial", 18, "bold"), fg=color, bg=card_bg).place(x=15, y=35)
        tk.Label(frame, text=change, font=("Arial", 10), fg=color, bg=card_bg).place(x=15, y=70)

    create_summary_card(window, 30, 110, "Total Balance", f"${total_balance:,.2f}", "", highlight_green if total_balance >= 0 else highlight_red)
    create_summary_card(window, 310, 110, "Income", f"${total_income:,.2f}", "", highlight_green)
    create_summary_card(window, 590, 110, "Expenses", f"${-total_expense:,.2f}", "", highlight_red)

    # Spending Overview with interactive toggle buttons and dynamic graph
    overview_frame = tk.Frame(window, bg=card_bg, width=950, height=300, highlightbackground="#ccc", highlightthickness=1)
    overview_frame.place(x=30, y=230)
    tk.Label(overview_frame, text="Spending Overview", font=("Arial", 14, "bold"), bg=card_bg).place(x=15, y=10)

    # Variable to track selected view
    overview_view = tk.StringVar(value='month')
    graph_canvas = [None]  # mutable holder for the canvas widget

    def draw_overview_graph():
        # Remove previous graph if exists
        if graph_canvas[0] is not None:
            graph_canvas[0].get_tk_widget().destroy()
        import datetime, calendar
        now = datetime.datetime.now()
        year = now.year
        try:
            if overview_view.get() == 'month':
                months = [datetime.date(year, m, 1).strftime('%b') for m in range(1, 13)]
                income_by_month = [0.0] * 12
                expense_by_month = [0.0] * 12
                for row in statement:
                    try:
                        date = datetime.datetime.strptime(row["Date"], "%Y-%m-%d")
                        if date.year == year:
                            month_idx = date.month - 1
                            amount = float(row["Amount"])
                            if row["Type"].lower() == "income":
                                income_by_month[month_idx] += amount
                            elif row["Type"].lower() == "expense":
                                expense_by_month[month_idx] += abs(amount)
                    except Exception:
                        continue
                x = months
                y_income = income_by_month
                y_expense = expense_by_month
                xlabel = ""
            elif overview_view.get() == 'week':
                today = now
                start_of_week = today - datetime.timedelta(days=today.weekday())
                week_dates = [(start_of_week + datetime.timedelta(days=i)).date() for i in range(7)]
                income_by_date = {d.strftime('%a'): 0.0 for d in week_dates}
                expense_by_date = {d.strftime('%a'): 0.0 for d in week_dates}
                for row in statement:
                    try:
                        date = datetime.datetime.strptime(row["Date"], "%Y-%m-%d").date()
                        if week_dates[0] <= date <= week_dates[-1]:
                            amount = float(row["Amount"])
                            day = date.strftime('%a')
                            if row["Type"].lower() == "income":
                                income_by_date[day] += amount
                            elif row["Type"].lower() == "expense":
                                expense_by_date[day] += abs(amount)
                    except Exception:
                        continue
                x = [d.strftime('%a') for d in week_dates]
                y_income = [income_by_date[d] for d in x]
                y_expense = [expense_by_date[d] for d in x]
                xlabel = ""
            elif overview_view.get() == 'year':
                years = [str(year - i) for i in reversed(range(5))]
                income_by_year = [0.0] * 5
                expense_by_year = [0.0] * 5
                for row in statement:
                    try:
                        date = datetime.datetime.strptime(row["Date"], "%Y-%m-%d")
                        y = str(date.year)
                        if y in years:
                            idx = years.index(y)
                            amount = float(row["Amount"])
                            if row["Type"].lower() == "income":
                                income_by_year[idx] += amount
                            elif row["Type"].lower() == "expense":
                                expense_by_year[idx] += abs(amount)
                    except Exception:
                        continue
                x = years
                y_income = income_by_year
                y_expense = expense_by_year
                xlabel = ""
            fig, ax = plt.subplots(figsize=(7, 2.5), dpi=100)
            ax.plot(x, y_income, color="#14c57c", marker="o", label="Income", linewidth=2)
            ax.plot(x, y_expense, color="#e34d4d", marker="o", label="Expenses", linewidth=2)
            ax.fill_between(x, y_income, color="#14c57c", alpha=0.08)
            ax.fill_between(x, y_expense, color="#e34d4d", alpha=0.08)
            ax.set_ylim(bottom=0)
            ax.set_title("")
            ax.set_xlabel(xlabel)
            ax.set_ylabel("")
            ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, frameon=False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_color('#ccc')
            ax.tick_params(axis='y', colors='#888')
            ax.tick_params(axis='x', colors='#888')
            fig.tight_layout(rect=[0, 0.05, 1, 1])
            canvas = FigureCanvasTkAgg(fig, master=overview_frame)
            canvas.draw()
            canvas.get_tk_widget().place(x=10, y=45)
            graph_canvas[0] = canvas
        except Exception as e:
            tk.Label(overview_frame, text=f"[Chart Error: {e}]", font=("Arial", 12), bg=card_bg, fg="#888").place(x=300, y=130)

    def set_overview_view(view):
        overview_view.set(view)
        # Update button styles
        btn_week.config(bg="#e6e6fa" if view=="week" else "#f5f7fb")
        btn_month.config(bg="#e6e6fa" if view=="month" else "#f5f7fb")
        btn_year.config(bg="#e6e6fa" if view=="year" else "#f5f7fb")
        draw_overview_graph()

    btn_week = tk.Button(overview_frame, text="Week", font=("Arial", 10, "bold"), bg="#f5f7fb", fg="#6a5acd", relief="ridge", bd=1, width=7, command=lambda: set_overview_view('week'))
    btn_week.place(x=600, y=10)
    btn_month = tk.Button(overview_frame, text="Month", font=("Arial", 10, "bold"), bg="#e6e6fa", fg="#6a5acd", relief="solid", bd=1, width=7, command=lambda: set_overview_view('month'))
    btn_month.place(x=670, y=10)
    btn_year = tk.Button(overview_frame, text="Year", font=("Arial", 10, "bold"), bg="#f5f7fb", fg="#6a5acd", relief="ridge", bd=1, width=7, command=lambda: set_overview_view('year'))
    btn_year.place(x=740, y=10)

    draw_overview_graph()

    # Recent Transactions (from statement.csv)
    transactions_frame = tk.Frame(window, bg=card_bg, width=750, height=250, highlightbackground="#ccc", highlightthickness=1)
    transactions_frame.place(x=30, y=550)
    tk.Label(transactions_frame, text="Recent Transactions", font=("Arial", 14, "bold"), bg=card_bg).place(x=15, y=10)

    # Create Treeview for table
    columns = ("Date", "Description", "Amount", "Type")
    tree = ttk.Treeview(transactions_frame, columns=columns, show="headings", height=7)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=170 if col!="Description" else 220)
    # Insert data
    for row in statement[-7:]:  # Show last 7 transactions
        tree.insert("", "end", values=(row["Date"], row["Description"], row["Amount"], row["Type"]))
    tree.place(x=15, y=45)

    # Budget Card with Progress Bar
    budget_frame = tk.Frame(window, bg=card_bg, width=500, height=300, highlightbackground="#ccc", highlightthickness=1)
    budget_frame.place(x=1100, y=230)
    tk.Label(budget_frame, text="Monthly Budget", font=("Arial", 14, "bold"), bg=card_bg).place(x=15, y=10)

    # Calculate current month expenses
    now = datetime.datetime.now()
    current_month = now.strftime("%Y-%m")
    monthly_expense = 0.0
    for row in statement:
        if row["Type"].lower() == "expense" and row["Date"].startswith(current_month):
            monthly_expense += abs(float(row["Amount"]))
    monthly_budget = 2000.0  # You can change this value as needed
    percent_used = min(monthly_expense / monthly_budget, 1.0)

    # Progress bar
    from tkinter import ttk as tkttk
    progress = tkttk.Progressbar(budget_frame, orient="horizontal", length=320, mode="determinate")
    progress.place(x=25, y=100)
    progress["value"] = percent_used * 100

    tk.Label(budget_frame, text=f"${monthly_expense:,.2f} spent of ${monthly_budget:,.2f}", font=("Arial", 12), bg=card_bg).place(x=60, y=140)
    tk.Label(budget_frame, text=f"{percent_used*100:.1f}% used", font=("Arial", 11, "bold"), bg=card_bg, fg=highlight_red if percent_used > 0.8 else highlight_green).place(x=130, y=170)

    # --- Monthly Budget with per-category progress bars (top 4 for current month) ---
    # Aggregate expenses by category for the current month
    category_totals = {}
    for row in statement:
        if row["Type"].lower() == "expense" and row["Date"].startswith(current_month):
            category = row["Description"]
            category_totals[category] = category_totals.get(category, 0.0) + abs(float(row["Amount"]))
    # Get top 4 categories by spending
    top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:4]
    # Default budgets for top categories (or fallback to 300 if not set)
    default_budget = 300
    custom_budgets = {
        "Rent": 800,
        "Groceries": 400,
        "Transport": 150,
        "Dining": 200,
        "Health": 200,
        "Utilities": 150,
        "Entertainment": 200,
        "Fuel": 120,
        "Shopping": 300,
        "Other": 100
    }
    category_budgets = {cat: custom_budgets.get(cat, default_budget) for cat, _ in top_categories}
    # Colors for categories
    category_colors = {
        "Rent": "#6a5acd",
        "Groceries": "#14c57c",
        "Transport": "#2196f3",
        "Dining": "#ffc107",
        "Health": "#8bc34a",
        "Utilities": "#00bcd4",
        "Entertainment": "#ff9800",
        "Fuel": "#9c27b0",
        "Shopping": "#f44336",
        "Other": "#607d8b"
    }
    y_offset = 40
    for cat, spent in top_categories:
        limit = category_budgets.get(cat, default_budget)
        percent = min(spent / limit, 1.0) if limit > 0 else 0
        over = spent > limit
        color = "#f44336" if over else category_colors.get(cat, "#14c57c")
        # Label
        label_text = f"{cat}"
        tk.Label(budget_frame, text=label_text, font=("Arial", 10, "bold"), bg=card_bg).place(x=15, y=y_offset)
        # Progress bar
        style_name = f"{cat}.Horizontal.TProgressbar"
        s = tkttk.Style()
        s.theme_use('default')
        s.configure(style_name, troughcolor=card_bg, background=color, thickness=12)
        bar = tkttk.Progressbar(budget_frame, style=style_name, orient="horizontal", length=320, mode="determinate")
        bar.place(x=120, y=y_offset+2)
        bar["value"] = min(spent / limit, 1.0) * 100 if limit > 0 else 0
        # Amount label
        amt_color = color if over else text_dark
        amt_text = f"${spent:,.0f} / ${limit:,.0f}"
        tk.Label(budget_frame, text=amt_text, font=("Arial", 10, "bold"), bg=card_bg, fg=amt_color).place(x=450, y=y_offset)
        y_offset += 32

    tk.Button(budget_frame, text="Adjust Budget", bg=purple, fg="white", font=("Arial", 11, "bold")).place(x=180, y=240)

    # Savings Goal Placeholder
    savings_frame = tk.Frame(window, bg=card_bg, width=370, height=180, highlightbackground="#ccc", highlightthickness=1)
    savings_frame.place(x=820, y=550)
    tk.Label(savings_frame, text="Savings Goal", font=("Arial", 14, "bold"), bg=card_bg).place(x=15, y=10)

    # Donut chart for savings progress
    try:
        # Example values (replace with your own logic if needed)
        saved = 500
        goal = 5000
        percent = saved / goal if goal > 0 else 0
        fig3, ax3 = plt.subplots(figsize=(1.2, 1.2), dpi=100)
        ax3.pie([percent, 1-percent], radius=1, colors=[highlight_green, '#eee'], startangle=90, counterclock=False, wedgeprops=dict(width=0.4, edgecolor='w'))
        ax3.text(0, 0, f"{int(percent*100)}%", ha='center', va='center', fontsize=12, fontweight='bold')
        ax3.set(aspect="equal")
        fig3.tight_layout()
        canvas3 = FigureCanvasTkAgg(fig3, master=savings_frame)
        canvas3.draw()
        canvas3.get_tk_widget().place(x=10, y=35)
    except Exception as e:
        tk.Label(savings_frame, text=f"[Donut Error: {e}]", font=("Arial", 10), bg=card_bg, fg="#888").place(x=10, y=60)

    # tk.Label(savings_frame, text="65% of goal", font=("Arial", 12, "bold"), bg=card_bg, fg=highlight_green).place(x=80, y=50)
    tk.Label(savings_frame, text=f"Vacation Fund\n{saved} saved of {goal} goal", font=("Arial", 10), bg=card_bg).place(x=180, y=45)
    tk.Button(savings_frame, text="Add to Savings", bg=purple, fg="white", font=("Arial", 11, "bold")).place(x=180, y=90)

    def add_income_popup():
        popup = tk.Toplevel(window)
        popup.title("Add Income")
        popup.geometry("350x200")
        popup.configure(bg="#f5f7fb")
        tk.Label(popup, text="Add Income", font=("Arial", 16, "bold"), bg="#f5f7fb").pack(pady=10)
        tk.Label(popup, text="Category:", bg="#f5f7fb").pack()
        income_categories = [
            "Salary", "Bonus", "Investment", "Gift", "Other"
        ]
        from tkinter import ttk as tkttk
        income_category_var = tk.StringVar()
        income_category_dropdown = tkttk.Combobox(popup, textvariable=income_category_var, values=income_categories, state="readonly")
        income_category_dropdown.pack()
        income_category_dropdown.set(income_categories[0])
        tk.Label(popup, text="Amount:", bg="#f5f7fb").pack()
        amt_entry = tk.Entry(popup)
        amt_entry.pack()
        def submit_income():
            import csv
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d")
            desc = income_category_var.get().strip()
            amt = amt_entry.get().strip()
            try:
                float_amt = float(amt)
            except:
                tk.Label(popup, text="Invalid amount!", fg="red", bg="#f5f7fb").pack()
                return
            with open("statement.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([date, desc, float_amt, "Income"])
            popup.destroy()
            window.destroy()
            dashboadr()  # reload dashboard
        tk.Button(popup, text="Submit", command=submit_income, bg="#14c57c", fg="white", font=("Arial", 11, "bold")).pack(pady=15)

    def add_expense_popup():
        popup = tk.Toplevel(window)
        popup.title("Add Expense")
        popup.geometry("350x200")
        popup.configure(bg="#f5f7fb")
        tk.Label(popup, text="Add Expense", font=("Arial", 16, "bold"), bg="#f5f7fb").pack(pady=10)
        tk.Label(popup, text="Category:", bg="#f5f7fb").pack()
        categories = [
            "Rent", "Groceries", "Transport", "Dining", "Health", "Utilities", "Entertainment", "Fuel", "Shopping", "Other"
        ]
        from tkinter import ttk as tkttk
        category_var = tk.StringVar()
        category_dropdown = tkttk.Combobox(popup, textvariable=category_var, values=categories, state="readonly")
        category_dropdown.pack()
        category_dropdown.set(categories[0])
        tk.Label(popup, text="Amount:", bg="#f5f7fb").pack()
        amt_entry = tk.Entry(popup)
        amt_entry.pack()
        def submit_expense():
            import csv
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d")
            category = category_var.get().strip()
            desc = category  # Only category as description
            amt = amt_entry.get().strip()
            try:
                float_amt = float(amt)
            except:
                tk.Label(popup, text="Invalid amount!", fg="red", bg="#f5f7fb").pack()
                return
            with open("statement.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([date, desc, -abs(float_amt), "Expense"])
            popup.destroy()
            window.destroy()
            dashboadr()  # reload dashboard
        tk.Button(popup, text="Submit", command=submit_expense, bg="#e34d4d", fg="white", font=("Arial", 11, "bold")).pack(pady=15)

    # Quick Actions
    quick_frame = tk.Frame(window, bg=card_bg, width=370, height=100, highlightbackground="#ccc", highlightthickness=1)
    quick_frame.place(x=820, y=700)
    tk.Label(quick_frame, text="Quick Actions", font=("Arial", 14, "bold"), bg=card_bg).place(x=15, y=10)
    tk.Button(quick_frame, text="Add Income", bg="#e0f7fa", font=("Arial", 10), command=add_income_popup).place(x=20, y=50)
    tk.Button(quick_frame, text="Add Expense", bg="#ffe0e0", font=("Arial", 10), command=add_expense_popup).place(x=130, y=50)
    tk.Button(quick_frame, text="Reports", bg="#e6f4ea", font=("Arial", 10)).place(x=240, y=50)

    # Run the app
    window.mainloop()
dashboadr()