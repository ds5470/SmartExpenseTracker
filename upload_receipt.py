import os
import boto3
from dotenv import load_dotenv

load_dotenv()

def upload_to_s3(file_path, bucket_name, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    try:
        print(f"Uploading {file_path} to {bucket_name}...")
        s3_client.upload_file(file_path, bucket_name, object_name)
        print("✅ Upload Successful!")
        return True
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

# --- TO TEST THIS ---
# 1. Replace with your actual bucket name from the AWS Console
MY_BUCKET = "my-personal-receipts-2026" 
# 2. Put a test image in your project folder and put its name here
TEST_IMAGE = "starbucks_receipt.png" 

if __name__ == "__main__":
    upload_to_s3(TEST_IMAGE, MY_BUCKET)