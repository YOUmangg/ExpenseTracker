import datetime
import sqlite3
from ai import send_query_date_extract, tell_class
import time
import matplotlib.pyplot as plt
import seaborn as sns
from ExpensesController import *


def main():
    init_db()
    
    while True:
        print("\nWhat do you want to do?")
        print('1. Add new expense')
        print('2. View all expenses')
        print('3. Explore your expenditure')
        print('4. Delete an expense')
        print('5. Export expenses to CSV')
        print('6. Exit')

        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            input_date_choice = input('Do you want to enter a custom date and time for the transaction? (Yes / No) \n')
            if(input_date_choice.lower() == "yes"):
                input_date = str(input('Enter the date and time: '))
                date = send_query_date_extract(content = input_date)
                print(date)
            name = input("Name of the expense: ")
            amount = int(input("Enter the amount you want to add: "))
            add_expense(date, name, amount)
            print("Expense added successfully!")
            time.sleep(1)
            
        elif choice == 2:
            view_expenses()
            time.sleep(2)

        elif choice == 3:
            # Placeholder for future exploration logic
            print("Which one of the following graphs would you like to see?")
            print("1. Monthly Exploration \n2. Weekly Exploration \n3. Daily Exploration \n4. Class Exploration")
            exp_choice = int(input())
            if(exp_choice == 1):
                monthly_exploration()
            elif(exp_choice == 3):
                daily_view()
            elif(exp_choice == 4):
                plot_expense_distribution()
        elif choice == 4:
            delete_expense()
            time.sleep(1)

        elif choice == 5:
            export_expenses_to_csv()
            time.sleep(1)
        elif choice == 6:
            print('Thank you for using the Expense Tracker! Saving your details...')
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

