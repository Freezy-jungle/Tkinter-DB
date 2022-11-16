import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
import mysql.connector


top = tk.Tk()

top.title('STUDENT MANAGEMENT SYSTEM')
top.config(bg= 'skyblue')
top.geometry('1300x700')
con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'StudentManagerSystem')
mycursor = con.cursor()

items = ['Male', 'Female']

pop_window = tk.Toplevel()
pop_window.title('MAKE YOUR CHANGES')
pop_window.geometry('1000x1000')

RecDel_button = tk.Button(text= "Record / Close")



def submit_rec():
    
    Name = entry_name.get()
    Contact_number = entry_ContNumber.get()
    Email_address = entry_EmAddres.get()
    Gender = entry_gender.get()
    DOB = entry_birth.get()
    Stream = entry_stream.get()

    try:
        sql = """ INSERT INTO SMS VALUES (%s, %s, %s, %s, %s, %s) """

        mycursor.execute(sql, (Name, Contact_number, Email_address, Gender, DOB, Stream))
        con.commit()
        messagebox.showinfo('information', 'Record inserted successfullt...')
        view_refresh()
        clear_fields()

    except Exception as e:
        print(e)
        con.close()


def view_refresh():
    sql_out = """ SELECT * FROM SMS """
    mycursor.execute(sql_out)
    rows = mycursor.fetchall()
    total = mycursor.rowcount
    print('Total Data Entries: ' +str(total))

    db_frame = tk.Frame(top, width=700, height= 700, bg= 'white')
    db_frame.grid(row= 1, column= 2, rowspan= 7, padx = 10, sticky= 'we, n')

    columns = ('name', 'contact_number', 'email_address', 'gender', 'dob', 'stream')
    tv = ttk.Treeview(db_frame, selectmode= 'browse', columns= columns, show='headings', height='10')
    tv.grid(row= 1, column= 1, padx= 10, pady= 10)
    tv["columns"]=("1","2","3","4","5","6")
    tv['show']='headings'

    tv.column("1", width=80, anchor= "c")
    tv.column("2", width=80, anchor= "c")
    tv.column("3", width=80, anchor= "c")
    tv.column("4", width=80, anchor= "c")
    tv.column("5", width=80, anchor= "c")
    tv.column("6", width=80, anchor= "c")

    tv.heading('1', text= 'Name')
    tv.heading('2', text= 'Contact_number')
    tv.heading('3', text= 'Email_address')
    tv.heading('4', text= 'Gender')
    tv.heading('5', text= 'DOB')
    tv.heading('6', text= 'Stream')

    for i, (name, contact_number, email_address, gender, dob, stream) in enumerate(rows, start =1):
        # print(i)
        tv.insert('', 'end', values= (name, contact_number, email_address, gender, dob, stream))


def clear_fields():
    entry_name.delete(0, 'end')
    entry_ContNumber.delete(0, 'end')
    entry_EmAddres.delete(0, 'end')
    entry_gender.delete(0, 'end')
    entry_birth.delete(0, 'end')
    entry_stream.delete(0, 'end')


def remove_table():
    try:
        sql = """ delete from SMS """

        mycursor.execute(sql)
        con.commit()
        messagebox.showinfo('information', 'Fields clear successfully...')
    except Exception as e:
        print(e)
        con.close()


def deletedrecord():
    Name = entry_name.get()

    try:
        sql = """ delete from SMS where Name = %s """

        mycursor.execute(sql, (Name, ))
        con.commit()
        messagebox.showinfo('information', 'Record deleted successfully...')
        view_refresh()
        clear_fields()

    except Exception as e:
        print(e)
        con.close()


def update():
    Name = entry_name.get()
    try:
        sql = """ UPDATE sms SET WHERE Name = %s """

        mycursor.execute(sql, (Name, ))
        con.commit()
        messagebox.showinfo('information', 'Record updated successfully...')
        view_refresh()
        clear_fields()

    except Exception as e:
        print(e)
        con.close()

label_name = tk.Label(top, text= 'Name', font= ('Fusion', 10), bg= 'skyblue')
label_name.grid(row=0, column=0, padx=10, pady= 10, sticky= 'w')
entry_name = tk.Entry(top)
entry_name.grid(row=0, column=1, padx= 10, pady= 10)

label_ContNumber = tk.Label(top, text= 'Contact number', font= ('Fusion', 10), bg= 'skyblue')
label_ContNumber.grid(row=1, column=0, padx=10, pady= 10, sticky= 'w')
entry_ContNumber = tk.Entry(top)
entry_ContNumber.grid(row=1, column=1, padx= 10, pady= 10)

label_EmAddres = tk.Label(top, text= 'Email Address', font= ('Fusion', 10), bg= 'skyblue')
label_EmAddres.grid(row=2, column=0, padx=10, pady= 10, sticky= 'w')
entry_EmAddres = tk.Entry(top)
entry_EmAddres.grid(row=2, column=1, padx= 10, pady= 10)

label_gender = tk.Label(top, text= 'Gender', font= ('Fusion', 10), bg= 'skyblue')
label_gender.grid(row=3, column=0, padx=10, pady= 10, sticky= 'w')
entry_gender = ttk.Combobox(top, values= items)
entry_gender.grid(row=3, column=1, padx= 10, pady= 10)

label_birth = tk.Label(top, text= 'Date of Birth (DOB)', font= ('Fusion', 10), bg= 'skyblue')
label_birth.grid(row=4, column=0, padx=10, pady= 10, sticky= 'w')
entry_birth = DateEntry(top, date_pattern= 'dd/mm/yyyy')
entry_birth.grid(row=4, column=1, padx= 10, pady= 10)

label_stream = tk.Label(top, text= 'Stream', font= ('Fusion', 10), bg= 'skyblue')
label_stream.grid(row=5, column=0, padx=10, pady= 10, sticky= 'w')
entry_stream = tk.Entry(top)
entry_stream.grid(row=5, column=1, padx= 10, pady= 10)

top.grid_columnconfigure(0, minsize= 350)
top.grid_columnconfigure(1, minsize= 100)

btn_SubmAddRec = tk.Button(top, text= 'Submit and Add Record', command= submit_rec)
btn_DelRec = tk.Button(top, text= 'Delete Record', command= deletedrecord)
btn_ViewRefresh = tk.Button(top, text= 'View Refresh', command= view_refresh)
btn_ClearF = tk.Button(top, text= 'Clear Fields', command= clear_fields)
btn_UpdateData = tk.Button(top, text= 'Update Data', command= update)

btn_SubmAddRec.grid(row=6, column=0, columnspan=2, stick= 'we', padx=10, pady=80)
btn_DelRec.grid(row= 7, column=0, stick = 'we', padx= 10)
btn_ViewRefresh.grid(row=7, column=1, stick = 'we', padx= 10)
btn_ClearF.grid(row=8, column=0, stick = 'we', padx= 10, pady= 10)
btn_UpdateData.grid(row=8, column=1, stick = 'we', padx= 10, pady= 10)


top.mainloop()
 
