import json
import string
from tkinter import *
import random
from tkinter import messagebox
import pyperclip

chars = string.printable
chars = chars.replace("", "").replace(" ", "")
print(chars)
c_win_closed = False

pass_l = 0


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def pass_settings():
    def window_kill():
        new_w.destroy()
        passgen()
        gen_pass_button.config(state=ACTIVE, bg="white")

    def callback(_):
        global pass_l
        pass_ll = int(spinbox.get())
        pass_l = pass_ll

    new_w = Toplevel(padx=10, pady=10)
    new_w.title("Set password length")
    label = Label(new_w, text="Set the length of the password, max 25 chars")
    label.grid(column=0, row=0, sticky=EW, pady=2, padx=2)
    spinbox = Scale(new_w, from_=1, to=25, orient=HORIZONTAL, command=callback)
    spinbox.grid(column=0, row=1, sticky=EW, pady=2, padx=2)
    new_w_button = Button(new_w, text="Ok", command=window_kill, pady=2, padx=2)
    new_w_button.grid(column=0, row=2, sticky=EW)
    gen_pass_button.config(state=DISABLED)
    new_w.protocol("WM_DELETE_WINDOW", window_kill)


def passgen():
    password_entry.delete(0, END)
    rand_pass = ''.join(random.choice(chars) for _ in range(pass_l))
    password_entry.insert(0, rand_pass)
    pyperclip.copy(rand_pass)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def saver():
    new_data = {
        website_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get(),
        }
    }

    # checking if there are empty fields
    if website_entry.get() == "" or password_entry.get() == "":
        messagebox.showerror("Empty fields", message="You have left empty fields, please correct")
    else:
        # confirmation if all good
        confirm = messagebox.askyesno(message=f"Are those information correct? \nWebsite: {website_entry.get()}"
                                              f"\nEmail: {email_entry.get()} \nPassword: {password_entry.get()} ")
        if confirm:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
                    data.update(new_data)

                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            clear()


def clear():
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    email_entry.delete(0, END)
    website_entry.focus()
    email_entry.insert(string="a1.andrzej@gmail.com", index=0)


def search():
    try:
        with open("data.json", "r") as data:
            data = json.load(data)
            messagebox.showinfo(message=f"Here is the password: {data[website_entry.get()]['password']}"
                                        f"\nYour email: {data[website_entry.get()]['email']}"
                                        f"\nFor the site: {website_entry.get()}\nPassword was copied to your clipboard")
            pyperclip.copy(data[website_entry.get()]['password'])

    except FileNotFoundError:
        messagebox.showerror(message=f"There is nothing saved yet, or file was removed. Save something first!")
    except KeyError:
        messagebox.showerror(message=f"Provided site does not exist!\n {website_entry.get()}")




# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
logo = PhotoImage(file="logo.png")
window.iconphoto(False, logo)
window.config(bg="white", pady=20, padx=20)
canvas = Canvas(width=200, height=200, bg="white", highlightbackground="white")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# website label
web_label = Label(text="Website:", bg="White")
web_label.grid(column=0, row=1)

# email label
email_label = Label(text="Email/Username:", bg="White")
email_label.grid(column=0, row=2)

# password label
password_label = Label(text="Password:", bg="White")
password_label.grid(column=0, row=3)

# website entry
website_entry = Entry(width=35, bg="White")
website_entry.grid(row=1, column=1, sticky=EW, padx=2, pady=2)
website_entry.focus()
# email entry
email_entry = Entry(width=35, bg="white")
email_entry.grid(row=2, column=1, sticky=EW, padx=2, pady=2,columnspan=2)
email_entry.insert(string="a1.andrzej@gmail.com", index=0)

# password entry
password_entry = Entry(width=21, bg="White")
password_entry.grid(column=1, row=3, sticky=EW, padx=2, pady=2)

# add button
add_button = Button(text="Add", width=36, bg="White", command=saver)
add_button.grid(column=1, row=4, columnspan=2, sticky=EW, padx=2, pady=2)

# Generate Password button
gen_pass_button = Button(width=15, text="Generate Password", bg="White", command=pass_settings)
gen_pass_button.grid(column=2, row=3, sticky=EW, padx=2, pady=2)

# Search button
search_button = Button(width=15, text="Search", bg="white", command=search)
search_button.grid(row=1, column=2, sticky=EW, pady=2, padx=2)

window.mainloop()
