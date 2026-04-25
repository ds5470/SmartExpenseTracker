from datetime import datetime
import os
import boto3
import mysql.connector 
from dotenv import load_dotenv
from analyze_receipt import extract_receipt_data
from llm_processor import get_category_from_llm
from dateutil import parser
import re

GREEN = "\033[92m"
RESET = "\033[0m"

load_dotenv()
skipped = 0
inserted = 0
processed = 0

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# file_name = "r1.png"

bucket_name = "my-personal-receipts-2026"

response = s3.list_objects_v2(Bucket=bucket_name)

count = len(response.get("Contents", []))

print("Number of objects:", count)
print("--------------------------------------------------------------------------")
print()
print()
print()



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
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print(f"{GREEN}**************************************************************************{RESET}")
        print()
        print()
        print()

        


    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



# Check on all the files
for obj in response.get("Contents", []):
    file_name = obj["Key"]
    print("")
    print(f"{GREEN}**************************************************************************{RESET}")

    data = extract_receipt_data(bucket_name, file_name)
    
    
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(f"📄 Processing: {file_name}")
    processed += 1
    


    
    if not data:
            print("❌ Skipped: No Textract data")
            print()
            print()
            skipped += 1
            continue
    
    
    total = (
        data.get("TOTAL", {}).get("value") or
        data.get("DEBIT_CARD", {}).get("value") or
        data.get("AMOUNT_PAID", {}).get("value") or
        data.get("SUBTOTAL", {}).get("value")
    )
    # print("🔍 Extracted fields:", data)


    if total:
        total = float(re.sub(r'[^\d.]', '', total))
    
    date = data.get("INVOICE_RECEIPT_DATE", {}).get("value")
    if date:
        import re
        date = re.sub(r'\.', '', date)   # remove "OCT."
        date = parser.parse(date).strftime('%Y-%m-%d')
    else:
        date = "1970-01-01"   # or continue if you prefer


    vendor = data.get("VENDOR_NAME", {}).get("value")
    if not vendor or vendor == "0" or len(vendor.strip()) < 2:
        print(f"❌ Bad vendor for {file_name}, ⚠️ Vendor issue → using 'Unknown'")
        vendor = "Unknown"

    if not total:
        print("❌ Skipped: Missing TOTAL")
        skipped += 1
        continue

    if not date:
        print("❌ Skipped: Missing DATE")
        skipped += 1
        continue

    vendor = " ".join(vendor.split())   # fixes weird spacing like "H ULTA BEAUT Y"
    vendor = vendor.replace("®", "")
    vendor = vendor.strip().title() 
    
    
    
    vendor_conf = data.get("VENDOR_NAME", {}).get("confidence")

    category = get_category_from_llm(vendor, total)    

    inserted += 1

    save_expense_to_db(vendor, date, total, category, vendor_conf)


print()
print(f"✅ Inserted: {inserted}")
print()
print(f"⚠️ Skipped: {skipped}")

# --- TEST IT ---
# if __name__ == "__main__":
    # Example clean data (use the output from your previous script)
    # save_expense_to_db(vendor, date, total, vendor_conf)