# FTP Server

# Reminder to add usb mount to fstab

Setting up an ftp server requires slightly more complicated configuration.

Initially, some packages are needed.

`sudo apt update`

*Updating the list of packages before installing any of them is always not a terrible idea.*

`sudo apt install vsftpd ufw -y`

`vsftpd` stands for **very secure ftp daemon** and is one of most used and easiest to setup FTP services.

`ufw` stands for **uncomplicated firewall** and is a higher level interface for handling the device's firewall, 
which is necessary for opening the FTP server's needed **ports**.

Let's say that the user using the FTP will be called ***camera*** and the ftp's directory will be ***/home/camera/ftp***.

Firstly, opening the mentioned ports via the ufw cli.

`sudo ufw allow 20/tcp`

`sudo ufw allow 21/tcp`

`sudo ufw allow 990/tcp`

`sudo ufw allow 40000:50000/tcp`

Checking if the ports are indeed open.

`sudo ufw status/tcp`

After that, adding the new ***camera*** user.

`sudo adduser camera`

While also creating the **ftp directory** with the right **owner** and **permissions**.

`sudo mkdir /home/camera/ftp`

`sudo chown nobody:nogroup /home/camera/ftp`

`sudo chmod a-w /home/camera/ftp`


Also, creating a directory where the actual camera files reside.
This is necessary to achieve a `chroot` jail, which makes this ftp setup even more secure.

`sudo mkdir /home/camera/ftp/files`

`sudo chown camera:camera /home/camera/ftp/files`

What happens is that the ***/home/camera/ftp*** directory will be the FTP's `chroot` which does not have write privileges, 
while the ***/home/camera/ftp/files*** will be the directory that the camera writes to.

After all that, it's time to actually configure **vsftpd**. The way that happens is by editing the *.conf* file of the service,
which exists at */etc/vsftpd.conf*. Saving the original configuration as backup is always a wise decision.

`sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.orig`

The necessary configuration is [linked here](#cloud-storage).

To add the ***camera*** user to the accepted list of ftp users, the following command needs to be executed.

`echo "camera" | sudo tee -a /etc/vsftpd.userlist`

In order for the `vsftpd` and `ufw` services to start on every system **reboot**, they have to be **enabled**.

`sudo systemctl enable vsftpd ufw`

Finally, disabling the shell access of the ***camera*** user is a good step towards better securing the server's protection against malicious intent.
That means that the logging as the ***camera*** user will not be possible.

Copy [this file](#somesome) in the `/bin` directory.

Alter the file's permissions as follows.

`sudo chmod a+x /bin/ftponly`

Add the new shell new shell to the list of shells.

`echo "/bin/ftponly" | sudo tee -a /etc/shells`

Update the user's shell with the following command.

`sudo usermod camera -s /bin/ftponly`

Everything should be working as intended after restarting the device.

For more information on the FTP Server's configuration, [this article](https://www.digitalocean.com/community/tutorials/how-to-set-up-vsftpd-for-a-user-s-directory-on-ubuntu-16-04) by *Melissa Anderson* is very useful.
