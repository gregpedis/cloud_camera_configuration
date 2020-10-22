import os
import datetime as dt

DAYS_BACK = 5
FTP_FOLDER = '/home/camera/ftp/files/'


def is_old(f):
    ctime = os.path.getctime(f)
    mtime = os.path.getmtime(f)  # OS differences are tricky.

    creation_date = dt.date.fromtimestamp(min(ctime, mtime))
    delta = dt.date.today() - creation_date
    return delta.days >= DAYS_BACK


def remove_files(files):
    for f in files:
        os.remove(f)


def main():
    os.chdir(FTP_FOLDER)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]

    old_files = [f for f in files if is_old(f)]
    remove_files(old_files)


if __name__ == "__main__":
    main()
