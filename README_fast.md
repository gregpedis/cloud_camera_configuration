# Real-time

- dhcp address reservation -> static IP
- Port-forward from router to camera 
- create account to [Now-DNS](https://now-dns.com/?p=clients)
- `sudo cp ./files/update_dns /home/pi/bin `
- add ` */3 * * * * /home/pi/bin/update_dns` to crontab by `crontab -e -u pi`

# FTP 

- `sudo apt update && apt install vsftpd ufw -y`
- `sudo ufw allow 20/tcp`
- `sudo ufw allow 21/tcp`
- `sudo ufw allow 990/tcp`
- `sudo ufw allow 40000:50000/tcp`
- `sudo ufw status` to check results
- `sudo adduser camera`
- `sudo mkdir /home/camera/ftp`
- `sudo chown nobody:nogroup /home/camera/ftp`
- `sudo chmod a-w /home/camera/ftp`
- `sudo mkdir /home/camera/ftp/files`
- `sudo chown camera:camera /home/camera/ftp/files`
- `sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.orig`
- `sudo cp ./files/vsftpd.conf /etc`
- `echo "camera" | sudo tee -a /etc/vsftpd.userlist`
- `sudo systemctl enable vsftpd ufw`
- `sudo cp ./files/ftponly /bin`
- `sudo chmod a+x /bin/ftponly`
- `echo "/bin/ftponly" | sudo tee -a /etc/shells`
- `sudo usermod camera -s /bin/ftponly`

# Cloud

- `sudo apt install python3 -y`
- `sudo cp ./files/operations_local.py /home/camera/ftp`
- `sudo cp ./files/operations_cloud.py /home/camera/ftp`
- change config parameters for local and cloud scripts
- add `0 2 * * * /usr/bin/python3 /home/camera/operations_local.py` on crontab
- add `0 4 * * * /usr/bin/python3 /home/camera/operations_cloud.py` on crontab
