import os
import mysql.connector 
from dotenv import load_dotenv

load_dotenv()

def save_expense_to_db(vendor, date, total, category, confidence):
    try:
        # 1. Establish the connection to your local MySQL
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=os.getenv('DB_PASSWORD'),
            database="my_expense_tracker"
        )
        cursor = conn.cursor()

        # 2. Prepare the SQL command with placeholders
        # We use %s to safely handle strings, dates, and decimals
        sql = """
        INSERT INTO expenses 
        (store_name, transaction_date, amount, category, confidence_score)
        VALUES (%s, %s, %s, %s, %s)
        """
        # 3. Create a tuple with your variables
        val = (vendor, date, total, category, confidence)

        # 4. Execute and COMMIT (This actually saves the data!)
        cursor.execute(sql, val)
        conn.commit()

        print(f"🚀 Record inserted successfully! ID: {cursor.lastrowid}")


    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()




# --- TEST IT ---
# if __name__ == "__main__":
#     # Example clean data (use the output from your previous script)
#     save_expense_to_db("STARBUCKS COFFEE", "2023-10-26", 21.41, 99.8)