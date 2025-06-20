import pandas as pd
import numpy as np
import boto3
from io import StringIO


def download_data(access_file: str, bucket: str, object_key: str, region: str) -> pd.DataFrame:
    """
    Loads in the data from an S3 bucket.

    Parameters:
        access_file (str): Path to the credentials CSV file.
        bucket (str): Name of the S3 bucket.
        object_key (str): Path to the object inside the bucket.
        region (str): AWS region name.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """

    if access_file is None:
        raise ValueError("access_file must be provided.")
    
    try:
        access = pd.read_csv(access_file)

        aws_access_key_id= access['Access key ID'][0]
        aws_secret_access_key = access['Secret access key'][0]

        region_name = region  # Change if needed

        # Step 2: S3 file details
        # bucket is defined in the function
        # object_key is defined in the function

        # Step 3: Connect to S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        # Step 4: Download the object (file) from S3
        response = s3.get_object(Bucket=bucket, Key=object_key)

        # Step 5: Convert the byte stream to a string, then to DataFrame
        csv_data = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))

        # Done! Use your DataFrame
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()
    
