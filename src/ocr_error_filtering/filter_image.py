import os
import pandas as pd
import boto3


def setup_s3_client():
    """ Set up AWS S3 client using boto3 with environment credentials. """
    return boto3.client('s3')

def list_s3_objects(s3_client, bucket_name, prefix=''):
    """ List objects in an S3 bucket directory specified by prefix. """
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        return [item['Key'] for item in response['Contents']]
    return []

def copy_images_within_s3(s3_client, bucket_name, source_prefix, destination_prefix, page_id_to_batch):
    """
    Copy specified images from one directory to another within the same AWS S3 bucket based on a mapping of page IDs to batch folders.

    Parameters:
    - s3_client: Initialized S3 client object.
    - bucket_name (str): Name of the AWS S3 bucket.
    - source_prefix (str): Source directory prefix in the bucket.
    - destination_prefix (str): Destination directory prefix in the bucket.
    - page_id_to_batch (dict): Mapping of page IDs to their corresponding batch folders.
    """
    for page_id, batches in page_id_to_batch.items():
        for batch in batches:
            batch_prefix = f"{source_prefix}{batch}/"  # Source folder
            objects = list_s3_objects(s3_client, bucket_name, batch_prefix)
            for obj_key in objects:
                image_id = obj_key.split('/')[-1].split('_')[0]
                if image_id == page_id:
                    destination_key = f"{destination_prefix}{obj_key.split('/')[-1]}"
                    # Copy the image to the new location within the same bucket
                    s3_client.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': obj_key}, Key=destination_key)
                    #s3_client.delete_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': obj_key}, Key=destination_key)

                    print(f"Copied {obj_key} to {destination_key}")
