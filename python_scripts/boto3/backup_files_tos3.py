import logging
import boto3
import s3fs
import os
import os.path
from botocore.exceptions import ClientError
import time
import datetime

s3_client = boto3.client('s3')
s3_client_fs = s3fs.S3FileSystem(anon=False)
bucket_names = []


def bucket_status(bucket_name):
    """To Get the List of Buckets"""
    bucket_response = s3_client.list_buckets()
    buckets = bucket_response['Buckets']
    for bucket in buckets:
        bucket_names.append(bucket['Name'])
    return bucket_names


def add_policy(bucket_name):
    """Update Bucket Policy as Not accessable from all IP's"""
    s3_client = boto3.client('s3')
    s3_client.put_public_access_block(
         Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': False
                }
    )

def create_bucket(bucket_name, region=None):
    """Check Bucket already exits or if not create new Bucket"""
    bucket_status(bucket_name)
    try:
        if bucket_name in bucket_names:
            print('already exists')
        elif region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
            add_policy(bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'locationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration = location)
            add_policy(bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def put_files(file_path,bucket_name,object_name=None):
    """Upload files from Local to S3 Bucket"""
    s3_client = boto3.client('s3')
    if object_name is None:
        object_name=os.path.basename(file_path)
    try:
        response = s3_client.upload_file(file_path,bucket_name,object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

"""To Get the List Bucket name that need to be created"""
folders = []
dest = 'Destination Directory'
os.chdir(dest)
for f in os.listdir(dest):
        folders.append(f)

"""Bucket creation"""
for bucket in folders:
    create_bucket(bucket)


"""To set the fileruntime"""
pdate = datetime.datetime.strftime((datetime.datetime.now()),'%Y-%m-%d')
pdate_str = datetime.datetime.strptime(pdate,'%Y-%m-%d')
pdate1 = (pdate_str - datetime.timedelta(days=1))
pdate1_str = datetime.datetime.strftime(pdate1,'%Y-%m-%d')
pdate_time = '11:59'
rtime = pdate1_str+' '+pdate_time
lm_time = datetime.datetime.strptime(rtime,'%Y-%m-%d %H:%M')


## Upload the files, which are only modified and which doesn't exist
for f in folders:
    x=os.path.abspath(f)
    for i,j,k in os.walk(x):
        bname = f
        for file in k:
            x=(time.ctime(os.path.getmtime(os.path.join(os.path.relpath(i, dest), file))))
            ftime = (datetime.datetime.strptime(x,'%a %b %d %H:%M:%S %Y'))
            if not s3_client_fs.exists(bname+'/'+'/'.join((os.path.join(os.path.relpath(i, dest), file)).split('\\')[1:])):
                put_files(((os.path.join(os.path.relpath(i, dest), file))),bname,'/'.join((os.path.join(os.path.relpath(i, dest), file)).split('\\')[1:]))
            elif (ftime > lm_time):
                put_files(((os.path.join(os.path.relpath(i, dest), file))),bname,'/'.join((os.path.join(os.path.relpath(i, dest), file)).split('\\')[1:]))
            else:
                pass