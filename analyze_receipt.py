import os
import boto3
from dotenv import load_dotenv

load_dotenv()

def extract_receipt_data(bucket_name, file_name):
    # Initialize Textract Client
    client = boto3.client(
        'textract',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    try:
        # Call the specialized Expense API 
        response = client.analyze_expense(
            Document={'S3Object': {'Bucket': bucket_name, 'Name': file_name}}
        )

        # Textract returns a list of 'ExpenseDocuments'
        for doc in response['ExpenseDocuments']:
            # We want 'SummaryFields' (Vendor, Total, Date)
            for field in doc['SummaryFields']:
                field_type = field['Type']['Text']
                value = field['ValueDetection']['Text']
                confidence = field['Type']['Confidence']

                # Only print the big 3 for now
                if field_type in ['VENDOR_NAME', 'TOTAL', 'INVOICE_RECEIPT_DATE']:
                    print(f"✅ {field_type}: {value} ({confidence:.2f}% confidence)")

    except Exception as e:
        print(f"❌ Error during AI analysis: {e}")

# --- TEST IT ---
MY_BUCKET = "my-personal-receipts-2026"
MY_FILE = "starbucks_receipt.png" # The name of the file already in S3

if __name__ == "__main__":
    extract_receipt_data(MY_BUCKET, MY_FILE)