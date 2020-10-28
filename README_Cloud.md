# Cloud Storage

The cloud storage service to be used is [pCloud](https://my.pcloud.com/) since it's free and provides a simple and easy to use API.

---

Firstly, create a pCloud account [here](https://my.pcloud.com/register). 

The username and password will be necessary in the synchronization circle.

---
The entire cloud process will be done via two python scripts, so initially we have to install python, as following.

`sudo apt install python3 -y`

There are two files that do the necessary file system operations, as following.

- [local operations](files/operations_local.py) which removes the local ftp files if they are too old.
- [cloud operations](files/operations_cloud.py) which removes and uploads files to the pCloud file system.

Copy both of these files in the `/home/camera/ftp` directory.

----



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

For reference, [this](files/crontab.txt) is what your crontab file should contain. 
