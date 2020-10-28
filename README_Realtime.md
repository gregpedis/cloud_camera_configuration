# Real-time Access

Access the **dhcp address reservation** panel in the router
and bind a lan ip address to the camera's mac address
in order to set a **static** local ip address.

---

The camera is exposed via a **port** to the local network.
**Port-forward**  from the router to the camera,
so that it is possible to be accessed outside of the LAN.

---

In order to acess the camera by a **hostname**, a **dynamic DNS provider** is necessary. 

The one i used is the free [Now-DNS](https://now-dns.com/?p=clients) and updating it is relatively easy.

In order to update the ip address and the domain name in a linux environment, 
copy [this script](/files/update_dns) in `/home/pi/bin`,
replacing all the necessary values with the ones from your dynamic dns provider account. 
If the directory does not exist, create it first.

After that, access the crontab of **user** via the following command.
<pre>crontab -e -u <b>&ltuser&gt</b></pre>

Add the following line at the end of the file.
<pre>*/3 * * * * /home/pi/bin/update_dns</pre>

Remote, real-time access to the camera should be working by now.
