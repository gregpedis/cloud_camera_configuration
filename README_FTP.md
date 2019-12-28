# FTP Server

Initially, some packages are needed.

```
sudo apt update
sudo apt install vsftpd ufw -y
```

*Updating the list of packages before installing any of them is always not a terrible idea.*

`vsftpd` stands for **very secure ftp daemon** and is one of most used and easiest to setup FTP services.

`ufw` stands for **uncomplicated firewall** and is a higher level interface for handling the device's firewall, 
which is necessary for opening the FTP server's needed **ports**.

---

Let's say that the user using the FTP will be called **camera** and the ftp's directory will be `/home/camera/ftp`.

Open the mentioned ports via the ufw cli.

```
sudo ufw allow 20/tcp
sudo ufw allow 21/tcp
sudo ufw allow 990/tcp
sudo ufw allow 40000:50000/tcp

sudo ufw status
```

The result should look like this.

```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere                  
20/tcp                     ALLOW       Anywhere                  
21/tcp                     ALLOW       Anywhere                  
40000:50000/tcp            ALLOW       Anywhere                  
990/tcp                    ALLOW       Anywhere                  
OpenSSH (v6)               ALLOW       Anywhere (v6)             
20/tcp (v6)                ALLOW       Anywhere (v6)             
21/tcp (v6)                ALLOW       Anywhere (v6)             
40000:50000/tcp (v6)       ALLOW       Anywhere (v6)             
990/tcp (v6)               ALLOW       Anywhere (v6) 
```

---

Add the new **camera** user and then create the **ftp directory** with the right **owner** and **permissions**.

```
sudo adduser camera

sudo mkdir /home/camera/ftp
sudo chown nobody:nogroup /home/camera/ftp
sudo chmod a-w /home/camera/ftp
```

Create a directory where the actual camera files reside.
This is necessary to achieve a **chroot** jail, which makes the setup even more secure.

```
sudo mkdir /home/camera/ftp/files
sudo chown camera:camera /home/camera/ftp/files
```

What happens is that the `/home/camera/ftp` directory will be the FTP's **chroot** which does not have write privileges, 
while the `/home/camera/ftp/files` will be the directory that the camera writes to.

---

You might want to use an external device as your storage, so next up is mounting said block device.
Run the following command to check your pre-existing devices.

`ls -lA /dev/disk/by-uuid`

Then plug the device and run the same command again.
You should find a new entry in the list of devices, since the system discovers it automatically.
For example, by plugging a usb dongle there should be a new device named **sda**-*something*.

<pre><i>lrwxrwxrwx 1 root root 10 Dec 26 12:56</i> <b>2653-CF8E</b> -> ../../sda1</pre>

The important thing here is the **UUID**, marked with bold, 
since it's the unique id necessary for the system to auto-mount the device on reboot.
Edit `/etc/fstab` and add the following line at the end, 
replacing the *\<my-usb-uuid\>* with your device's **UUID**.

<pre><b>UUID</b>=<i>&ltmy-usb-uuid&gt</i> home/camera/ftp/files <b>auto nosuid,nodev,nofail</b> 0 0</pre>

With this directory/mounting configuration,
the path `/home/camera/ftp/files` can map to either **external** device or the **internal** filesystem,
depending on fstab finding the device during startup. Neat.

---

It's time to actually configure **vsftpd**. The way that happens is by editing the *.conf* file of the service,
which exists at `/etc/vsftpd.conf`. Saving the original configuration as backup is always a wise decision.

`sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.orig`

The necessary configuration is [linked here](ftp/vsftpd.conf).

To add the ***camera*** user to the accepted list of ftp users execute the following command.

`echo "camera" | sudo tee -a /etc/vsftpd.userlist`

In order for the `vsftpd` and `ufw` services to start on every system **reboot**, they have to be **enabled**.

`sudo systemctl enable vsftpd ufw`

---

Disabling the shell access of the ***camera*** user 
is a good step towards better securing the server's protection against malicious intent.
That means that the logging as the ***camera*** user will not be possible.

Copy [this file](ftp/ftponly) in the `/bin` directory.

Alter the file's permissions as follows.

`sudo chmod a+x /bin/ftponly`

Add the new shell new shell to the list of shells.

`echo "/bin/ftponly" | sudo tee -a /etc/shells`

Update the user's shell with the following command.

`sudo usermod camera -s /bin/ftponly`

---

Everything should be working as intended after restarting the device via `sudo reboot`.

For more information on the FTP Server's configuration, [this article](https://www.digitalocean.com/community/tutorials/how-to-set-up-vsftpd-for-a-user-s-directory-on-ubuntu-16-04) by *Melissa Anderson* is very useful.
