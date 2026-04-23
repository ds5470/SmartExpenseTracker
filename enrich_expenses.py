import mysql.connector
import os
from dotenv import load_dotenv
from llm_processor import get_category_from_llm

load_dotenv()

# connect to DB
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=os.getenv('DB_PASSWORD'),
    database="my_expense_tracker"
)

cursor = connection.cursor()

# fetch uncategorized rows
cursor.execute("""
    SELECT id, store_name, amount 
    FROM expenses 
    WHERE category IS NULL
""")

rows = cursor.fetchall()

for row in rows:
    expense_id, name, amount = row

    # skip bad data
    if name == "0" or not name.strip():
        continue

    category = get_category_from_llm(name, amount)

    cursor.execute(
        "UPDATE expenses SET category = %s WHERE id = %s",
        (category, expense_id)
    )

connection.commit()

cursor.close()
connection.close()

print("✅ Existing expenses updated!")