import os
import datetime as dt

DAYS_BACK = 2
FTP_FOLDER = '/home/camera/ftp/files/'


def to_be_deleted(f):
    ctime = os.path.getctime(f)
    mtime = os.path.getmtime(f)  # OS differences are tricky.

    if ctime >= 0 and mtime >= 0:
        time = min(ctime, mtime)
    elif ctime >= 0:
        time = ctime
    elif mtime >= 0:
        time = mtime
    else:
        return True

    creation_date = dt.date.fromtimestamp(time)
    delta = dt.date.today() - creation_date
    return delta.days >= DAYS_BACK


def remove_files(files):
    for f in files:
        os.remove(f)


def main():
    os.chdir(FTP_FOLDER)
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(FTP_FOLDER) for f in filenames]

    old_files = [f for f in files if to_be_deleted(f)]
    remove_files(old_files)


if __name__ == "__main__":
    main()
