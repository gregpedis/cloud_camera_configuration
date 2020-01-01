# Cloud Storage

The cloud storage service to be used is [MEGA](https://mega.nz/start) since it's free and provides command-line interface tools.

First install the necessary dependencies.

For a Debian/Ubuntu with QT >= 5.6 (e.g: Ubuntu 18.04):
```
sudo apt install libzen-dev libmediainfo-dev debhelper qtbase5-dev qt5-qmake qt4-linguist-tools libqt5dbus5 libqt5svg5-dev libcrypto++-dev libraw-dev libc-ares-dev libssl-dev libsqlite3-dev zlib1g-dev wget dh-autoreconf cdbs unzip libtool-bin pkg-config qt5-default qttools5-dev-tools libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libmediainfo-dev
```

For older Debian/Ubuntu based systems (e.g: Ubuntu 16.04):
```
sudo apt install build-essential autoconf automake m4 libtool libtool-bin qt4-qmake make libqt4-dev libcrypto++-dev libsqlite3-dev libc-ares-dev libcurl4-openssl-dev libssl-dev libraw-dev libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libmediainfo-dev
```

After that, install the actual cli tools.
```
sudo apt install megatools
```

---
Create a MEGA account [here](https://mega.nz/register).
After that everything should be ready to start configuring a backup schedule,
meaning the ftp files directory will be copied at a daily interval.

The `mega-tools` package contains lots of cli commands, but the ones we are going to use are the following.

| Command | Description |
| ------- | ----------- |
| mega-server | Initializes a daemon running the backups |
| mega-login  | Logins with a user's credentials         |
| mega-backup | Handles the backup scheduling            |

---
3. Execute mega-login

---
4. Configure backup schedule

---
