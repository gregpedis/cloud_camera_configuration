# Configuration README

This repository contains configuration instructions and files for setting up a cloud camera.

There are, roughly speaking, three necessary aspects for setting this up:

* [Real-time access](#real-time-access) to the camera
* [FTP Server](#ftp-server) for storing the files
* [Cloud Storage](#cloud-storage) for backups


## Real-time Access

Setting up real-time access to a camera is relatively simple.

It is also completely decoupled from the rest of the configuration, so it's easy to start with it.

First, setting a **static** ip address is needed. That is done by accessing the *dhcp address reservation* panel in the router
and binding a lan ip address to the camera's mac address.

Secondly, the camera is exposed via a **port** to the local network. That port has to be **forwarded** by the router to the camera,
so that it is possible to be accessed outside of the local network.

Thirdly, normal routers do not have a static external address, which results to a automatically updated dynamic one.
In order to keep that address static, a **dynamic DNS provider** is necessary. 
The one i used is [now-dns](https://now-dns.com/?p=clients) and updating is relatively easy.
In order to update the ip address and the domain name in a linux environment, a single line of code should be added to the user's **crontab**. To access that crontab, just use the following command.

`crontab -e -u <user>`

Add a new line with the following code, replacing all the needed values with the ones from your dynamic dns provider account.

`curl -u <email>:<password> "https://now-dns.com/update?hostname=<hostname>"`

## FTP Server

### install vsftpd

good stuff

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
