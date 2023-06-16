import pymssql #import python ms sql library
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime
import uuid
import base64

conn = pymssql.connect(host='cypress.csil.sfu.ca',user='s_dsb9',password='3nbjhR2G7FnGa4F3',database='dsb9354')
mycursor = conn.cursor()
mycursor.execute('SELECT * from dbo.helpdesk')

row = mycursor.fetchone()
while row:
    print(row)
    row = mycursor.fetchone()

#################################Start of Login page###################################
def login_page():
    global greeting_frame, textbox_frame, button_frame

    # Create widgets for the login page.
    greeting_frame = tkinter.Frame(root)
    greeting_frame.pack()
    textbox_frame = tkinter.Frame(root)
    textbox_frame.pack()
    button_frame = tkinter.Frame(root)
    button_frame.pack(pady=20)

    greeting_label = tkinter.Label(greeting_frame, text='Welcome to my Database Application', font=("Arial", 14, "bold"))
    greeting_label.pack(pady=20)
    entry_label = tkinter.Label(textbox_frame, text='Enter your User ID:')
    entry_label.grid(row=0, column=0)

    global login_entry,login_user
    login_entry = tkinter.Entry(textbox_frame, width=20)
    login_entry.insert(0, 'ID') #example id: __pce5zHvkmGRao0GOy5Zg
    login_entry.grid(row=0, column=1)
    login_user = login_entry.get()
    login_button = tkinter.Button(button_frame, text="Login", command=check_login, width = 20)
    login_button.pack()

#Example User ID = __pce5zHvkmGRao0GOy5Zg
# Define a function to check if the user id is in the user_id column of dbo.user_yelp.
def check_login():
    user_id = login_entry.get()
    mycursor.execute("SELECT user_id FROM dbo.user_yelp")
    rows = mycursor.fetchall()
    user_ids = [row[0] for row in rows]

    if user_id in user_ids:
        messagebox.showinfo("Success", "Login successful!", parent=root)
        second_page()
    else:
        messagebox.showerror("Error", "Login failed.", parent=root)
#################################End of Login page###################################

#################################Start of Second page###################################
def second_page():
    global secondpage_label, secondpage_buttons
    # Destroy the widgets from the previous page.
    greeting_frame.destroy()
    textbox_frame.destroy()
    button_frame.destroy()

    # Create new widgets for the new page.
    secondpage_label = tkinter.Label(root, text='You are now logged in!')
    secondpage_label.pack(pady=20)
    secondpage_buttons = tkinter.Frame(root)
    secondpage_buttons.pack(side=tkinter.TOP, pady=20)
    secondpage_label2 = tkinter.Label(secondpage_buttons, text="Select one of the two:", font=("Arial", 14, "bold"))
    secondpage_label2.pack(side=tkinter.TOP)
    search_business_button = tkinter.Button(secondpage_buttons, text="Search Business", width=20, command=business_page)
    search_business_button.pack(side=tkinter.TOP, padx=5, pady=5)
    search_users_button = tkinter.Button(secondpage_buttons, text="Search Users", width=20, command=users_page)
    search_users_button.pack(side=tkinter.TOP, padx=5, pady=5)
    back_button = tkinter.Button(secondpage_buttons, text="Back", command=go_back_loginpage)
    back_button.pack(side=tkinter.BOTTOM, pady=20)

def go_back_loginpage():
    # Destroy the widgets from the current page.
    secondpage_label.destroy()
    secondpage_buttons.destroy()
    # Create the widgets from the previous page.
    login_page()
#################################End of second page###################################

#################################Start of Business page###################################
def business_page():
    global thirdpage_label, search_frame, businesspage_button
    # Destroy the widgets from the current page.
    secondpage_label.destroy()
    secondpage_buttons.destroy()

    # Create new widgets for the business search page.
    thirdpage_label = tkinter.Label(root, text='Business Search', font=("Arial", 14, "bold"))
    thirdpage_label.pack(pady=20)
    search_frame = tkinter.Frame(root)
    search_frame.pack()
    businesspage_button = tkinter.Frame(root)
    businesspage_button.pack(side=tkinter.TOP, pady=20)

    # Create the sort selector.
    sort_label = tkinter.Label(search_frame, text='Sort Stars by:')
    sort_label.grid(row=0, column=0, columnspan=1)
    stars_combobox = ttk.Combobox(search_frame, values=['Min Stars', 'Max Stars'], state="readonly")
    stars_combobox.grid(row=0, column=1, columnspan=2)
    city_label = tkinter.Label(search_frame, text='City:')
    city_label.grid(row=1, column=0,columnspan=1)
    city_entry = tkinter.Entry(search_frame)
    city_entry.grid(row=1, column=1,columnspan=2)
    name_label = tkinter.Label(search_frame, text='Name:')
    name_label.grid(row=2, column=0,columnspan=1)

    global name_entry
    name_entry = tkinter.Entry(search_frame)
    name_entry.grid(row=2, column=1,columnspan=2)
    # Create the search button.
    search_button = tkinter.Button(search_frame, text='Search', width = 20, command=lambda:business_searching(stars_combobox.get(),city_entry.get(),name_entry.get()))
    search_button.grid(row=3, column=1, columnspan=2, pady=10)
    # Create the back button.
    back_button = tkinter.Button(businesspage_button, text='Back', command=go_back_secondpage)
    back_button.pack(side=tkinter.BOTTOM, pady=20)

def business_searching(stars,city,name):
    headings = ['ID', 'Name', 'Address','City','Stars']
    columns = ['0','1','2','3','4']
    result = business_qy(stars,city,name,conn)
    table_maker(columns,headings,result,search_frame,0)
    
def business_qy(stars,city,name,connection):
# Define the query for retrieving the business data
    if stars == '':
        query = """
            SELECT business_id, name, address, city, stars 
            FROM dbo.business 
            WHERE name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI 
                AND city COLLATE Latin1_General_CI_AI LIKE %(city)s 
            ORDER BY name
        """
        params = {'name': f'%{name}%', 'city': f'%{city}%'}
    elif stars == 'Min Stars':
        query = """
            SELECT business_id, name, address, city, stars 
            FROM dbo.business 
            WHERE stars = (
                SELECT MIN(stars) 
                FROM dbo.business 
                WHERE name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI 
                    AND city COLLATE Latin1_General_CI_AI LIKE %(city)s
            ) AND name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI 
                AND city COLLATE Latin1_General_CI_AI LIKE %(city)s 
            ORDER BY name
        """
        params = {'name': f'%{name}%', 'city': f'%{city}%', 'stars': stars}
    elif stars == 'Max Stars':
        query = """
            SELECT business_id, name, address, city, stars 
            FROM dbo.business 
            WHERE stars = (
                SELECT MAX(stars) 
                FROM dbo.business 
                WHERE name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI 
                    AND city COLLATE Latin1_General_CI_AI LIKE %(city)s
            ) AND name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI 
                AND city COLLATE Latin1_General_CI_AI LIKE %(city)s 
            ORDER BY name
        """
        params = {'name': f'%{name}%', 'city': f'%{city}%', 'stars': stars}

    # Execute the query and fetch the data
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        data = cursor.fetchall()

    # Display a message box if no data were found
    if not data:
        messagebox.showinfo("Message", "No data was found based on your search")

    return data

def pre_review(event):
    item = event.widget.item(event.widget.selection())
    id, name = item['values'][:2]

    result = messagebox.askyesno("Message", f"Do you want to write a review for {name}?")
    if result:
        stars = simpledialog.askstring('Rate', 'Please rate the business from 0 to 5:')
        if stars is None:
            messagebox.showinfo('Message', f"You did not rate {name}.")
        elif (float(stars) > 5) or (float(stars) < 0):
            messagebox.showerror('Error', f"Please rate {name} between 1 and 5.")
        else:
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            review(str(login_user), id, stars, current_date)
            messagebox.showinfo('Message', f"You rated {name} {stars} stars! Have a good day!")
    else:
        messagebox.showinfo('Message', f"You did not rate {name}.")


def review(user_id, business_id, stars, date):
    uid = uuid.uuid4()
    uid_str = base64.urlsafe_b64encode(uid.bytes).rstrip(b'=').decode('utf-8')[:22]

    with conn.cursor() as cursor:
        cursor.execute(
            'INSERT INTO dbo.review (review_id, user_id, business_id, stars, date) '
            'VALUES (%(review)s, %(username)s, %(business)s, %(stars)s, %(date)s)',
            {'review': uid_str, 'username': user_id, 'business': str(business_id), 'stars': float(stars), 'date': date}
        )
        conn.commit()

def go_back_secondpage():
    # Destroy the widgets from the current page.
    thirdpage_label.destroy()
    search_frame.destroy()
    businesspage_button.destroy()
    # Create the widgets from the previous page.
    second_page()
#################################End of Business page###################################

#################################Start of Users page###################################
def users_page():
    global thirdpage_label2, search_frame2, userspage_button
    # Destroy the widgets from the current page.
    secondpage_label.destroy()
    secondpage_buttons.destroy()

    # Create new widgets for the users search page.
    thirdpage_label2 = tkinter.Label(root, text='Users Search', font=("Arial", 14, "bold"))
    thirdpage_label2.pack(pady=20)
    search_frame2 = tkinter.Frame(root)
    search_frame2.pack()
    userspage_button = tkinter.Frame(root)
    userspage_button.pack(side=tkinter.TOP, pady=20)

    #name
    name_label2 = tkinter.Label(search_frame2, text='Name:')
    name_label2.grid(row=0, column=1,columnspan=1)
    name_entry2 = tkinter.Entry(search_frame2)
    name_entry2.grid(row=0, column=2,columnspan=1)

    # Create the sort selector.
    sort_label = tkinter.Label(search_frame2, text='Useful:')
    sort_label.grid(row=1, column=1,columnspan=1)
    useful_combobox = ttk.Combobox(search_frame2, values=['Yes', 'No'], state="readonly")
    useful_combobox.grid(row=1, column=2,columnspan=1)
    useful = useful_combobox.get()
    sort_label = tkinter.Label(search_frame2, text='Funny:')
    sort_label.grid(row=2, column=1,columnspan=1)
    funny_combobox = ttk.Combobox(search_frame2, values=['Yes', 'No'], state="readonly")
    funny_combobox.grid(row=2, column=2,columnspan=1)
    funny = funny_combobox.get()
    sort_label = tkinter.Label(search_frame2, text='Cool:')
    sort_label.grid(row=3, column=1,columnspan=1)
    cool_combobox = ttk.Combobox(search_frame2, values=['Yes', 'No'], state="readonly")
    cool_combobox.grid(row=3, column=2,columnspan=1)
    cool = cool_combobox.get()

    # Create the search button.
    search_button = tkinter.Button(search_frame2,width=20, text='Search', command=lambda:user_searching(name_entry2.get(), useful_combobox.get(),funny_combobox.get(),cool_combobox.get()))
    search_button.grid(row=4, column=2, columnspan=1, pady=10)
    # Create the back button.
    back_button = tkinter.Button(userspage_button, text='Back', command=go_back_secondpage2)
    back_button.pack(side=tkinter.BOTTOM, pady=20)

def user_searching(name,useful,funny, cool):
    headings = ['ID', 'Name', 'Useful','Funny','Cool','Date']
    columns = ['0','1','2','3','4','5']
    result2 = users_qy(name,useful,funny,cool,conn)
    table_maker(columns,headings,result2,search_frame2,1)

def users_qy(name,useful,funny,cool,connection):
    cursor = connection.cursor()
    useful_value = 1 if useful == 'Yes' else 0
    funny_value = 1 if funny == 'Yes' else 0
    cool_value = 1 if cool == 'Yes' else 0

    query = '''
            SELECT user_id, name, 
                CASE WHEN %(useful)s = 1 THEN useful ELSE 0 END AS useful,
                CASE WHEN %(funny)s = 1 THEN funny ELSE 0 END AS funny,
                CASE WHEN %(cool)s = 1 THEN cool ELSE 0 END AS cool,
                yelping_since
            FROM dbo.user_yelp
            WHERE name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI 
                AND useful >= %(useful)s
                AND funny >= %(funny)s
                AND cool >= %(cool)s
            ORDER BY name
            '''

    cursor.execute(query, {'name': f'%{name}%', 'useful': useful_value, 'funny': funny_value, 'cool': cool_value})
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("Message", "No data was found based on your search")

    return data

def pre_friendship(event):
    item = event.widget.item(event.widget.selection())
    friend_id, name = item['values'][:2]

    if messagebox.askyesno("Message", f"Would you like to be friends with {name}?"):
        add_friend(login_user, friend_id)
        messagebox.showinfo("Message", f"{name} is now your friend!")
    else:
        messagebox.showinfo("Message", f"You are not friends with {name}")


def add_friend(user_id, friend_id):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO dbo.friendship (user_id, friend) VALUES (%s, %s)', (user_id, friend_id))
    conn.commit()


def go_back_secondpage2():
    # Destroy the widgets from the current page.
    thirdpage_label2.destroy()
    search_frame2.destroy()
    userspage_button.destroy()

    # Create the widgets from the previous page.
    second_page()
#################################End of of Users page###################################

def table_maker(columns,headings,dataset,tree_frame,type1):
    tree_frame.pack()
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=19)

    for col, heading in zip(columns, headings):
        tree.column(col, width=130, anchor='center')
        tree.heading(col, text=heading)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tkinter.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.grid(row=6, column=0, columnspan=4)
    scrollbar.grid(row=6, column=4)

    for data in dataset:
        tree.insert('', tkinter.END, values=data)

    if type1 == 1:
        friend_info = tkinter.Label(search_frame2, text='If you want to make a friend, double click the row!', bg='#ffffff', font=("Arial", 10))
        friend_info.grid(row=5, column=2, pady=10)
        tree.bind('<Double-Button-1>', pre_friendship)
    elif type1 == 0:
        review_info = tkinter.Label(search_frame, text='If you want to rate a business, double click the row!', bg='#ffffff', font=("Arial", 10))
        review_info.grid(row=5, column=1, pady=10)
        tree.bind('<Double-Button-1>', pre_review)

root = tkinter.Tk()
root.title('Deep Bhimani - CMPT 354 Assignment 7')
root.geometry('900x760+300+300')
login_page()
root.mainloop()