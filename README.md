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

The *.txt* files usually are examples, details or command-line outputs, 
whereas the rest of the files are segments or completed parts of the camera's ocnfriguration.

---

The system used has the following properties.

```
OS: Raspbian GNU/Linux 10 (buster) armv7l
Host: Raspberry Pi 3 Model B Plus Rev 1.3
Kernel: 4.19.75-v7+
Uptime: 11 days, 1 hour, 19 mins
Packages: 891 (dpkg)
Shell: bash 5.0.3
Terminal: /dev/pts/0
CPU: BCM2835 (4) @ 1.400GHz
Memory: 174MiB / 926MiB
```
