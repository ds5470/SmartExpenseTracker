AI-Powered Smart Expense Tracker
A modular Python-based pipeline that automates the transition from physical receipts to structured database records using AWS Cloud AI and MySQL.

🚀 Features
Automated Cloud Upload: Programmatically handles receipt storage in Amazon S3.

Intelligent Extraction: Leverages AWS Textract (AnalyzeExpense API) to perform OCR and entity extraction for vendor names, dates, and totals.

Data Sanitization: Cleans raw AI text (e.g., stripping '$' and formatting dates) into SQL-compatible formats using Python.

Relational Storage: Stores normalized financial records in a MySQL database for long-term tracking.

🛠 Tech Stack
Language: Python 3.10+

Cloud: AWS (S3, Textract, IAM)

Database: MySQL

Libraries: boto3, mysql-connector-python, python-dotenv, python-dateutil

📋 Setup & Launch Instructions
1. Environment Configuration
Create a .env file in the root directory and populate it with your credentials:

Code snippet

AWS_ACCESS_KEY=your_access_key
AWS_SECRET_KEY=your_secret_key
AWS_REGION=us-east-1
DB_PASSWORD=your_mysql_password
2. Database Initialization
Ensure your MySQL server is running and create the table:
/usr/local/mysql/bin/mysql -u root -p

SQL

CREATE DATABASE my_expense_tracker;
USE my_expense_tracker;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_date DATE NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    confidence_score FLOAT
    category VARCHAR(50),
    summary TEXT
);
3. Running the Pipeline
Activate your virtual environment and run the master script with your receipt image:

Bash

source venv/bin/activate
python3 main.py <your_receipt_image.jpg>
🏗 Project Structure
main.py: The orchestrator script managing the end-to-end flow.

upload_receipt.py: Handles AWS S3 communication.

clean_and_analyze.py: Processes AWS Textract responses and sanitizes data.

save_to_db.py: Manages MySQL connection and data insertion.