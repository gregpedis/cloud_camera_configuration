import os
import requests
import datetime as dt

BASE_ENDPOINT = "https://api.pcloud.com/"
BASE_PATH = "/some2"
FTP_FOLDER = '/home/camera/ftp/files/'
DAYS_BACK_DELETE = 5
DAYS_BACK_UPLOAD = 1

username = "trafalgar1618@hotmail.com"
password = "yaft9BAUH.sqay0waus"
expire_seconds = 7200
expire_inactive_seconds = 3600

method_auth = "userinfo"
method_listfolder = "listfolder"
method_deletefolder = "deletefolderrecursive"
method_createfolder = "createfolderifnotexists"
method_uploadfile = "uploadfile"


def generate_foldername(days_back=0):
    date = dt.date.today() - dt.timedelta(days=days_back)
    foldername = f"{date.year}_{date.month}_{date.day}"
    return foldername


def to_be_uploaded(f):
    ctime = os.path.getctime(f)
    mtime = os.path.getmtime(f)
    creation_date = dt.date.fromtimestamp(min(ctime, mtime))
    delta = dt.date.today() - creation_date
    return delta.days == DAYS_BACK_UPLOAD


def get_files():
    os.chdir(FTP_FOLDER)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    valid_files = [f for f in files if to_be_uploaded(f)]

    keyvalues = {}
    for f in valid_files:
        keyvalues[f] = open(f, 'rb')
    return keyvalues


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

    result = requests.post(endpoint, data=data, files=files)
    result_json = result.json()
    return result_json


def main():
    token = generate_token()
    delete_folder(token)
    create_folder(token)
    upload_files(token)
    pass


if __name__ == "__main__":
    main()
