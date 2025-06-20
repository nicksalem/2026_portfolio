import boto3
import pandas as pd
import numpy as np
from io import StringIO
import os


def writeDF (access_file=None,bucket_name = None, object_key=None, df=None):

    access = pd.read_csv(access_file) #type:ignore
              
    aws_access_key_id= access['Access key ID'][0]
    aws_secret_access_key = access['Secret access key'][0]

    region_name = 'us-east-1'  # Change if needed
     # Step 2: Connect to S3 with your credentials
    s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    # String IO is used to store the data in memory, RAM, and not on disk
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False) #type:ignore

    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=csv_buffer.getvalue()
    )

    print(f"✅ Uploaded CSV to s3://{bucket_name}/{object_key}")