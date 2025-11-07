def ask_yes_no(question):
    confirm = input(question)
    while True:
        if confirm not in ('Y', 'n', 'yes', 'no'):
            confirm = input('Please enter either "yes" or "no": ')
            continue
        if confirm in ('Y', 'yes'):
            return True
        else:
            return False


def load_s3_files_list(bucket_name):
    """
    Load a set of all file keys from an S3 bucket.

    Args:
        bucket_name: Name of the S3 bucket

    Returns:
        set: A set containing all file keys in the bucket
    """
    from boto.s3.connection import Bucket

    from pola.s3 import create_s3_connection

    conn = create_s3_connection()
    bucket = Bucket(conn, name=bucket_name)

    s3_files = set()
    for key in bucket.list():
        s3_files.add(key.name)

    return s3_files
