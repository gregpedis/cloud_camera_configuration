# Real-time Access

Setting up real-time access to a camera is relatively simple.

It is also completely decoupled from the rest of the configuration, so it's easy to start with it.

Setting a **static** ip address is needed. That is done by accessing the **dhcp address reservation** panel in the router
and binding a lan ip address to the camera's mac address.

---

The camera is exposed via a **port** to the local network. That port has to be **forwarded** by the router to the camera,
so that it is possible to be accessed outside of the local network.

---

Normal routers do not have a static external address, which results to an automatically updated dynamic one.
In order to keep that address static, a **dynamic DNS provider** is necessary. 
The one i used is the free [Now-DNS](https://now-dns.com/?p=clients) and updating it is relatively easy.
In order to update the ip address and the domain name in a linux environment, 
a single line of code should be added to the user's **crontab**. 
To access that crontab, just use the following command.

`crontab -e -u <user>`

Add a new line with the following code, 
replacing all the needed values with the ones from your dynamic dns provider account.

`curl -u <email>:<password> "https://now-dns.com/update?hostname=<hostname>"`

Remote, real-time access to the camera should be working by now.
