import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def generate_weekly_summary(): 
    # query DB
    # send to LLM


    pass


def get_total_by_vendor(vendor_name):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=os.getenv('DB_PASSWORD'),
        database="my_expense_tracker"
    )
    cursor = conn.cursor()

    # SQL logic to sum all expenses for a specific store
    query = "SELECT category, SUM(amount) AS total_amount FROM expenses WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) GROUP BY category; %s"

    cursor.execute(query, (f"%{vendor_name}%",))
    
    result = cursor.fetchall()
    
    print(f"--- 📊 Spending Report ---")
    print(f"Total spent at {vendor_name}: ${result if result else 0.00}")
    
    cursor.close()
    conn.close()



if __name__ == "__main__":
    get_total_by_vendor("Starbucks")