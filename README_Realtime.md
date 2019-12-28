# Real-time Access

Access the **dhcp address reservation** panel in the router
and bind a lan ip address to the camera's mac address
in order to set a **static** ip address.

---

The camera is exposed via a **port** to the local network.
**Port-forward**  from the router to the camera
so that it is possible to be accessed outside of the local network.

---

Normal routers do not have a static external address, which results to an automatically updated dynamic one.
In order to keep that address static, a **dynamic DNS provider** is necessary. 
The one i used is the free [Now-DNS](https://now-dns.com/?p=clients) and updating it is relatively easy.

In order to update the ip address and the domain name in a linux environment, 
access the crontab of **user** via the following command.

<pre>crontab -e -u <b>&ltuser&gt</b></pre>

Add the following line, 
replacing all the needed values with the ones from your dynamic dns provider account.

<pre>curl -u <b>&ltemail&gt</b>:<b>&ltpassword&gt</b> "https://now-dns.com/update?hostname=<b>&lthostname&gt</b>"</pre>

Remote, real-time access to the camera should be working by now.
