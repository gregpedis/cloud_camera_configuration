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

The `mega-tools` package contains lots of cli commands, but the ones we are going to use are the following.

| Command | Functionality |
| ------- | ------------- |
| mega-login  | Logins with a user's credentials         |
| mega-server | Initializes a daemon running the backups |
| mega-backup | Configures the backup scheduling         |

*For more information on the cli commands, 
check [MEGAcmd's documentation](https://github.com/meganz/MEGAcmd/blob/master/UserGuide.md).*

---
Create a MEGA account [here](https://mega.nz/register).
After that everything should be ready to start configuring a backup schedule,
meaning the ftp files directory will be copied at a set time interval.

Logging in with the user's credentials is an one time thing, since the MEGA service keeps the information in the device indefinitely.
That being said, execute the following, while replacing the necessary values with your account's details.

<pre>mega-login <i>&ltemail&gt</i> <i>&ltpassword&gt</i></pre>

---
Before configuring the backup schedule, 
it is important to initialize the mega-server daemon on a possible system reboot,
since it is the one responsible for scheduling the backups.

MEGA tools do not supply that functionality,
which means we have to create our own systemd service to start the daemon.

Copy [this file](files/megaCmdServer.service) in `/etc/systemd/system`.

After that, **start** and **enable** the service and check if everything runs smoothly.
```
sudo systemctl start megaCmdServer
sudo systemctl enable megaCmdServer
sudo systemctl status megaCmdServer
```

The result should look like this.
<pre>
● megaCmdServer.service - Starting the mega-cmd-server that backups the necessary files.
   Loaded: <b>loaded (/etc/systemd/system/megaCmdServer.service; enabled</b>; vendor preset: enabled)
   Active: <b>active (running)</b> since Tue 2019-12-31 14:27:43 EET; 24h ago
 Main PID: 592 (mega-cmd-server)
    Tasks: 14 (limit: 2200)
   Memory: 32.7M
   CGroup: /system.slice/megaCmdServer.service
           └─592 /usr/bin/mega-cmd-server
</pre>

---
To configure a backup schedule, we are going to use the `mega-backup` command.

Create a folder on your MEGA account storage and name it `Camera_Files`. After that, execute the following command.
```
sudo mega-backup /home/camera/ftp/files /Camera_Files --period="0 0 20 * * *" --num-backups=7 
```
What this does is configure a backup of `/home/camera/ftp/files` in the `Camera_Files` remote folder, 
**every day at midnight**, while preserving the last **7 backups**.

For some reason, backups run **4 hours after** scheduled, 
which is why my configuration has the **hour** parameter in the cron-like syntax set to **20**.
What this means is since the backup should run at **midnight**, it should be configured **4 hours** before midnight.

Check if the backup schedule configuration is correct. 
```
sudo mega-backup -l
```

The result should look like the following snippet.
```
TAG   LOCALPATH                                      REMOTEPARENTPATH                                       STATUS
5     /home/camera/ftp/files                         /Camera_Files                                          ACTIVE
  Max Backups:   7
  Period:         "0 0 20 * * *"
  Next backup scheduled for: Sun, 04 Mar 1979 22:00:00 +0200
```

*For more information on how MEGA backups work, 
[click here](https://github.com/meganz/MEGAcmd/blob/master/contrib/docs/BACKUPS.md).*

---
Now we need to clean the files directory so that the daily backup format is achieved.
We are going to use a python script to delete every file added during the previous days.

To begin with, install **python3**.

`sudo apt install python3`

After that, copy [this file](files/folder_cleanse.py) in the `/home/camera` directory.

Access the crontab of **user** via the following command.
<pre>crontab -e -u <b>&ltuser&gt</b></pre>

Add the following line at the end of the file.

`0 4 * * * sudo /usr/bin/python3 /home/camera/folder_cleanse.py`

---
Finally, since i'm using a raspberry pi, a device overheat is possible so logging the temperature is quite useful.

Copy [this file](files/log_temperature) in the `/home/pi/bin` directory.

Access the crontab of **user** via the following command.
<pre>crontab -e -u <b>&ltuser&gt</b></pre>

Add the following line at the end of the file.

`15,30,45 * * * * /home/pi/bin/log_temperature`

---
The configuration should be complete by now.
For reference, [this](files/crontab.txt) is how your crontab file should look. 
