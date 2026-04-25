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

    results = {}
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
                    print(f"{field_type}: {value} ({confidence:.2f}% confidence)")
                    results[field_type] = {
                        "value": value,
                        "confidence": confidence
                    }
            return results

    except Exception as e:
        print(f"❌ Error during AI analysis: {e}")
        return []

# --- TEST IT ---
MY_BUCKET = "my-personal-receipts-2026"
# MY_FILE = "starbucks_receipt.png" # The name of the file already in S3

def analyze_all_receipts():
    folder_path = '/Users/dewansharma/Documents/SmartExpenseTracker/receipts'
    folder_list = os.listdir(folder_path)
    # print(folder_len)

    for i in range(1, len(folder_list) + 2):
        try:
            MY_FILE = "r" + str(i) + '.png'
            # print(MY_FILE)
            extract_receipt_data(MY_BUCKET, MY_FILE)
            print("✅ Image analyzed : r" + str(i) + ".png sucessfully")
            print()
        except Exception:
            print("❌ Error occured")
    print("✅ Analyzed all receipts sucessfully")

if __name__ == "__main__":
    # extract_receipt_data(MY_BUCKET, MY_FILE)
    analyze_all_receipts()