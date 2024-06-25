import tkinter as tk
from tkinter import messagebox
import mysql.connector
class Phonebook:
    def __init__(self,server_username,server_password):
        self.root = tk.Tk()
        self.root.geometry("670x650")
        self.root.title("Phonebook")
        self.server_username = server_username
        self.server_password = server_password
        self.db = mysql.connector.connect(host="localhost",
                                     user=self.server_username,
                                     passwd=self.server_password)
        self.table_name = "my_contacts"
        self.cursor_object = self.db.cursor()
        # GUI
        self.app_icon_image = tk.PhotoImage(file="assets/images/phone-book.png").subsample(3,3)
        self.add_contact_image = tk.PhotoImage(file="assets/images/add-contact-64-icon.png").subsample(3,3)
        self.search_contact_image = tk.PhotoImage(file="assets/images/search-icon.png").subsample(3,3)
        self.back_icon_image = tk.PhotoImage(file="assets/images/back-icon.png").subsample(3,3)
        tk.Label(self.root,text="Phonebook Contacts",font=("Arial",20),image=self.app_icon_image,compound=tk.LEFT).pack()
        self.side_panel = tk.Frame(self.root,padx=10)
        self.side_panel.pack(side=tk.LEFT)
        self.all_contacts = tk.Button(self.side_panel,text="All",width=10,font=("Times New Roman",18),bg="turquoise",command=self.show_all_contacts,activebackground="turquoise")
        self.all_contacts.grid(row=0,column=0,pady=15)
        self.family_contacts_button = tk.Button(self.side_panel,text="Family",width=10,font=("Arial",18),bg="#eb2f06",fg="#ffffff",command=self.show_family_contacts,activebackground="#eb2f06")
        self.family_contacts_button.grid(row=1,column=0,pady=15)
        self.friends_contacts_button = tk.Button(self.side_panel,width=10,text="Friends",font=("Arial",18),bg="green",fg="white",command=self.show_friends_contacts,activebackground="green")
        self.friends_contacts_button.grid(row=2,column=0,pady=15)
        self.work_contacts_button = tk.Button(self.side_panel,width=10,text="Work",font=("Arial",18),bg="#fa983a",command=self.show_work_contacts,activebackground="#fa983a")
        self.work_contacts_button.grid(row=3,column=0,pady=15)
        self.neighbours_contacts_btn = tk.Button(self.side_panel,width=10,text="Neighbours",font=("Arial",18),bg="#D980FA",command=self.show_neighbours_contacts,activebackground="#D980FA")
        self.neighbours_contacts_btn.grid(row=4,column=0,pady=15)
        self.medical_contacts_btn = tk.Button(self.side_panel,width=10,text="Medical",font=("Arial",18),bg="#3c6382",fg="#ffffff",command=self.show_medical_contacts,activebackground="#3c6382")
        self.medical_contacts_btn.grid(row=5,column=0,pady=15)
        self.others_contacts_btn = tk.Button(self.side_panel,width=10,text="Others",font=("Arial",18),bg="#6F1E51",fg="#ffffff",command=self.show_others_contacts,activebackground="#6F1E51")
        self.others_contacts_btn.grid(row=6,column=0,pady=15)
        self.container = tk.Frame(self.root, background="turquoise")
        self.buttons_frame_main = tk.Frame(self.container,background="turquoise")
        self.buttons_frame_main.pack(pady=15)
        self.search_by_name_btn = tk.Button(self.buttons_frame_main,text="Search\nall contacts",bg="#0c2461",fg="#FFFFFF",command=self.search_by_name,font=("Arial",12),image=self.search_contact_image,compound=tk.LEFT,padx=3,activebackground="#0c2461")
        self.search_by_name_btn.grid(row=0,column=0)
        self.search_term = tk.StringVar()
        self.search_entry = tk.Entry(self.buttons_frame_main,textvariable=self.search_term,bg="#ffffff",bd=2,font=("Arial",12))
        self.search_entry.bind("<KeyRelease>",self.listen_typing_search_entry)
        self.add_contact_btn = tk.Button(self.buttons_frame_main,text="Add new contact", command=self.add_contact_to_phonebook,bg="#0c2461",fg="white",font=("Arial",12),image=self.add_contact_image,compound=tk.LEFT,padx=3)
        self.add_contact_btn.grid(row=0,column=2,padx=3)
        self.canvas = tk.Canvas(self.container, width=410, height=500)
        self.canvas.configure(bg="#ffffff")
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, background="#70a1ff")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.container.pack(pady=2)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.groupname_list = ["Family", "Friends", "Work", "Neighbours", "Medical", "Others"]
        self.establish_connection_to_database()
        display_query = "SELECT * FROM my_contacts ORDER BY firstname;"
        self.refresh_updated_data(display_query)
        self.root.mainloop()

    # Function to establish connection to backend database.
    def establish_connection_to_database(self):
        # Check whether database is present or not.
        query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'my_phonebook';"
        self.cursor_object.execute(query)
        self.answer = self.cursor_object.fetchone()
        if self.answer:
            pass
        else:  # Create a database named 'my_phonebook' if no such database exists.
            command_db_creation = "CREATE DATABASE my_phonebook;"
            self.cursor_object.execute(command_db_creation)
        command_str = "USE my_phonebook"
        self.cursor_object.execute(command_str)
        self.database_name_var = "my_phonebook"
        # Check if there is table 'my_contacts' present in database 'my_phonebook'.
        # If there is no such table, create table.
        try:
            query = "SELECT * FROM my_contacts;"
            self.cursor_object.execute(query)
            table_rows = self.cursor_object.fetchall()
        except Exception as err:
            query = "CREATE TABLE my_contacts (id int NOT NULL AUTO_INCREMENT,firstname VARCHAR(255),lastname VARCHAR(255),phonenumber VARCHAR(20),groupname VARCHAR(100),address VARCHAR(255),PRIMARY KEY (id));"
            self.cursor_object.execute(query)


    # Function to display rows from table based on the query input passed as argument.
    def refresh_updated_data(self,display_query):
        try:
            self.cursor_object.execute(display_query)
            # Delete all widgets inside the frame 'scrollable_frame'.
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            # Add new widgets to frame 'scrollable_frame' byb fetching data from the table.
            result = self.cursor_object.fetchall()
            for record_ptr in range(len(result)):
                user_data = result[record_ptr][1]+" "+result[record_ptr][2]
                # Create a frame to place the Label and Button widgets in it.
                person_var = tk.IntVar()
                person_var.set(result[record_ptr][0])
                # Label widget containing user data from fetched from table
                person_label = tk.Label(self.scrollable_frame, bg="white",fg="#000000", font=("Times New Roman", 14), width=50, padx=2,text=user_data,anchor=tk.W)
                person_label.grid(row=record_ptr,column=0,pady=1,padx=2)
                person_label.bind("<Button-1>",lambda event,details=result[record_ptr]:self.clicked_contact(event,details))
        except:
            messagebox.showerror("Error occurred", "Unable to refresh")

    def clicked_contact(self,event,details_tuple):
        self.display_contact_details(details_tuple)

    # Function to go back to the home window of the application.
    def open_main_window(self,frame_to_destroy):
        frame_to_destroy.destroy()
        self.container.pack(pady=2)
        self.show_all_contacts()

    # Function to insert new contact in the table 'my_contacts' based on the values inputted into the Entry widgets.
    def save_contact(self,fname_input,lastname_input,phonenumber_input,group_input,address_input,save_button):
        if fname_input!="" and phonenumber_input!="":
            formula = "INSERT INTO my_contacts (firstname,lastname,phonenumber,groupname,address) VALUES (%s,%s,%s,%s,%s)"
            self.cursor_object.execute(formula,(fname_input,lastname_input,phonenumber_input,group_input,address_input))
            self.db.commit()
            messagebox.showinfo("Contact Added","New contact saved to Phonebook")
            save_button.destroy()
        else:
            messagebox.showwarning("Invalid contact","First name and phone number is mandatory")


    def edit_button_clicked(self,edit_button,save_changes_button,details,fname_display,lname_display,phonenum_display,groupname_display,address_display,fname_entry,lname_entry,phonenum_entry,radiobuttonlist,x,address_label,address_entry):
        edit_button.destroy()
        save_changes_button.grid(row=0,column=2,padx=6)
        # Hide
        fname_display.grid_forget()
        lname_display.grid_forget()
        phonenum_display.grid_forget()
        groupname_display.grid_forget()
        address_display.grid_forget()
        # Display all Entry widgets and radio button widgets to make changes to the currently displaying contact.
        fname_entry.grid(row=0,column=1)
        fname_entry.insert(0,details[1])
        lname_entry.grid(row=1,column=1)
        lname_entry.insert(0,details[2])
        phonenum_entry.grid(row=2,column=1)
        phonenum_entry.insert(0,details[3])
        radiobuttonlist[0].grid(row=3,column=1)
        radiobuttonlist[1].grid(row=4,column=1)
        radiobuttonlist[2].grid(row=5,column=1)
        radiobuttonlist[3].grid(row=6,column=1)
        radiobuttonlist[4].grid(row=7,column=1)
        radiobuttonlist[5].grid(row=8,column=1)
        address_label.grid(row=9,column=0)
        address_entry.grid(row=9,column=1)
        address_entry.insert(0,details[5])


    # Function to update changes made to contact using editing.
    def save_changes_to_contact(self,save_changes_button,id_input,fname_var,lastname_var,phonenumber_var,groupname_var,address_var,fname_display,lname_display,phonenum_display,groupname_display,address_display,fname_entry,lname_entry,phonenum_entry,radiobutton_list,address_label,address_entry):
        formula = f"UPDATE my_contacts SET firstname=%s,lastname=%s,phonenumber=%s,groupname=%s,address=%s WHERE id={id_input};"
        self.cursor_object.execute(formula,(fname_var,lastname_var,phonenumber_var,groupname_var,address_var))
        self.db.commit()
        messagebox.showinfo("Contact updated","Contact details updated!")
        save_changes_button.destroy()
        # Hide Entry widgets
        fname_entry.grid_forget()
        lname_entry.grid_forget()
        phonenum_entry.grid_forget()
        # Hide radio buttons
        radiobutton_list[0].grid_forget()
        radiobutton_list[1].grid_forget()
        radiobutton_list[2].grid_forget()
        radiobutton_list[3].grid_forget()
        radiobutton_list[4].grid_forget()
        radiobutton_list[5].grid_forget()
        # Hide the Entry widget for address
        address_entry.grid_forget()
        # Display all Label widgets in the column1 with the updated data.
        fname_display.grid(row=0,column=1)
        fname_display.config(text=fname_var)
        lname_display.grid(row=1,column=1)
        lname_display.config(text=lastname_var)
        phonenum_display.grid(row=2,column=1)
        phonenum_display.config(text=phonenumber_var)
        groupname_display.grid(row=3,column=1)
        groupname_display.config(text=groupname_var)
        address_label.grid(row=4,column=0)
        address_display.grid(row=4,column=1)
        address_display.config(text=address_var)


    # Function to insert new contact into the table.
    def add_contact_to_phonebook(self):
        # Hide the container frame.
        self.container.pack_forget()
        # Create a new frame
        self.add_contact_frame = tk.Frame(self.root)
        self.add_contact_frame.pack()
        # Frame to hold 'Back' and 'Save' buttons in a row.
        frame1 = tk.Frame(self.add_contact_frame)
        frame1.pack(expand=tk.TRUE)
        self.go_back_button = tk.Button(frame1,text="Back",bg="black",fg="#ffffff",font=("Arial",14),command=lambda :self.open_main_window(self.add_contact_frame),image=self.back_icon_image,compound=tk.LEFT,activebackground="#000000",activeforeground="#ffffff")
        self.go_back_button.grid(row=0,column=0)
        tk.Label(frame1).grid(row=0,column=1,padx=28)
        self.save_button = tk.Button(frame1,text="Save contact",bg="blue",fg="white",font=("Arial",14))
        self.save_button.grid(row=0,column=2)
        # variables
        self.firstname_var = tk.StringVar()
        self.lastname_var = tk.StringVar()
        self.phone_number_var = tk.StringVar()
        self.groupname_var = tk.StringVar()
        self.address_var = tk.StringVar()
        # UI widgets
        tk.Label(self.add_contact_frame,text="First name",font=("Cambria",17)).pack()
        self.firstname_entry = tk.Entry(self.add_contact_frame,textvariable=self.firstname_var,font=("Cambria",17))
        self.firstname_entry.pack()
        tk.Label(self.add_contact_frame, text="Last name",font=("Cambria",17)).pack()
        self.lastname_entry = tk.Entry(self.add_contact_frame, textvariable=self.lastname_var,font=("Cambria",17))
        self.lastname_entry.pack()
        tk.Label(self.add_contact_frame, text="Phone number",font=("Cambria",17)).pack()
        self.phonenumber_entry = tk.Entry(self.add_contact_frame, textvariable=self.phone_number_var,font=("Cambria",17))
        self.phonenumber_entry.pack()
        tk.Label(self.add_contact_frame, text="Group",font=("Cambria",17)).pack()
        groupname_list = ["Family","Friends","Work","Neighbours","Medical","Others"]
        # variable for radiobutton
        self.x = tk.IntVar()
        # Radiobuttons
        radio1 = tk.Radiobutton(self.add_contact_frame, value=0, text=groupname_list[0], variable=self.x,font=("Cambria",12))
        radio1.pack()
        radio2 = tk.Radiobutton(self.add_contact_frame, value=1, text=groupname_list[1], variable=self.x,font=("Cambria",12))
        radio2.pack()
        radio3 = tk.Radiobutton(self.add_contact_frame, value=2, text=groupname_list[2], variable=self.x,font=("Cambria",12))
        radio3.pack()
        radio4 = tk.Radiobutton(self.add_contact_frame, value=3, text=groupname_list[3], variable=self.x,font=("Cambria",12))
        radio4.pack()
        radio5 = tk.Radiobutton(self.add_contact_frame, value=4, text=groupname_list[4], variable=self.x,font=("Cambria",12))
        radio5.pack()
        radio6 = tk.Radiobutton(self.add_contact_frame, value=5, text=groupname_list[5], variable=self.x,font=("Cambria",12))
        radio6.pack()
        self.groupname_var.set(groupname_list[self.x.get()])
        tk.Label(self.add_contact_frame, text="Address",font=("Cambria",17)).pack()
        self.address_entry = tk.Entry(self.add_contact_frame, textvariable=self.address_var,font=("Cambria",17))
        self.address_entry.pack()
        # Pass the widgets to the save button's command function.
        self.save_button.config(command=lambda :self.save_contact(self.firstname_var.get(),self.lastname_var.get(),self.phone_number_var.get(),groupname_list[self.x.get()],self.address_var.get(),self.save_button))

    # Function to display a selected contact in a separate frame.
    def display_contact_details(self,details):
        # Hide the container frame.
        self.container.pack_forget()
        # Create a frame
        display_contact_card = tk.Frame(self.root,width=580,padx=5,pady=10)
        display_contact_card.pack()
        buttons_frame = tk.Frame(display_contact_card)
        buttons_frame.grid(row=0,column=0,columnspan=2)
        back_button = tk.Button(buttons_frame,text="Back",command=lambda :self.open_main_window(display_contact_card),bg="#000000",fg="#ffffff",font=("Arial",14),image=self.back_icon_image,compound=tk.LEFT,activebackground="#000000",activeforeground="#ffffff")
        back_button.grid(row=0,column=0)
        tk.Label(buttons_frame).grid(row=0,column=1,padx=30)
        save_changes_button = tk.Button(buttons_frame, text="Save changes",bg="#000000",fg="#FFFFFF",font=("Arial",14))
        edit_button = tk.Button(buttons_frame,text="Edit",command=lambda :self.edit_button_clicked(edit_button,save_changes_button,details),bg="#000000",fg="#ffffff",font=("Arial",14))
        edit_button.grid(row=0,column=2,padx=7)
        delete_contact_button = tk.Button(buttons_frame,text="Delete",bg="red",fg="#FFFFFF",command=lambda :self.delete_contact(details[0],delete_contact_button,back_button),font=("Arial",14))
        delete_contact_button.grid(row=0,column=3)
        card_frame = tk.Frame(display_contact_card,width=550,background="#ffffff")
        card_frame.grid(row=1,column=0,pady=10)
        tk.Label(card_frame,text="First name:",font=("Arial",14),bg="#FFFFFF").grid(row=0,column=0,pady=5)
        fname_display = tk.Label(card_frame,text=details[1],font=("Arial",14),bg="#FFFFFF")
        fname_display.grid(row=0,column=1)
        fname_var = tk.StringVar()
        fname_entry = tk.Entry(card_frame,textvariable=fname_var,font=("Cambria",14))
        tk.Label(card_frame,text="Last name:",font=("Arial",14),bg="#FFFFFF").grid(row=1,column=0,pady=5)
        lname_display = tk.Label(card_frame,text=details[2],font=("Arial",14),bg="#FFFFFF")
        lname_display.grid(row=1,column=1)
        lname_var = tk.StringVar()
        lname_entry = tk.Entry(card_frame,textvariable=lname_var,font=("Cambria",14))
        tk.Label(card_frame,text="Phone number:",font=("Arial",14),bg="#FFFFFF").grid(row=2,column=0,pady=5)
        phonenum_display = tk.Label(card_frame,text=details[3],font=("Arial",14),bg="#FFFFFF")
        phonenum_display.grid(row=2,column=1)
        phonenum_var = tk.StringVar()
        phonenum_entry = tk.Entry(card_frame,textvariable=phonenum_var,font=("Cambria",14))
        tk.Label(card_frame, text="Group:", font=("Arial", 14), bg="#FFFFFF").grid(row=3, column=0,pady=5)
        groupname_display = tk.Label(card_frame, text=details[4], font=("Arial", 14), bg="#FFFFFF")
        groupname_display.grid(row=3, column=1)
        groupname_var = tk.StringVar()
        groupname_list = ["Family", "Friends", "Work", "Neighbours", "Medical", "Others"]
        self.x = tk.IntVar()
        radio1 = tk.Radiobutton(card_frame,value=0, text=groupname_list[0], variable=self.x,font=("Cambria",14),bg="#FFFFFF")
        radio2 = tk.Radiobutton(card_frame,value=1,text=groupname_list[1],variable=self.x,font=("Cambria",14),bg="#FFFFFF")
        radio3 = tk.Radiobutton(card_frame, value=2, text=groupname_list[2], variable=self.x,font=("Cambria",14),bg="#FFFFFF")
        radio4 = tk.Radiobutton(card_frame, value=3, text=groupname_list[3], variable=self.x,font=("Cambria",14),bg="#FFFFFF")
        radio5 = tk.Radiobutton(card_frame, value=4, text=groupname_list[4], variable=self.x,font=("Cambria",14),bg="#FFFFFF")
        radio6 = tk.Radiobutton(card_frame, value=5, text=groupname_list[5], variable=self.x,font=("Cambria",14),bg="#FFFFFF")
        self.x.set(self.groupname_list.index(details[4]))
        radiobutton_list = [radio1,radio2,radio3,radio4,radio5,radio6]
        # address
        address_label = tk.Label(card_frame, text="Address:", font=("Arial", 14), bg="#FFFFFF")
        address_label.grid(row=4, column=0,pady=5)
        address_display = tk.Label(card_frame, text=details[5], font=("Arial", 14), bg="#FFFFFF")
        address_display.grid(row=4, column=1)
        address_var = tk.StringVar()
        address_entry = tk.Entry(card_frame, textvariable=address_var,font=("Cambria",14))
        # Set the command functions for the buttons by passing arguments.
        edit_button.config(command=lambda :self.edit_button_clicked(edit_button,save_changes_button,details,fname_display,lname_display,phonenum_display,groupname_display,address_display,fname_entry,lname_entry,phonenum_entry,radiobutton_list,self.x,address_label,address_entry))
        save_changes_button.config(command=lambda :self.save_changes_to_contact(save_changes_button,details[0],fname_var.get(),lname_var.get(),phonenum_var.get(),groupname_list[self.x.get()],address_var.get(),fname_display,lname_display,phonenum_display,groupname_display,address_display,fname_entry,lname_entry,phonenum_entry,radiobutton_list,address_label,address_entry))

    # Function to delete a oontact from the table.
    def delete_contact(self,id_input,delete_contact_button,back_button):
        deletion_query = f"DELETE FROM my_contacts WHERE id={id_input}"
        self.cursor_object.execute(deletion_query)
        self.db.commit()
        delete_contact_button.destroy()
        back_button.invoke()

    # Function to show the Entry widget which acts as a search bar to search contacts.
    def search_by_name(self):
        self.search_entry.grid(row=0,column=1,padx=5)


    # Function to display filtered contacts which starts with certain characters based on the characters typed in the search bar widget.
    def listen_typing_search_entry(self,event):
        search_query = f"SELECT * FROM my_contacts WHERE firstname LIKE '{self.search_term.get()}%' ORDER BY firstname"
        self.refresh_updated_data(search_query)

    # Function to display all rows from table by sorting them by the column 'firstname'.
    def show_all_contacts(self):
        display_query = "SELECT * FROM my_contacts ORDER BY firstname;"
        self.refresh_updated_data(display_query)
        self.container.config(background="turquoise")
        self.buttons_frame_main.config(background="turquoise")

    # Function to display all rows which comes under the groupname 'Family' from the table by sorting them by the column 'firstname'.
    def show_family_contacts(self):
        search_query = "SELECT * FROM my_contacts WHERE groupname='Family' ORDER BY firstname;"
        self.refresh_updated_data(search_query)
        self.container.config(background="#eb2f06")
        self.buttons_frame_main.config(background="#eb2f06")

    # Function to display all rows which comes under the groupname 'Friends' from the table by sorting them by the column 'firstname'.
    def show_friends_contacts(self):
        search_query = "SELECT * FROM my_contacts WHERE groupname='Friends' ORDER BY firstname;"
        self.refresh_updated_data(search_query)
        self.container.config(background="green")
        self.buttons_frame_main.config(background="green")


    # Function to display all rows which comes under the groupname 'Work' from the table by sorting them by the column 'firstname'.
    def show_work_contacts(self):
        search_query = "SELECT * FROM my_contacts WHERE groupname='Work' ORDER BY firstname;"
        self.refresh_updated_data(search_query)
        self.container.config(background="#fa983a")
        self.buttons_frame_main.config(background="#fa983a")


    # Function to display all rows which comes under the groupname 'Neighbours' from the table by sorting them by the column 'firstname'.
    def show_neighbours_contacts(self):
        search_query = "SELECT * FROM my_contacts WHERE groupname='Neighbours' ORDER BY firstname;"
        self.refresh_updated_data(search_query)
        self.container.config(background="#D980FA")
        self.buttons_frame_main.config(background="#D980FA")

    # Function to display all rows which comes under the groupname 'Medical' from the table by sorting them by the column 'firstname'.
    def show_medical_contacts(self):
        search_query = "SELECT * FROM my_contacts WHERE groupname='Medical' ORDER BY firstname;"
        self.refresh_updated_data(search_query)
        self.container.config(background="#3c6382")
        self.buttons_frame_main.config(background="#3c6382")

    # Function to display all rows which comes under the groupname 'Others' from the table by sorting them by the column 'firstname'.
    def show_others_contacts(self):
        search_query = "SELECT * FROM my_contacts WHERE groupname='Others' ORDER BY firstname;"
        self.refresh_updated_data(search_query)
        self.container.config(background="#6F1E51")
        self.buttons_frame_main.config(background="#6F1E51")

