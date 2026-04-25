import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def export_data():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="my_expense_tracker"
    )

    query = """
    SELECT 
        id,
        store_name,
        transaction_date,
        amount,
        category,
        confidence_score
    FROM expenses
    """

    df = pd.read_sql(query, conn)

    df.to_csv("/Users/dewansharma/Documents/SmartExpenseTracker/expenses_csv/expenses.csv", index=False)
    
    
    print("------------------------------------------------------------------------------------------")
    category_query = """
    SELECT category, SUM(amount) as total_spent
    FROM expenses
    GROUP BY category
    """

    df_cat = pd.read_sql(category_query, conn)
    df_cat.to_csv("/Users/dewansharma/Documents/SmartExpenseTracker/expenses_csv/category_summary.csv", index=False)



    print("------------------------------------------------------------------------------------------")
    monthly_query = """
    SELECT 
        DATE_FORMAT(transaction_date, '%Y-%m') as month,
        category,
        SUM(amount) as total_spent
    FROM expenses
    GROUP BY month, category
    """

    df_month = pd.read_sql(monthly_query, conn)
    df_month.to_csv("/Users/dewansharma/Documents/SmartExpenseTracker/expenses_csv/monthly_trends.csv", index=False)



    print("------------------------------------------------------------------------------------------")
    
    conn.close()

    print("✅ All exports completed successfully")




if __name__ == "__main__":
    export_data()