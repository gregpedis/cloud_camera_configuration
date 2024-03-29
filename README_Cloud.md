# Cloud Storage (pCloud)

The cloud storage service to be used is [pCloud](https://my.pcloud.com/) since it's free and provides a simple and easy to use API.

---

Firstly, create a pCloud account [here](https://my.pcloud.com/register). 

The username and password will be necessary in the synchronization circle.

---
The entire cloud process will be done via two python scripts, so initially we have to install **python3**, as following.

<pre>sudo apt install python3 -y</pre>

There are two files that do the necessary file system operations, as following.

- [local operations](files/operations_local.py) which removes the local ftp files if they are too old.
- [cloud operations](files/operations_cloud.py) which removes and uploads files to the pCloud file system.

Copy both of these files in the `/home/camera` directory.

Add the user that will be running the scripts to the camera group. This is important because of file permissions on the ftp server.

<pre>sudo usermod -a -G camera <b>&ltuser&gt</b></pre> 

It is important to set some parameters in both scripts, residing at the top level of each of them.

Keep in mind that both scripts are designed to be executed in late night/early morning times, generally after midnight.

---

For the **local operations script**, the configuration is as follows:

<pre>
<b>DAYS_BACK</b> = 5
<b>FTP_FOLDER</b> = '/home/camera/ftp/files'
</pre>

- *FTP_FOLDER* is self-explanatory and most likely does not need changing.

- *DAYS_BACK* option configures which day's files to delete. The formula is **Script_execution_date minus DAYS_BACK**.

*For example, if you want to delete the last day's files and the script is running at 1:00 AM, DAYS_BACK should be 1.*

---

For the **cloud operations script**, the configuration is as follows:

<pre>
BASE_ENDPOINT = "https://api.pcloud.com/"
<b>BASE_PATH</b> = "/camera_files"
<b>FTP_FOLDER</b> = '/home/camera/ftp/files/'

<b>DAYS_BACK_DELETE</b> = 5
<b>DAYS_BACK_UPLOAD</b> = 1

<b>username</b> = "placeholder"
<b>password</b> = "placeholder"
expire_seconds = 36000
expire_inactive_seconds = 36000

method_auth = "userinfo"
method_listfolder = "listfolder"
method_deletefolder = "deletefolderrecursive"
method_createfolder = "createfolderifnotexists"
method_uploadfile = "uploadfile"
</pre>

- *FTP_FOLDER* is self-explanatory and most likely does not need changing.

- *BASE_PATH* defines the root folder in the pCloud file system and a directory with the same name should be manually created on your pCloud filesystem.

- *DAYS_BACK_DELETE* behaves the same way as *DAYS_BACK* does on the local operations script, but instead removes remote files.

- *DAYS_BACK_UPLOAD* behaves the same way as *DAYS_BACK* does on the local operations script, but instead uploads remote files.

- *username* is your pCloud account's username.

- *password* is your pCloud account's password.

The *BASE_ENDPOINT*, *expire* options and *method* options define boilerplate configuration for pCloud's api, so no alterations needed.

---

After setting up the files and the configuration of the files, the scheduling needs to be setup.

Access the crontab of **user** via the following command.
<pre>crontab -e -u <b>&ltuser&gt</b></pre> 

Add the following lines at the end of the file.

<pre>
0 2 * * * sudo /usr/bin/python3 /home/camera/operations_<b>local</b>.py

0 4 * * * sudo /usr/bin/python3 /home/camera/operations_<b>cloud</b>.py
</pre>

---
Finally, since i'm using a raspberry pi, a device overheat is possible so logging the temperature is quite useful.

Copy [this file](files/log_temperature) in the `/home/pi/bin` directory.

Access the crontab of **user** via the following command.
<pre>crontab -e -u <b>&ltuser&gt</b></pre>

Add the following line at the end of the file.

<pre>15,30,45 * * * * /home/pi/bin/log_temperature</pre>

---
The configuration should be complete by now.

For reference, [this](files/crontab.txt) is what your crontab file should contain. 
