### TENSIGHT_STOCK
import warnings
import os
import os.path
import boto3
from datetime import date
from cryptography.utils import CryptographyDeprecationWarning

# For Ignoring CryptographyDeprecationWarning
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=CryptographyDeprecationWarning)
    import paramiko


def getfile():
    """Get File from Linux Server to Local drive"""
    # Login Credentials
    hostname='ip address'
    username='username'
    password='password'

    # File locations
    source = 'source folder'
    destination = 'destination folder'

    # filename
    filename = date.today().strftime('%Y-%m-%d')+'-filename'
    fileformat = 'csv'
    filename = filename+'.'+fileformat

    # paramiko
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname,username=username, password=password)
    sftp_client=ssh_client.open_sftp()

    # Source and Destination directory
    s = source+'/'+filename
    d = os.path.join(destination,filename)

    # Check if file exits or Not in source location, If exists copy to the Destination Location
    try:
        sftp_client.stat(s)
        sftp_client.get(s,d)
        sftp_client.close()
        ssh_client.close()
    except:
        print('File Not Found')
    finally:
        print('Transfer File Completed')


def upload_s3():
    """Uploading the data from local system to S3 Bucket"""
    # Boto3 instance
    s3 = boto3.resource('s3')
    bucketname = 'bucket name'
    destination = 'folder name'

    # filename
    filename = date.today().strftime('%Y-%m-%d')+'filename'
    fileformat = 'csv'
    filename = filename+'.'+fileformat

    # File Path 
    spath = 'file path'
    os.chdir(spath)
    source = os.path.join(spath,filename)
    destination = destination+'/'+filename

    print(source)
    print(os.path.exists(source))

    # Check if file exits or Not in source location, If exists copy to the S3 Bucket
    try:
        if os.path.exists(filename):
            s3.meta.client.upload_file(source,bucketname,destination)
    except:
        print('File Not Found')
    finally:
        print('Completed')
        os.chdir('..')
    

# Function Call
getfile()
upload_s3()