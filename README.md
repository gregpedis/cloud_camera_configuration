# Configuration README

This repository contains configuration instructions and files for setting up a cloud camera.
There are, roughly speaking, three necessary aspects for setting this up:

* [Real-time access](README_Realtime.md) to the camera
* [FTP Server](README_FTP.md) for storing the files
* [Cloud Storage](README_Cloud.md) for backups

---

Also, there are configuration files provided, as well as some helpful examples and details text files.
The files are sorted based on their use case, which results in three folders:

* [ftp](ftp) - Configuration files for the ftp server.
* [cloud](cloud) - Configuration files for the cloud storage.
* [common](common) - Configuration files with general purpose.

The *.txt* files are usually examples, details or command-line outputs, 
whereas the rest of the files are segments or completed parts of the camera's ocnfriguration.

---

The system used has the following properties.

<pre>
<b>OS:</b> Raspbian GNU/Linux 10 (buster) armv7l
<b>Host:</b> Raspberry Pi 3 Model B Plus Rev 1.3
<b>Kernel:</b> 4.19.75-v7+
<b>Uptime:</b> 11 days, 1 hour, 19 mins
<b>Packages:</b> 891 (dpkg)
<b>Shell:</b> bash 5.0.3
<b>Terminal:</b> /dev/pts/0
<b>CPU:</b> BCM2835 (4) @ 1.400GHz
<b>Memory:</b> 174MiB / 926MiB
</pre>
