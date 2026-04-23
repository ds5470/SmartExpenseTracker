import os, boto3, re
from dotenv import load_dotenv
from dateutil import parser
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
 
def clean_data(raw_date, raw_total):
    # 1. Clean the Date: Transforms "OCT. 26, 2023" -> "2023-10-26"
    clean_date = parser.parse(raw_date).strftime('%Y-%m-%d')
    
    # 2. Clean the Total: Removes "$" and other non-numeric symbols
    clean_total = re.sub(r'[^\d.]', '', raw_total)
    
    return clean_date, clean_total

def extract_and_clean(bucket, file):
    client = boto3.client(
        'textract',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    
    response = client.analyze_expense(
        Document={'S3Object': {'Bucket': bucket, 'Name': file}}
    )

    extracted = {'vendor': 'Unknown', 
        'total': '0.00', 
        'date': 'Jan 1, 1900'}
    for doc in response['ExpenseDocuments']:
        for field in doc['SummaryFields']:
            f_type = field['Type']['Text']
            f_val = field.get('ValueDetection', {}).get('Text', '0.00')
            
            if f_type == 'VENDOR_NAME': 
                extracted['vendor'] = f_val
            elif f_type in ['TOTAL', 'AMOUNT_PAID', 'RECEIPT_TOTAL', 'SUBTOTAL']: 
                # Adding extra possible labels for 'total'
                extracted['total'] = f_val
            elif f_type in ['INVOICE_RECEIPT_DATE', 'DATE']: 
                extracted['date'] = f_val
    
    final_date, final_total = clean_data(extracted['date'], extracted['total'])
    print(f"--- Cleaned Data for SQL ---")
    print(f"Store: {extracted['vendor']}")
    print(f"Date:  {final_date}")
    print(f"Total: {final_total}")
    
    return extracted['vendor'], final_date, final_total



if __name__ == "__main__":
    extract_and_clean("your-bucket-name", "receipt.jpg")