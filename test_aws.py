import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError 

# 1. Load your .env file
# Ensure .env is in the same folder as this script
load_dotenv()

def verify_aws_mac():
    # 2. Extract keys from environment
    access_key = os.getenv('AWS_ACCESS_KEY')
    secret_key = os.getenv('AWS_SECRET_KEY')
    region = os.getenv('AWS_REGION', 'us-east-1')

    print("--- Mac AWS Connection Test ---")
    
    if not access_key or not secret_key:
        print("❌ Error: Could not find AWS keys in your .env file.")
        return

    try:
        # 3. Initialize the AWS Session
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        
        # 4. Verify identity with STS
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ Success! Your Mac is talking to AWS as: {identity['Arn']}")

    except ClientError as e:
        print(f"❌ AWS Connection Failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    verify_aws_mac()