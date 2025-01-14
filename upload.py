import argparse
import os

import boto3
from botocore.exceptions import NoCredentialsError


def upload_directory_to_s3(directory, bucket_name, s3_prefix=''):
    """
    Uploads a file to an S3 bucket.

    :param file_name: File to upload
    :param bucket_name: S3 bucket name
    :param object_name: S3 object name (optional)
    :return: True if upload was successful, else False
    """
    # Initate S3 client
    s3 = boto3.client('s3')

    for root, _, files in os.walk(directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, directory)
            s3_object_path = os.path.join(s3_prefix, relative_path).replace('\\', '/')

            try:
                s3.upload_file(local_path, bucket_name, s3_object_path)
                print(f'Uploaded {local_path} to {bucket_name}/{s3_object_path}')
            except NoCredentialsError:
                print('AWS credentials not available.')
                return False
    print('Directory uploaded successfully.')
    return True


# Example usage:
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Upload a local directory to an S3 bucket.'
    )
    parser.add_argument('directory', help='Path to the local directory to upload.')
    bucket_name = 'aironworks-test-results'
    parser.add_argument(
        '--prefix',
        default='',
        help='Optional S3 prefix (e.g., folder path in the bucket).',
    )
    s3_prefix = 'playwright/test-results'  # Optional prefix
    args = parser.parse_args()

    upload_directory_to_s3(args.directory, bucket_name, args.prefix)
