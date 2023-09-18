import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END, messagebox, filedialog
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from db import Database


db = Database("Employee.db")
conn = sqlite3.connect('Employee.db')

root = tk.Tk()
root.title("emp")
root.geometry("800x800")
root.state("zoomed")

root.grid_columnconfigure(0, weight=1)

# Import necessary libraries (at the beginning of your script)


# ... (Your existing code for imports, setup, and loading data)

# Create a function to handle the gender distribution analysis

# Start the main GUI loop


# Entry frame var
name = tk.StringVar()
age = tk.StringVar()
gender = tk.StringVar()
email = tk.StringVar()
doj = tk.StringVar()
address = tk.StringVar()
contact = tk.StringVar()
username = tk.StringVar()
password = tk.StringVar()

# Button var
add = tk.StringVar()
update = tk.StringVar()
delete = tk.StringVar()

# Create a style for ttk widgets
style = ttk.Style()
style.configure("TFrame", background="forestgreen")
style.configure("TLabel", background="forestgreen", foreground="LightGoldenRodYellow", font=("Arial", 20))

# Creating the frame namely entries_frame
entries_frame = ttk.Frame(root)
entries_frame.grid(row=1, column=0, sticky="nsew")

title = ttk.Label(entries_frame, text="Employee Table", background="indigo", foreground="white")
title.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 10), sticky="N")
title.config(font=("Arial", 30))
# Name
lbName = ttk.Label(entries_frame, text="Name")
lbName.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
txName = ttk.Entry(entries_frame, textvariable=name, width=30)
txName.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Age
lbAge = ttk.Label(entries_frame, text="Age")
lbAge.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
txAge = ttk.Entry(entries_frame, textvariable=age, width=30)
txAge.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

# Gender
lbGen = ttk.Label(entries_frame, text="Gender")
lbGen.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
coGen = ttk.Combobox(entries_frame, width=27, textvariable=gender, state="readonly")
coGen['values'] = ("Male", "Female")
coGen.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Date of Joining
lbDoj = ttk.Label(entries_frame, text="Date of Joining")
lbDoj.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
txDoj = ttk.Entry(entries_frame, textvariable=doj, width=30)
txDoj.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

# Email
lbEmail = ttk.Label(entries_frame, text="Email")
lbEmail.grid(row=1, column=2, padx=20, pady=10, sticky="nsew")
txEmail = ttk.Entry(entries_frame, textvariable=email, width=30)
txEmail.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

# username
lbuse = ttk.Label(entries_frame, text="USERNAME")
lbuse.grid(row=1, column=5, padx=20, pady=10, sticky="nsew")
txuse = ttk.Entry(entries_frame, textvariable=username, width=30)
txuse.grid(row=1, column=6, padx=10, pady=10, sticky="nsew")

# password
lbpas = ttk.Label(entries_frame, text="PASSWORD")
lbpas.grid(row=2, column=5, padx=20, pady=10, sticky="nsew")
txpas = ttk.Entry(entries_frame, textvariable=password, width=30)
txpas.grid(row=2, column=6, padx=10, pady=10, sticky="nsew")

# Contact
lbCnt = ttk.Label(entries_frame, text="Contact")
lbCnt.grid(row=2, column=2, padx=20, pady=10, sticky="nsew")
txCnt = ttk.Entry(entries_frame, textvariable=contact, width=30)
txCnt.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

# Address
lbAdd = ttk.Label(entries_frame, text="Address")
lbAdd.grid(row=3, column=2, padx=20, pady=10, sticky="nsew")
txAdd = tk.Text(entries_frame, width=40, height=5)
txAdd.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

# Load your image using PIL
image = Image.open("ems.jpg")  # Replace "your_image.png" with your image file path
image = image.resize((200, 200))  # Resize the image if needed

# Convert the PIL image to a PhotoImage object (Tkinter-compatible)
tk_image = ImageTk.PhotoImage(image)

# Create a Label to display the image
image_label = tk.Label(root, image=tk_image)
image_label.place(x=1700, y=10)  # Adjust the coordinates to position the image as desired

df = pd.read_sql_query("SELECT * FROM Employee", conn)


def analyze_gender_distribution():
    # Ensure that 'df' is accessible within this function
    global df
    selected_gender = gender.get()
    print("Selected Gender:", selected_gender)  # Add this line for debugging
    df = pd.read_sql_query("SELECT * FROM Employee", conn)
    print("Data from Database:", df)
    # Calculate gender distribution, create pie chart, and display statistics
    total_employees = len(df)
    male_employees = len(df[df['gender'] == 'Male'])
    female_employees = len(df[df['gender'] == 'Female'])
    percentage_male = (male_employees / total_employees) * 100
    percentage_female = (female_employees / total_employees) * 100
    df['Gender Distribution'] = ''
    df.loc[df['gender'] == 'Male', 'Gender Distribution'] = 'Male'
    df.loc[df['gender'] == 'Female', 'Gender Distribution'] = 'Female'

    # Create a pie chart to visualize the gender distribution
    plt.figure(figsize=(6, 6))
    gender_distribution_counts = df['Gender Distribution'].value_counts()
    plt.pie(gender_distribution_counts, labels=gender_distribution_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Gender Distribution Among Employees')

    # Display gender distribution statistics
    gender_stats_text = f"Total Employees: {total_employees}\n" \
                        f"Male Employees: {male_employees} ({percentage_male:.2f}%)\n" \
                        f"Female Employees: {female_employees} ({percentage_female:.2f}%)"
    messagebox.showinfo("Gender Distribution Statistics", gender_stats_text)


# ... (The rest of your code for GUI setup)

# Create a button to trigger the gender distribution analysis
gender_analysis_button = tk.Button(entries_frame, text="Analyze Gender Distribution",
                                   command=analyze_gender_distribution,
                                   padx=10, pady=20, width=20, bg="cyan2", borderwidth=0)
gender_analysis_button.place(x=1400, y=100)

def count_employees_joined_after(doj_date):
    try:
        # Create or connect to the SQLite database (use your database name)
        conn = sqlite3.connect('Employee.db')
        cur = conn.cursor()

        # Define the SQL query to count employees who joined after the specified DOJ date
        query = f"SELECT COUNT(*) FROM Employee WHERE doj > '{doj_date}'"

        # Execute the query
        cur.execute(query)

        # Fetch the result
        count = cur.fetchone()[0]

        # Close the database connection
        conn.close()

        return count

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0  # Return 0 in case of an error


def calculate_tenure():
    # Get the Date of Joining (DOJ) from the form
    doj_text = doj.get()

    # Check if the DOJ field is empty
    if not doj_text:
        messagebox.showwarning("Tenure Calculation", "Please enter the Date of Joining.")
        return

    try:
        # Call the count_employees_joined_after function to get the count
        employees_count = count_employees_joined_after(doj_text)

        # Display the count of employees who joined after the specified DOJ date in a messagebox
        result_message = f"Number of employees who joined after {doj_text}:  {employees_count}"
        messagebox.showinfo("Employee Count", result_message)

    except ValueError:
        messagebox.showerror("Date Error", "Please enter a valid Date of Joining in the format YYYY-MM-DD.")


# ... (The rest of your GUI setup and code)


tenure_button = tk.Button(entries_frame, text="Calculate Tenure", command=calculate_tenure,
                          padx=10, pady=20, bg="thistle1", borderwidth=0,width=20)
tenure_button.place(x=1400,y=200)


def import_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if not file_path:
        return  # User canceled the file dialog

    try:
        # Read the selected CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path)

        # Create or connect to the SQLite database (use your database name)
        conn = sqlite3.connect('Employee.db')

        # Get the list of columns in the DataFrame
        columns = df.columns.tolist()

        # Create a table in the database with the same column names as in the CSV file
        create_table_sql = f"CREATE TABLE IF NOT EXISTS Employee ({', '.join([f'{col} TEXT' for col in columns])})"
        conn.execute(create_table_sql)

        # Insert the data from the DataFrame into the "Employee" table
        df.to_sql('Employee', conn, if_exists='append', index=False)

        conn.commit()
        conn.close()
        displayAll()
        messagebox.showinfo("CSV Import", "Data imported successfully.")

    except FileNotFoundError:
        messagebox.showerror("CSV Import Error", f"File not found: {file_path}")
    except Exception as e:
        messagebox.showerror("CSV Import Error", f"An error occurred: {str(e)}")


# Create a button for importing CSV data
import_csv_button = ttk.Button(entries_frame, text="Import CSV Data", command=import_csv_file)
import_csv_button.place(x=1410,y=300)




def getData(event):
    select_row = tv.focus()
    data = tv.item(select_row)
    global row
    row = data["values"]

    if row and len(row) > 1:
        name.set(row[1])
        age.set(row[2])
        gender.set(row[3])
        email.set(row[4])
        doj.set(row[5])
        txAdd.delete(1.0, END)
        txAdd.insert(END, row[7])
        contact.set(row[6])
        username.set(row[8])
        password.set(row[9])
    else:
        # Handle the case where row doesn't contain the expected data
        messagebox.showerror("Error", "Selected row does not contain valid data")


# Create a label to display the message
message_label = tk.Label(entries_frame, text="", fg="violetred4", background="forestgreen", font=("cabiliri", 20))
message_label.grid(row=6, column=10, columnspan=4, rowspan=3, padx=20, pady=20, sticky="nsew")


# Function to center the message label
def center_message_label():
    x = (entries_frame.winfo_width() - message_label.winfo_reqwidth()) / 2
    y = (entries_frame.winfo_height() - message_label.winfo_reqheight()) / 2
    message_label.place(x=x, y=y)


# Modify the displayAll function
def displayAll():
    rows = db.Fetch()  # Fetch records from the database
    tv.delete(*tv.get_children())
    if not rows:  # Check if there are no records
        message_label.config(text="Empty !")  # Update the message label with "None"
    else:
        message_label.config(text="")  # Clear the message label
        for row in rows:
            tv.insert("", END, values=row)


message_frame = ttk.Frame(entries_frame)
message_frame.grid(row=5, column=5,  padx=10, pady=10)

# Create a label for the message
message_label = ttk.Label(message_frame, text="", font=("Arial", 20),foreground="firebrick4",borderwidth=2)
message_label.pack()

def update_db():
    try:
        if not all([txName.get(), txAge.get(), coGen.get(), txEmail.get(), txDoj.get(), txCnt.get(),
                    txAdd.get("1.0", "end-1c"), txuse.get(), txpas.get()]):
            messagebox.showerror("Error in input", "Please fill all the details")
            return

        # Get the currently selected row in the Treeview
        select_row = tv.focus()
        data = tv.item(select_row)
        selected_row = data["values"]

        # Get the address text from the Text widget
        address_text = txAdd.get("1.0", "end-1c")

        # Set each value individually based on the entry fields and ComboBox
        selected_row[1] = txName.get()
        selected_row[2] = txAge.get()
        selected_row[3] = coGen.get()
        selected_row[4] = txEmail.get()
        selected_row[5] = txDoj.get()
        selected_row[6] = txCnt.get()
        selected_row[7] = address_text
        selected_row[8] = txuse.get()
        selected_row[9] = txpas.get()

        # Update the Treeview with the modified values
        tv.item(select_row, values=selected_row)

        # Get the ID of the selected row
        selected_id = selected_row[0]

        # Update the record in the database
        db.Update(selected_id, txName.get(), txAge.get(), coGen.get(), txEmail.get(), txDoj.get(),
                  txCnt.get(), address_text, txuse.get(), txpas.get())

        messagebox.showinfo("Success", "Record updated")
        clear_db()
        displayAll()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred while updating the record: {str(e)}")


def add_db():
    try:
        if not all([txName.get(), txAge.get(), coGen.get(), txEmail.get(), txDoj.get(), txCnt.get(),
                    txAdd.get("1.0", "end-1c"), txuse.get(), txpas.get()]):
            messagebox.showerror("Error in input", "Please fill all the details")
            return

        # Get the address text from the Text widget
        address_text = txAdd.get("1.0", "end-1c")

        # Use the address_text variable when inserting into the database
        db.insert(txName.get(), txAge.get(), coGen.get(), txEmail.get(), txDoj.get(), txCnt.get(), address_text,
                  txuse.get(), txpas.get())

        messagebox.showinfo("Success", "Record inserted")
        clear_db()
        displayAll()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred while inserting the record: {str(e)}")


def delete_db():
    db.Delete(row[0])
    clear_db()
    displayAll()


def clear_db():
    name.set("")
    age.set("")
    gender.set("")
    email.set("")
    doj.set("")
    txAdd.delete(1.0, END)
    contact.set("")
    username.set("")
    password.set("")








# Creating a button frame
# Creating a button frame
btFrame = tk.Frame(entries_frame, bg="forestgreen", borderwidth=0)
btFrame.grid(row=7, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

btUpdate = tk.Button(btFrame, text="Update", command=update_db, padx=10, pady=20, width=15, bg="lightgreen",
                     borderwidth=0)
btUpdate.grid(row=0, column=0, padx=10)

btAdd = tk.Button(btFrame, text="Add", command=add_db, padx=10, pady=20, width=15, bg="gold", borderwidth=0)
btAdd.grid(row=0, column=1, padx=10)

btDelete = tk.Button(btFrame, text="Delete", command=delete_db, padx=10, pady=20, width=15, bg="red", borderwidth=0)
btDelete.grid(row=0, column=2, padx=10)

btClear = tk.Button(btFrame, text="Clear", command=clear_db, padx=10, pady=20, width=15, bg="grey", borderwidth=0)
btClear.grid(row=0, column=3, padx=10)

def refresh_data():
    # Clear the current data in the Treeview
    tv.delete(*tv.get_children())

    # Fetch and display the latest data from the database
    displayAll()


refresh_button = ttk.Button(btFrame, text="Refresh Data", command=refresh_data)
refresh_button.grid(row=0, column=4, padx=30, pady=10)
refresh_button.config(command=refresh_data)

# tabel formation frame
# Create a frame for the Treeview using grid
tree_frame = tk.Frame(root)
tree_frame.grid(row=8, column=0, sticky="nsew")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1, minsize=1500)

# Rest of your Treeview and styling configuration


# Create a style for the Treeview headings and rows
style = ttk.Style()
style.configure("mystyle.Treeview.Heading", background="red", font=('Arial', 15))
style.configure("mystyle.Treeview", font=('Arial', 13), rowheight=50)

# Create the Treeview widget with the configured style
tv = ttk.Treeview(tree_frame, columns=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), style="mystyle.Treeview")

tv.heading("1", text="ID", anchor="center")
tv.column("1", width=5, anchor="center")

tv.heading("2", text="NAME", anchor="center")
tv.column("2", width=10, anchor="center")

tv.heading("3", text="AGE", anchor="center")
tv.column("3", width=5, anchor="center")

tv.heading("4", text="GENDER", anchor="center")
tv.column("4", width=10, anchor="center")

tv.heading("5", text="EMAIL", anchor="center")
tv.column("5", width=10, anchor="center")

tv.heading("6", text="D.O.J", anchor="center")
tv.column("6", width=10, anchor="center")

tv.heading("7", text="CONTACT", anchor="center")
tv.column("7", width=10, anchor="center")

tv.heading("8", text="ADDRESS", anchor="center")
tv.column("8", width=10, anchor="center")

tv.heading("9", text="USERNAME", anchor="center")
tv.column("9", width=10, anchor="center")

tv.heading("10", text="PASSWORD", anchor="center")
tv.column("10", width=10, anchor="center")

tv['show'] = 'headings'
tv.grid(row=0, column=0, sticky="nsew")
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill="x")

displayAll()
root.mainloop()
