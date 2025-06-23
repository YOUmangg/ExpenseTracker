import sqlite3
import datetime
import sqlite3
from ai import send_query_date_extract, tell_class
import time
import matplotlib.pyplot as plt
import seaborn as sns

DB_FILE = 'expenses.db'

classes = ['Travel', 'Food', 'Beverage', 'Home Food Essentials', 'Rent', 'Cook', 'Bills', 'Clothing', 'Home 1', 'Enjoyment', 'Gifts', 'Tips']

def add_column(column_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if the column already exists
    cursor.execute("PRAGMA table_info(expenses)")
    columns = [col[1] for col in cursor.fetchall()]
    if column_name in columns:
        # If the column already exists, print a message and return
        print(f"Column '{column_name}' already exists in the expenses table.")
        conn.close()
        return
    # Add the new column
    print(f"Adding column '{column_name}' to the expenses table...")
    cursor.execute(f"ALTER TABLE expenses ADD COLUMN {column_name} TEXT DEFAULT 'Enjoyment'")
    conn.commit()
    conn.close()
    print("Column 'category' added successfully!")

# add_column('category')  # Uncomment this line to execute the column addition

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS expenses (
                   expense_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   date TEXT, 
                   name TEXT,
                   amount INTEGER,
                   category TEXT DEFAULT 'Enjoyment')  -- Default category set to 'Enjoyment'
                   ''')
    conn.commit()
    conn.close()

def update_category_for_existing_rows():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Update the 'category' column for existing rows
    cursor.execute("UPDATE expenses SET category = 'Enjoyment' WHERE name LIKE '%Yellow%' ")
    conn.commit()
    conn.close()
    print(f"Updated 'category' column for existing rows.")

# update_category_for_existing_rows()  # Uncomment this line to execute the update

def add_expense(date, name, amount):
    conn = sqlite3.connect(DB_FILE)
    expense_class = tell_class(name, classes)
    if(expense_class not in classes):
        classes.append(expense_class)
    cursor = conn.cursor()
    print(expense_class)
    cursor.execute("INSERT INTO expenses (date, name, amount, category) VALUES (?, ?, ?, ?)", (date, name, amount, expense_class))
    conn.commit()
    conn.close()

def view_expenses():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    
    total_expense = 0
    for row in rows:
        print(f'Date: {row[1]}, Name: {row[2]}, Amount: {row[3]}, Category: {row[4]}')
        total_expense += row[3]
        
    print('Total expense = ', total_expense)
    conn.close()

def daily_view():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    
    total_expense = 0
    dict_datenametotal = {}
    for row in rows:
        row_name = row[1].split()[0]
        # Initialize the list for new date keys
        if row_name not in dict_datenametotal:
            dict_datenametotal[row_name] = []
        
        dict_datenametotal[row_name].append([row[2], row[3]]) #name, amount list
        print(f'Date: {row_name}, Name: {row[2]}, Amount: {row[3]}')
        total_expense += row[3]
    
    conn.close()

    final_dict = {} 

    #create another dict with one key value pair
    for key in dict_datenametotal.keys():
        total_val = 0
        name = ""

        for val in dict_datenametotal[key]:
            name += "_" + val[0]
            total_val += val[1]
        
        final_dict[key + '_' + name] = total_val
    
    #Plot creation
    plt.figure(figsize=(12, 6))  # Adjusted figure size for better aesthetics
    sns.barplot(x = list(final_dict.keys()), y = [final_dict[key] for key in final_dict.keys()])
    
    # Beautifying the plot
    plt.title('Monthly Expense Overview', fontsize=16)  # Adding a title
    plt.xlabel('Date', fontsize=14)  # Label for x-axis
    plt.ylabel('Total Amount', fontsize=14)  # Label for y-axis
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(axis='y')  #grid lines for better readability
    
    plt.show()
                
    # Create another dict with one key value pair
    for key in dict_datenametotal.keys():
        total_val = 0
        name = ""
        # Only keep the date part in the key
        date_part = key.split('_')[0]  # Get the date part
        for val in dict_datenametotal[key]:
            name += "_" + val[0]
            total_val += val[1]
        
        final_dict[date_part + '_' + name] = total_val  # date_part as key
    
    #Plot monthly view
    return dict_datenametotal #Check why I am returning this

def plot_expense_distribution():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()
    
    categories = [row[0] for row in rows]
    amounts = [row[1] for row in rows]

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    
    conn.close()

# Call the function to plot the pie chart
# plot_expense_distribution()  # Uncomment this line to execute the pie chart plotting

def monthly_exploration():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Prompt user for the month and year
    month = int(input("Enter the month (1-12) you want to explore: "))
    year = int(input("Enter the year (YYYY) you want to explore: "))
    
    # Fetch expenses for the selected month and year
    cursor.execute("SELECT * FROM expenses WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?", (str(year), f"{month:02}"))
    rows = cursor.fetchall()
    
    if not rows:
        print("No expenses found for the selected month and year.")
        conn.close()
        return
    
    total_expense = 0
    expense_dict = {}
    
    for row in rows:
        print(f'Date: {row[1]}, Name: {row[2]}, Amount: {row[3]}, Category: {row[4]}')
        total_expense += row[3]
        
        # Aggregate expenses by name
        if row[2] in expense_dict:
            expense_dict[row[2]] += row[3]
        else:
            expense_dict[row[2]] = row[3]
    
    print('Total expense for {}/{} = {}'.format(month, year, total_expense))
    
    # Plotting the expenses
    plt.figure(figsize=(12, 6))
    plt.bar(expense_dict.keys(), expense_dict.values(), color='skyblue')
    
    # Beautifying the plot
    plt.title(f'Expenses for {month}/{year}', fontsize=16)
    plt.xlabel('Expense Name', fontsize=14)
    plt.ylabel('Amount', fontsize=14)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(axis='y')  # Add grid lines for better readability
    
    plt.show()
    
    conn.close()

# Call the function to explore monthly expenses
# monthly_exploration()  # Uncomment this line to execute the monthly exploration

def delete_expense():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # First show all expenses with IDs
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    
    if not rows:
        print("No expenses to delete!")
        conn.close()
        return
        
    print("\nCurrent Expenses:")
    print("ID | Date | Name | Amount")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
    
    print("\nEnter -1 to delete all expenses")
    print("Enter 0 to cancel")
    print("Or enter the ID of the expense to delete")
    
    # Get expense ID to delete
    try:
        expense_id = int(input("Your choice: "))
        if expense_id == 0:
            print("Deletion cancelled.")
            conn.close()
            return
        
        # Delete all expenses
        if expense_id == -1:
            confirm = input("Are you sure you want to delete ALL expenses? This cannot be undone! (yes/no): ")
            if confirm.lower() == 'yes':
                print("Deleting all expenses...")
                cursor.execute("DELETE FROM expenses") 
                conn.commit()
                print("All expenses deleted successfully!")
            else:
                print("Deletion cancelled.")
            conn.close()
            return
            
        # Check if ID exists
        cursor.execute("SELECT * FROM expenses WHERE expense_id = ?", (expense_id,))
        if not cursor.fetchone():
            print("Invalid expense ID!")
            conn.close()
            return
            
        # Confirm deletion of single expense
        confirm = input(f"Are you sure you want to delete expense ID {expense_id}? (yes/no): ")
        if confirm.lower() == 'yes':
            cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
            conn.commit()
            print("Expense deleted successfully!")
        else:
            print("Deletion cancelled.")
            
    except ValueError:
        print("Please enter a valid number!")
    finally:
        conn.close()

def export_expenses_to_csv():
    import csv
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    
    with open('expenses.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Expense ID', 'Date', 'Name', 'Amount', 'Category'])
        csv_writer.writerows(rows)
    
    conn.close()
    print("Expenses exported to expenses.csv successfully!")
