import os
import time

BACKUP_INTERVAL = 14400
THRESHOLD = time.time() - BACKUP_INTERVAL

FTP_FOLDER = '/home/camera/ftp/files/'
os.chdir(FTP_FOLDER)

files = [f for f in os.listdir('.') if os.path.isfile(f)]
old_files = [f for f in files if os.path.getctime(f) < THRESHOLD]

for f in old_files:
        os.remove(f)
        
