import os
import requests
import datetime as dt

BASE_ENDPOINT = "https://api.pcloud.com/"
BASE_PATH = "/camera_files"
FTP_FOLDER = '/home/camera/ftp/files/'

DAYS_BACK_DELETE = 6
DAYS_BACK_UPLOAD = 1

username = "<enter_email_address>"
password = "<enter_password>"
expire_seconds = 36000
expire_inactive_seconds = 36000

method_auth = "userinfo"
method_listfolder = "listfolder"
method_deletefolder = "deletefolderrecursive"
method_createfolder = "createfolderifnotexists"
method_uploadfile = "uploadfile"
UPLOADED_FILES_GRANULARITY = 25


def generate_foldername(days_back=0):
    date = dt.date.today() - dt.timedelta(days=days_back)
    foldername = f"{date.year}_{date.month}_{date.day}"
    return foldername


def to_be_uploaded(f):
    ctime = os.path.getctime(f)
    mtime = os.path.getmtime(f)

    if ctime >= 0 and mtime >= 0:
        time = min(ctime, mtime)
    elif ctime >= 0:
        time = ctime
    elif mtime >= 0:
        time = mtime
    else:
        return False

    creation_date = dt.date.fromtimestamp(time)
    delta = dt.date.today() - creation_date
    return delta.days == DAYS_BACK_UPLOAD


def get_files():
    os.chdir(FTP_FOLDER)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    valid_files = [f for f in files if to_be_uploaded(f)]
    return valid_files

    
def generate_token():
    endpoint = BASE_ENDPOINT+method_auth
    data = {
        "username": username,
        "password": password,
        "authexpire": expire_seconds,
        "authinactiveexpire": expire_seconds,
        "getauth": True
    }

    result = requests.post(endpoint, data=data)
    result_json = result.json()
    auth = result_json["auth"]
    return auth


def list_base_folder(token):
    endpoint = BASE_ENDPOINT + method_listfolder
    data = {
        "auth": token,
        "path": BASE_PATH,
        "nofiles": 1,
        "recursive": 1
    }

    result = requests.post(endpoint, data=data)
    result_json = result.json()

    values = result_json["metadata"]["contents"]
    folders = [v["name"] for v in values]
    return folders


def delete_folder(token):
    foldername = generate_foldername(DAYS_BACK_DELETE)
    folders = list_base_folder(token)

    if foldername in folders:
        endpoint = BASE_ENDPOINT + method_deletefolder
        data = {
            "auth": token,
            "path": f"{BASE_PATH}/{foldername}"
        }

        result = requests.post(endpoint, data=data)
        result_json = result.json()
        return result_json


def create_base_folder(token):
    endpoint = BASE_ENDPOINT + method_createfolder
    data = {
            "auth": token,
            "path": BASE_PATH
    }

    result = requests.post(endpoint, data=data)
    result_json = result.json()
    return result_json


def create_folder(token):
    foldername = generate_foldername(DAYS_BACK_UPLOAD)
    endpoint = BASE_ENDPOINT + method_createfolder
    data = {
        "auth": token,
        "path": f"{BASE_PATH}/{foldername}"
    }

    result = requests.post(endpoint, data=data)
    result_json = result.json()
    return result_json


def upload_files(token):
    foldername = generate_foldername(DAYS_BACK_UPLOAD)
    endpoint = BASE_ENDPOINT + method_uploadfile
    data = {

        "auth": token,
        "path": f"{BASE_PATH}/{foldername}",
        "nopartial": 1,
    }

    files = get_files()
    chunks = [files[x:x+UPLOADED_FILES_GRANULARITY] 
            for x in range(0, len(files), UPLOADED_FILES_GRANULARITY)]
    
    for chunk in chunks:
        keyvalues = {} 
        for f in chunk:
            keyvalues[f] = open(f, 'rb')
        result = requests.post(endpoint, data=data, files=keyvalues)


def main():
    token = generate_token()
    create_base_folder(token)
    delete_folder(token)
    create_folder(token)
    upload_files(token)


if __name__ == "__main__":
    main()
