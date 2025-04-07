# from flask import Flask, request, jsonify
# import sqlite3
# import datetime

# app = Flask(__name__)
# DB_FILE = 'expenses.db'

# def init_db():
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute('''
#                    CREATE TABLE IF NOT EXISTS expenses (
#                    expense_id INTEGER PRIMARY KEY AUTOINCREMENT, 
#                    date TEXT, 
#                    name TEXT,
#                    amount REAL,
#                    category TEXT
#                    )
#                    ''')
#     conn.commit()
#     conn.close()

# @app.route('/add_expense', methods=['POST'])
# def add_expense():
#     data = request.json
#     date = data.get('date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     name = data['name']
#     amount = data['amount']
#     category = data.get('category', 'General')  # Default category

#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO expenses (date, name, amount, category) VALUES (?, ?, ?, ?)", (date, name, amount, category))
#     conn.commit()
#     conn.close()
#     return jsonify({"message": "Expense added successfully!"}), 201

# @app.route('/view_expenses', methods=['GET'])
# def view_expenses():
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM expenses")
#     rows = cursor.fetchall()
#     conn.close()

#     expenses = [{"expense_id": row[0], "date": row[1], "name": row[2], "amount": row[3], "category": row[4]} for row in rows]
#     return jsonify(expenses), 200

# @app.route('/delete_expense/<int:expense_id>', methods=['DELETE'])
# def delete_expense(expense_id):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
#     conn.commit()
#     conn.close()
#     return jsonify({"message": "Expense deleted successfully!"}), 200

# @app.route('/update_category', methods=['PUT'])
# def update_category():
#     data = request.json
#     expense_id = data['expense_id']
#     category = data['category']

#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("UPDATE expenses SET category = ? WHERE expense_id = ?", (category, expense_id))
#     conn.commit()
#     conn.close()
#     return jsonify({"message": "Category updated successfully!"}), 200

# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)