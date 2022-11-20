import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import algo as algo


# root window
root = tk.Tk()
root.geometry("350x350")
root.resizable(False, False)
root.title("Interactive Brokers Value Averaging")

# account type
def show_account_type():
    # showinfo(title="Result", message=account_type.get())
    return account_type.get()


account_type = tk.StringVar()
intervals = (
    ("Trading Account", 7496),
    ("Paper Account", 7497),
)

# label
label = ttk.Label(text="Select account type:")
label.pack(fill="x", padx=5, pady=5)

# radio buttons
for interval in intervals:
    r = ttk.Radiobutton(
        root, text=interval[0], value=interval[1], variable=account_type
    )
    r.pack(fill="x", padx=25, pady=5)

account_type.set(7497)

# recurring interval
def show_recurring_interval():
    # showinfo(title="Result", message=recurring_interval.get())
    return recurring_interval.get()


recurring_interval = tk.StringVar()
intervals = (
    ("Weekly", 7),
    ("Fortnightly", 14),
    ("Monthly", 28),
)

# label
label = ttk.Label(text="Select recurring interval:")
label.pack(fill="x", padx=5, pady=5)

# radio buttons
for interval in intervals:
    r = ttk.Radiobutton(
        root, text=interval[0], value=interval[1], variable=recurring_interval
    )
    r.pack(fill="x", padx=25, pady=5)

recurring_interval.set(28)

# minimum amount to invest per asset
def show_minimum_amount():
    # showinfo(title="Minimum Amount", message=spin_box.get())
    return spin_box1.get()


minimum_amount = tk.StringVar(value=700)
spin_box1 = ttk.Spinbox(
    root,
    from_=0,
    to=10000,
    increment=50,
    justify="left",
    textvariable=minimum_amount,
    wrap=True,
)

# label
label = ttk.Label(text="Minimum amount to invest per asset:")
label.pack(fill="x", padx=5, pady=5)

spin_box1.pack(fill="x", padx=125, pady=5)

# amount to invest
def show_recurring_amount():
    # showinfo(title="Recurring Amount", message=spin_box.get())
    return spin_box2.get()


recurring_amount = tk.StringVar(value=3250)
spin_box2 = ttk.Spinbox(
    root,
    from_=1000,
    to=10000,
    increment=50,
    justify="left",
    textvariable=recurring_amount,
    wrap=True,
)

# label
label = ttk.Label(text="Amount to invest:")
label.pack(fill="x", padx=5, pady=5)

spin_box2.pack(fill="x", padx=125, pady=5)


from tkinter.messagebox import askokcancel, showinfo, WARNING


def confirm():
    msg = f"Account Type: {show_account_type()}\nRecurring Interval: {show_recurring_interval()}\nMinimum Amount: {show_minimum_amount()}\nRecurring Amount: {show_recurring_amount()}"
    answer = askokcancel(title="Confirmation", message=msg, icon=WARNING)

    if answer:
        showinfo(title="Investing", message="Please don't close IBKR or this app")
        algo.invest(
            int(show_account_type()),
            int(show_recurring_interval()),
            int(show_minimum_amount()),
            int(show_recurring_amount()),
        )


# button
button = ttk.Button(root, text="Invest", command=confirm)
button.pack(fill="x", padx=125, pady=5)

root.mainloop()
