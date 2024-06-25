import os
import tkinter as tk
from tkinter import messagebox
import phonebook

def get_details():
    global server_username,server_password,server_username_var,server_password_var
    server_username = server_username_var.get()
    server_password = server_password_var.get()

def login():
    global db,my_cursor,server_username,server_password
    get_details()
    # server name is always "localhost" for MySQL
    if server_username==os.getenv('MYSQL_USER') and server_password==os.getenv('MYSQL_PASSWORD'):
        root.destroy()
        phonebook.Phonebook(server_username,server_password)
    else:
        messagebox.showerror("Wrong login details","Please enter correct username and password!")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x220")
    root.title("Phonebook - Login")
    root.config(bg="#1289A7")
    app_icon_image = tk.PhotoImage(file="assets/images/phone-book.png")
    db = None
    my_cursor = None
    server_username_var = tk.StringVar()
    server_password_var = tk.StringVar()
    server_username = server_password = ""
    main_frame = tk.Frame(root,background="#1289A7")
    main_frame.pack(pady=10)
    # Login UI
    tk.Label(main_frame, text="Enter server user id:",font=("Arial",15),bg="#1289A7",fg="#000000").pack(pady=5)
    entry_server_username = tk.Entry(main_frame, textvariable=server_username_var,font=("Arial",15))
    entry_server_username.pack(pady=5)
    tk.Label(main_frame, text="Enter server password:",font=("Arial",15),bg="#1289A7",fg="#000000").pack(pady=5)
    entry_server_password = tk.Entry(main_frame, textvariable=server_password_var,font=("Arial",15),show="*")
    entry_server_password.pack(pady=3)
    # Button
    login_btn = tk.Button(root, text="Login", command=login,font=("Arial",15),bg="#000000",fg="#FFFFFF",activebackground="#000000",activeforeground="#FFFFFF")
    login_btn.pack()
    root.iconphoto(True,app_icon_image)
    root.mainloop()