# AI-Powered Expense Tracker

An end-to-end intelligent expense tracking system that extracts data from receipts using AWS Textract, processes it with Python, and visualizes insights using Tableau.

---

## Features

* Automated receipt data extraction using AWS Textract (Expense API)
* Intelligent expense categorization using LLM
* Cloud storage using AWS S3
* Structured storage in MySQL database
* Interactive Tableau dashboard for insights, including a category-based pie chart similar to what Chase Bank uses in its app to help users quickly understand spending distribution
* Dark-theme visualization for better UX

---

## Architecture

Receipt Image → AWS S3 → AWS Textract → Python Processing → MySQL → Tableau Dashboard

---

## Tech Stack

* **Backend:** Python, Boto3
* **Cloud:** AWS S3, AWS Textract
* **Database:** MySQL
* **AI/NLP:** LLM-based categorization
* **Visualization:** Tableau

---

## Dashboard Insights

* Spending by category
* Monthly spending trends
* Top merchants analysis
* Interactive filters and drill-down

---

## How It Works

1. Upload receipt images to AWS S3, where they are securely stored and made available for processing by downstream services.
2. Textract extracts structured expense data by analyzing the receipt image and identifying key fields such as total amount, merchant name, and line items.
3. Python processes and cleans data by normalizing formats, removing inconsistencies, and preparing it for storage and analysis.
4. LLM categorizes transactions by interpreting merchant names and context to assign each expense to a meaningful category like food, travel, or shopping.
5. Data stored in MySQL, allowing efficient querying and structured access for analytics and visualization.
6. Tableau visualizes insights through interactive dashboards, including charts and a pie chart similar to modern banking apps like Chase, helping users easily understand spending patterns.

---

## Screenshots

<img width="2700" height="1704" alt="image" src="https://github.com/user-attachments/assets/b6904d06-bc3c-4f66-81bb-bf8515f115c1" />


---

## Future Improvements

* Real-time expense tracking UI
* Mobile app integration
* Budget prediction using ML
* Expense anomaly detection

---

## 📌 Author

Your Name
