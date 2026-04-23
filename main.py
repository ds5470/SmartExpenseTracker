import sys
import os
from upload_receipt import upload_to_s3
from llm_processor import get_category_from_llm
from clean_and_analyze import extract_and_clean
from save_to_db import save_expense_to_db
from llm_processor import enrich_expense

def run_pipeline(local_file_path):
    BUCKET_NAME = "my-personal-receipts-2026" # Replace with yours
    
    # Step 1: Upload to S3
    print(f"\n--- Step 1: Uploading {local_file_path} ---")
    success = upload_to_s3(local_file_path, BUCKET_NAME)
    if not success: return

    # Step 2: Extract & Clean with AI
    print("\n--- Step 2: Analyzing with AWS Textract AI ---")
    # We use the filename as the 'key' in S3
    s3_key = os.path.basename(local_file_path)
    vendor, date, total = extract_and_clean(BUCKET_NAME, s3_key)
    category = get_category_from_llm(vendor, total)

    # parse JSON
    category = get_category_from_llm()


    # Step 3: Save to MySQL
    print("\n--- Step 3: Saving to Local Database ---")
    save_expense_to_db(vendor, date, total, category)

    # save_expense_to_db(vendor, date, total, 99.0) # Using 99 as a placeholder confidence
    
    print("\n✅ Project Execution Complete! Check your MySQL table.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_receipt_image>")
    else:
        run_pipeline(sys.argv[1])