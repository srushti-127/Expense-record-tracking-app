import datetime as dt
from expense_db import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter import Tk, PhotoImage
import tkinter as tk

#Create object for database
data = Database(db = 'expense_database.db')

#Create global variables
count = 0
selected_rowid = 0

def save_record():
    global data
    data.insert_record(item_name = item_name.get(),
                        item_price = item_amt.get(),
                        purchase_date = transaction_date.get())
    
def set_date():
    date = dt.datetime.now()            # Fetches the current date & time
    dropvar.set(f'{date:%d %B %Y}')

def clear_entries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    fetch_data = data.fetch_record('SELECT rowid, * FROM expense_record')
    global count
    for rec in fetch_data:
        tv.insert(parent = '', index = '0', iid = count,
                    values = (rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refresh_data)

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dropvar.set(str(d))

    except Exception as ep:
        pass

def update_record():
    global selected_rowid
    selected = tv.focus()

    # Upadted or not
    try:
        data.update_record(namevar.get(), amtvar.get(), dropvar.get(), selected_rowid)
        tv.item(selected, text = "", values = (namevar.get(), amtvar.get(), dropvar.get()))
    except Exception as ep:
        messagebox.showerror("Error", ep)

    # Clear entry boxes
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refresh_data)



def total_balance():
    fetched_data = data.fetch_record(query = 'SELECT SUM(item_price) FROM expense_record')
    for fetch_data in fetched_data:
        for data in fetch_data:
            messagebox.showinfo("Current Balance: ", f"Total Expense: ' {data} \nBalance Remaining: {50000 - data}")


def refresh_data():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()

def delete_row():
    global selected_rowid
    data.remove_record(selected_rowid)
    refresh_data()



                # GUI
    
#Creating tkinter object
ws = tk.Tk()
ws.title('Expen$e Tracker')

fonts = ('Times new roman', 10)
namevar = StringVar()
amtvar = IntVar()
dropvar = StringVar()

# f1 = recieving input part in the interface(bottom half)
# f2 = used to display the data stored trough interface(upper half)

#Frame widget
f2 = Frame(ws)
f2.pack()

f1 = Frame(
    ws,
    padx = 10,
    pady = 10,
)

f1.pack(expand = True, fill = BOTH)

# Label widget
Label(f1, text = 'Enter Item Name', font = fonts).grid(row = 0, column = 0, sticky = W)
Label(f1, text = 'Enter Item Price', font = fonts).grid(row = 1, column = 0, sticky = W)
Label(f1, text = 'Enter Purchase Date',font = fonts).grid(row = 2, column = 0, sticky = W)


# Entry widgers
item_name = Entry(f1, font = fonts, textvariable = namevar)
item_amt = Entry(f1, font = fonts, textvariable = amtvar)
transaction_date = Entry(f1, font = fonts, textvariable = dropvar)

# Entry grid placement
item_name.grid(row = 0, column = 1, sticky = EW, padx = (10, 0))
item_amt.grid(row = 1, column = 1, sticky = EW, padx = (10, 0))
transaction_date.grid(row = 2, column = 1, sticky = EW, padx = (10, 0))


# Action buttons
cur_date = Button(
    f1,
    text = 'Current Date',
    font = fonts,
    bg = '#04C4D9',
    command = set_date,             # Calling set_date function
    width = 15
)


submit_btn = Button(
    f1,
    text = 'Save Record',
    font = fonts,
    command = save_record,      # Calling save_record function
    bg = '#42602D',
    fg = 'white'
)

clr_btn = Button(
    f1,
    text = 'Clear Entry',
    font = fonts,
    command = clear_entries,      # Calling clear_entries function
    bg = '#D9B036',
    fg = 'white'
)

quit_btn = Button(
    f1,
    text = 'Exit',
    font = fonts,
    command = lambda:ws.destroy(),      # Calling destroy function of tkinter in ws object using lambda
    bg = '#D33532',
    fg = 'white'
)

total_bal = Button(
    f1,
    text = 'Total Balance',
    font = fonts,
    bg = '#486966',
    command = total_balance,      # Calling total_balance function
)

update_btn = Button(
    f1,
    text = 'Update',
    bg = '#C2BB00',
    command = update_record,      # Calling update_record function
    font = fonts
)

del_btn = Button(
    f1,
    text = 'Delete',
    bg = '#BD2A2E',
    command = delete_row,      # Calling delete_row function
    font = fonts
)

# placing grids
submit_btn.grid(row = 0, column = 2, sticky = EW, padx = (10, 0))
total_bal.grid(row = 0, column = 3, sticky = EW, padx = (10, 0))

clr_btn.grid(row = 1, column = 2, sticky = EW, padx = (10, 0))
update_btn.grid(row = 1, column = 3, sticky = EW, padx = (10, 0))

quit_btn.grid(row = 2, column = 2, sticky = EW, padx = (10, 0))
del_btn.grid(row = 2, column = 3, sticky = EW, padx = (10, 0))

cur_date.grid(row = 3, column = 1, sticky = EW, padx = (10, 0))


# Tree view
tv = ttk.Treeview(f2, columns = (1, 2, 3, 4), show = 'headings', height = 8)
tv.pack(side = 'left')

# Adding the headings to treeview
tv.column(1, anchor = CENTER, stretch=NO, width=70)
tv.heading(1, text = 'Serial no')

tv.column(2, anchor = CENTER)
tv.heading(2, text = 'Item Name')

tv.column(3, anchor = CENTER)
tv.heading(3, text = 'Item Price')

tv.column(4, anchor = CENTER)
tv.heading(4, text = 'Purchase Date')

# Blinding Treeview
tv.bind("ButtonRelease - 1>", select_record)

# Style for Treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient = 'vertical')
scrollbar.configure(command = tv.yview)
scrollbar.pack(side = 'right', fill = 'y')
tv.config(yscrollcommand = scrollbar.set)

# calling functio
fetch_records()

#infinite MAIN loop
ws.mainloop()