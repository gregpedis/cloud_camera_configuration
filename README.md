# Configuration README

This repository contains configuration instructions and files for setting up a cloud camera.

There are, roughly speaking, three necessary aspects for setting this up:

* [Real-time access](#real-time-access) to the camera
* [FTP Server](#ftp-server) for storing the files
* [Cloud Storage](#cloud-storage) for backups


## Real-time Access

Setting up real-time access to a camera is relatively simple.

It is also completely decoupled from the rest of the configuration, so it's easy to start with it.

1. Set up a static ip address
2. update dns hostname
3. router port forward

## FTP Server

1. install vsftpd
2. add camera user
3. add usb mount to fstab
4. configure vsftpd.conf
5. install ufw
6. setup ufw tcp and ftp access
7. Enable vsftpd/ufw services
8. Disable shell for camera user


## Cloud Storage

1. install megacmd cli
2. create mega account
3. Execute mega-login
4. Configure backup schedule
