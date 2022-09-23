# from fileinput import filename
from ftplib import FTP
import os
from datetime import datetime
import warnings
import os.path
from cryptography.utils import CryptographyDeprecationWarning
import pandas as pd

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=CryptographyDeprecationWarning)
    import paramiko

class InventoryView:
    # FTP Server
    ftp_ip = 'ftp ip address'
    ftp_userid = 'username'
    ftp_password = 'password'
    ftp_direc = 'ftp directory'
    
    # Local 
    local_direc = 'local directory'

    # Linux Server
    hostname = 'server ip'
    prod_username = 'username'
    prod_password = 'password'
    prod_direc = 'directory in linux server'

    def __init__(self,filename):
        self.filename = filename

    def ftp_download(self):
        ftp = FTP()
        ftp.connect(InventoryView.ftp_ip)
        ftp.login(InventoryView.ftp_userid,InventoryView.ftp_password)
        ftp.cwd(InventoryView.ftp_direc)
        d_location = os.path.join(InventoryView.local_direc, self.filename)
        
        with open(d_location,'wb') as file:
            ftp.retrbinary(f'RETR {self.filename}', file.write)
        ftp.quit()
        print('downloaded')

    def modifydata_StdSales(self):
        os.chdir(InventoryView.local_direc)

        try:
            df = pd.read_csv(self.filename)
        except:
            df = pd.read_csv(self.filename,engine='python', sep=r'"\s*,\s*"')

            list1 = []
            for i,j in enumerate(df.columns):
                list1.append(j.replace('"',''))

            df.columns=list1

            for i, j in  enumerate(df['column1']):
                df['column1'][i]=df['column1'][i].replace('"','')

            for i, j in  enumerate(df['column15']):
                df['column15'][i]=df['column15'][i].replace('"','')
        finally:
            df = df.drop(['column10','column11','column12'],axis=1)
            df.to_csv(self.filename, index=False)


    def modifydata_StdReturn(self):
        os.chdir(InventoryView.local_direc)

        try:
            df = pd.read_csv(self.filename)
        except:
            df = pd.read_csv(self.filename,engine='python', sep=r'"\s*,\s*"')

            list1 = []
            for i,j in enumerate(df.columns):
                list1.append(j.replace('"',''))

            df.columns=list1

            for i, j in  enumerate(df['column1']):
                df['column1'][i]=df['column1'][i].replace('"','')

            for i, j in  enumerate(df['column15']):
                df['column15'][i]=df['column15'][i].replace('"','')
        finally:
            df = df.drop(['column10','column11'],axis=1)
            df.to_csv(self.filename, index=False)


    def modifydata_RtnEnquiry(self):
        os.chdir(InventoryView.local_direc)

        df = pd.read_csv(self.filename)
        df = df.drop(['column10'],axis=1)
        df.to_csv(self.filename, index=False)


    def file_transfer(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=InventoryView.hostname, username=InventoryView.prod_username, password=InventoryView.prod_password)
        sftp_client = ssh_client.open_sftp()
        
        os.chdir(InventoryView.local_direc)

        if os.path.exists(self.filename):
            sftp_client.put(self.filename,InventoryView.prod_direc+self.filename)
            sftp_client.close()
            ssh_client.close()
            print('Success')
        else:
            print('File Not Found in your local directory')

    def delete_files(self):
        for i,j,k in os.walk(InventoryView.local_direc):
            for file in k:
                os.remove(file)


filename = 'filename1'+datetime.now().strftime('%Y%m%d')+'.csv'
a = InventoryView(filename)
a.ftp_download()
a.file_transfer()

filename = 'filename2'+datetime.now().strftime('%Y%m%d')+'.csv'
b= InventoryView(filename)
b.ftp_download()
b.modifydata_RtnEnquiry()
b.file_transfer()

filename = 'filename3'+datetime.now().strftime('%Y%m%d')+'.csv'
c = InventoryView(filename)
c.ftp_download()
c.modifydata_StdSales()
c.file_transfer()

filename = 'filename4'+datetime.now().strftime('%Y%m%d')+'.csv'
d = InventoryView(filename)
d.ftp_download()
d.modifydata_StdReturn()
d.file_transfer()

filename = 'filename5'+datetime.now().strftime('%Y%m%d')+'.csv'
e = InventoryView(filename)
e.ftp_download()
e.file_transfer()
e.delete_files()